from __future__ import annotations

import csv
import os
import unittest
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch

from week10.fintrust_migration import __all__ as public_api
from week10.fintrust_migration.ec2.classifier import classify_instances, get_migration_wave
from week10.fintrust_migration.ec2.mgn_helpers import list_source_servers
from week10.fintrust_migration.orchestrator import lambda_handler as orchestrator_handler
from week10.fintrust_migration.rds.dms_helpers import (
    get_all_task_health,
    get_cdc_latency,
    get_task_status,
    is_cutover_ready,
    start_task,
    wait_for_status,
)
from week10.fintrust_migration.s3.sync_helpers import (
    get_execution_status,
    lambda_handler as throttle_handler,
    monitor_nightly_transfers,
    set_task_throttle,
    start_task_execution,
    wait_for_execution,
)
from week10.fintrust_migration.utils.sessions import get_cross_account_session
from week10.fintrust_migration.utils.transfer_costs import compare_transfer_costs


ROOT = Path(__file__).resolve().parents[2]


class RecordingClient:
    def __init__(self, responses=None):
        self.responses = list(responses or [])
        self.calls = []

    def __getattr__(self, name):
        def operation(**kwargs):
            self.calls.append((name, kwargs))
            if self.responses:
                response = self.responses.pop(0)
                if isinstance(response, Exception):
                    raise response
                return response
            return {}

        return operation


class FakePaginator:
    def __init__(self, pages):
        self.pages = pages

    def paginate(self, **kwargs):
        del kwargs
        yield from self.pages


class PagedClient(RecordingClient):
    def __init__(self, pages):
        super().__init__()
        self.pages = pages

    def get_paginator(self, name):
        self.calls.append(("get_paginator", {"name": name}))
        return FakePaginator(self.pages)


def instance(identifier, strategy=None, wave=None):
    tags = [{"Key": "Name", "Value": f"server-{identifier}"}]
    if strategy:
        tags.append({"Key": "migration:strategy", "Value": strategy})
    if wave:
        tags.append({"Key": "migration:wave", "Value": str(wave)})
    return {
        "InstanceId": identifier,
        "InstanceType": "m5.large",
        "State": {"Name": "running"},
        "Tags": tags,
    }


def task_response(status="running", tables_errored=0):
    return {
        "ReplicationTasks": [
            {
                "ReplicationTaskArn": "arn:task",
                "ReplicationTaskIdentifier": "oracle-to-aurora",
                "Status": status,
                "ReplicationTaskStats": {"TablesLoaded": 20, "TablesErrored": tables_errored},
                "StopReason": "connection failed" if status == "failed" else None,
            }
        ]
    }


class Clock:
    def __init__(self, values):
        self.values = iter(values)

    def __call__(self):
        return next(self.values)


class WeekTenTests(unittest.TestCase):
    def test_public_api_contains_required_functions(self):
        required = {
            "classify_instances",
            "get_migration_wave",
            "get_task_status",
            "start_task",
            "stop_task",
            "wait_for_status",
            "get_cdc_latency",
            "is_cutover_ready",
            "start_task_execution",
            "get_execution_status",
            "wait_for_execution",
            "set_task_throttle",
        }
        self.assertTrue(required.issubset(set(public_api)))

    def test_cross_account_session_uses_temporary_credentials(self):
        sts = RecordingClient(
            [
                {
                    "Credentials": {
                        "AccessKeyId": "temporary-access",
                        "SecretAccessKey": "temporary-secret",
                        "SessionToken": "temporary-token",
                    }
                }
            ]
        )

        class BaseSession:
            region_name = "af-south-1"

            def client(self, service):
                self.service = service
                return sts

        created = {}

        def factory(**kwargs):
            created.update(kwargs)
            return "session"

        result = get_cross_account_session(
            "arn:aws:iam::111122223333:role/MigrationReadOnly",
            base_session=BaseSession(),
            session_factory=factory,
        )
        self.assertEqual(result, "session")
        self.assertEqual(created["aws_session_token"], "temporary-token")
        self.assertEqual(sts.calls[0][0], "assume_role")

    def test_transfer_costs_match_supplied_components(self):
        result = compare_transfer_costs("3000")
        self.assertEqual(result["device_count"], 38)
        self.assertEqual(result["datasync_total_usd"], Decimal("37896.00"))
        self.assertEqual(result["snowball_total_usd"], Decimal("28100.00"))
        self.assertEqual(result["hybrid_total_usd"], Decimal("31850.00"))

    def test_application_portfolio_totals_285(self):
        with (ROOT / "week10" / "data" / "application-portfolio.csv").open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(sum(int(row["application_count"]) for row in rows), 285)
        self.assertEqual(sum(int(row["portfolio_percent"]) for row in rows), 100)

    def test_classifier_handles_pages_and_unresolved_tags(self):
        client = PagedClient(
            [
                {"Reservations": [{"Instances": [instance("i-1", "Rehost", 1)]}]},
                {"Reservations": [{"Instances": [instance("i-2")]}]},
            ]
        )
        portfolio, unresolved = classify_instances(client)
        self.assertEqual(portfolio["rehost"][0]["name"], "server-i-1")
        self.assertEqual(unresolved[0]["id"], "i-2")

    def test_wave_filter_and_validation(self):
        client = PagedClient(
            [{"Reservations": [{"Instances": [instance("i-1", "rehost", 1), instance("i-2", "refactor", 2)]}]}]
        )
        self.assertEqual([item["id"] for item in get_migration_wave(1, client)], ["i-1"])
        with self.assertRaises(ValueError):
            get_migration_wave(4, client)

    def test_mgn_inventory_handles_next_token(self):
        client = RecordingClient(
            [
                {
                    "items": [
                        {
                            "sourceServerID": "s-1",
                            "sourceProperties": {"identificationHints": {"hostname": "legacy-app"}},
                            "dataReplicationInfo": {"dataReplicationState": "CONTINUOUS", "lagDuration": "PT4S"},
                            "lifeCycle": {"state": "READY_FOR_TEST"},
                        }
                    ],
                    "nextToken": "next",
                },
                {"items": []},
            ]
        )
        result = list_source_servers(client)
        self.assertEqual(result[0]["hostname"], "legacy-app")
        self.assertEqual(client.calls[1][1]["nextToken"], "next")

    def test_dms_status_and_missing_task(self):
        status = get_task_status("arn:task", RecordingClient([task_response()]))
        self.assertEqual(status["identifier"], "oracle-to-aurora")
        with self.assertRaises(ValueError):
            get_task_status("arn:missing", RecordingClient([{"ReplicationTasks": []}]))

    def test_full_dms_restart_requires_approval(self):
        client = RecordingClient([{"ReplicationTask": {"Status": "starting"}}])
        with self.assertRaises(PermissionError):
            start_task("arn:task", "start-replication", client, wait=False)
        start_task("arn:task", "start-replication", client, allow_full_restart=True, wait=False)
        self.assertEqual(client.calls[0][1]["StartReplicationTaskType"], "start-replication")

    def test_resume_dms_is_default(self):
        client = RecordingClient([{"ReplicationTask": {"Status": "starting"}}])
        result = start_task("arn:task", dms_client=client, wait=False)
        self.assertEqual(result["Status"], "starting")
        self.assertEqual(client.calls[0][1]["StartReplicationTaskType"], "resume-processing")

    def test_wait_for_dms_handles_failure(self):
        client = RecordingClient([task_response("starting"), task_response("failed")])
        with self.assertRaisesRegex(RuntimeError, "connection failed"):
            wait_for_status(
                "arn:task",
                "running",
                client,
                sleep=lambda seconds: None,
                clock=Clock([0, 1]),
            )

    def test_wait_for_dms_times_out(self):
        client = RecordingClient([task_response("starting")])
        with self.assertRaises(TimeoutError):
            wait_for_status(
                "arn:task",
                "running",
                client,
                timeout_seconds=10,
                sleep=lambda seconds: None,
                clock=Clock([0, 10]),
            )

    def test_cdc_latency_selects_latest_points(self):
        older = datetime(2026, 9, 10, 12, 0, tzinfo=timezone.utc)
        newer = datetime(2026, 9, 10, 12, 1, tzinfo=timezone.utc)
        cloudwatch = RecordingClient(
            [
                {"Datapoints": [{"Timestamp": newer, "Maximum": 12}, {"Timestamp": older, "Maximum": 40}]},
                {"Datapoints": [{"Timestamp": newer, "Maximum": 8}]},
            ]
        )
        result = get_cdc_latency(
            "rep-1",
            "task-1",
            cloudwatch,
            checked_at=datetime(2026, 9, 10, 12, 2, tzinfo=timezone.utc),
        )
        self.assertEqual(result["source_seconds"], 12)
        self.assertEqual(result["target_seconds"], 8)

    def test_cutover_gate_requires_both_lag_metrics(self):
        dms = RecordingClient([task_response()])
        cloudwatch = RecordingClient(
            [
                {"Datapoints": [{"Timestamp": datetime.now(timezone.utc), "Maximum": 10}]},
                {"Datapoints": []},
            ]
        )
        ready, _ = is_cutover_ready("arn:task", "rep-1", "task-1", dms, cloudwatch)
        self.assertFalse(ready)

    def test_cutover_gate_accepts_healthy_task(self):
        now = datetime.now(timezone.utc)
        dms = RecordingClient([task_response()])
        cloudwatch = RecordingClient(
            [
                {"Datapoints": [{"Timestamp": now, "Maximum": 10}]},
                {"Datapoints": [{"Timestamp": now, "Maximum": 15}]},
            ]
        )
        ready, _ = is_cutover_ready("arn:task", "rep-1", "task-1", dms, cloudwatch)
        self.assertTrue(ready)

    def test_all_task_health_uses_paginator(self):
        client = PagedClient([task_response(), task_response("stopped", 1)])
        result = get_all_task_health(client)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[1]["tables_errored"], 1)

    def test_datasync_start_returns_execution_arn(self):
        client = RecordingClient([{"TaskExecutionArn": "arn:execution/1"}])
        self.assertEqual(start_task_execution("arn:task", client), "arn:execution/1")

    def test_datasync_status_uses_result_failures(self):
        client = RecordingClient(
            [
                {
                    "Status": "SUCCESS",
                    "FilesTransferred": 40,
                    "BytesTransferred": 1024,
                    "Result": {"FilesTransferFailed": 2, "PrepareDuration": 50},
                }
            ]
        )
        result = get_execution_status("arn:execution/1", client)
        self.assertEqual(result["files_failed"], 2)
        self.assertEqual(result["prepare_milliseconds"], 50)

    def test_datasync_wait_reaches_success(self):
        client = RecordingClient([{"Status": "LAUNCHING"}, {"Status": "SUCCESS"}])
        result = wait_for_execution(
            "arn:execution/1",
            client,
            sleep=lambda seconds: None,
            clock=Clock([0, 1]),
        )
        self.assertEqual(result["status"], "SUCCESS")

    def test_datasync_wait_times_out(self):
        client = RecordingClient([{"Status": "RUNNING"}])
        with self.assertRaises(TimeoutError):
            wait_for_execution(
                "arn:execution/1",
                client,
                timeout_seconds=10,
                sleep=lambda seconds: None,
                clock=Clock([0, 10]),
            )

    def test_throttle_converts_megabits_to_bytes(self):
        client = RecordingClient()
        result = set_task_throttle("arn:task", 500, client)
        self.assertEqual(result, 62_500_000)
        self.assertEqual(client.calls[0][1]["Options"]["BytesPerSecond"], 62_500_000)
        with self.assertRaises(ValueError):
            set_task_throttle("arn:task", -1, client)

    def test_throttle_handler_requires_known_mode(self):
        with patch.dict(os.environ, {"DATASYNC_TASK_ARN": "arn:task"}, clear=False):
            with patch("week10.fintrust_migration.s3.sync_helpers.set_task_throttle", return_value=1_125_000_000):
                result = throttle_handler({"mode": "overnight"}, None)
                self.assertEqual(result["bandwidth_mbps"], 9000)
            with self.assertRaises(ValueError):
                throttle_handler({"mode": "weekend"}, None)

    def test_nightly_monitor_tracks_multiple_executions(self):
        client = RecordingClient(
            [
                {"TaskExecutionArn": "arn:execution/1"},
                {"TaskExecutionArn": "arn:execution/2"},
                {"Status": "SUCCESS"},
                {"Status": "ERROR", "Result": {"FilesTransferFailed": 1}},
            ]
        )
        result = monitor_nightly_transfers(
            ["arn:task/1", "arn:task/2"],
            client,
            sleep=lambda seconds: None,
            clock=Clock([0]),
        )
        self.assertEqual(result["arn:execution/1"]["status"], "SUCCESS")
        self.assertEqual(result["arn:execution/2"]["status"], "ERROR")

    def test_orchestrator_rejects_unknown_action(self):
        with self.assertRaisesRegex(ValueError, "Unknown migration action"):
            orchestrator_handler({"action": "guess"}, None)

    def test_sql_submission_contains_assessed_views(self):
        sql = (ROOT / "week10" / "sql" / "migration_views.sql").read_text(encoding="utf-8")
        required = {
            "v_wave_progress",
            "v_customer_accounts",
            "v_monthly_txn_summary",
            "v_daily_transfer_volume",
            "v_volume_migration_progress",
        }
        for view in required:
            self.assertIn(f"CREATE OR REPLACE VIEW {view}", sql)
        self.assertIn("NULLIF(v.total_size_gb, 0)", sql)


if __name__ == "__main__":
    unittest.main()
