"""DMS lifecycle and cutover checks for FinTrust database migrations."""

from __future__ import annotations

import time
from datetime import datetime, timedelta, timezone
from typing import Any, Callable

from ..utils.sessions import get_client


FAILURE_STATES = {"failed", "error"}


def get_task_status(task_arn: str, dms_client: Any | None = None) -> dict[str, Any]:
    """Read one DMS task and raise when the ARN cannot be found."""
    client = dms_client or get_client("dms")
    response = client.describe_replication_tasks(
        Filters=[{"Name": "replication-task-arn", "Values": [task_arn]}]
    )
    tasks = response.get("ReplicationTasks", [])
    if not tasks:
        raise ValueError(f"Task not found: {task_arn}")
    task = tasks[0]
    return {
        "arn": task["ReplicationTaskArn"],
        "identifier": task["ReplicationTaskIdentifier"],
        "status": task["Status"],
        "stats": task.get("ReplicationTaskStats", {}),
        "stop_reason": task.get("StopReason"),
    }


def wait_for_status(
    task_arn: str,
    target_status: str,
    dms_client: Any | None = None,
    timeout_seconds: int = 1800,
    poll_seconds: int = 30,
    sleep: Callable[[float], None] = time.sleep,
    clock: Callable[[], float] = time.monotonic,
) -> dict[str, Any]:
    """Wait for a task status with failure and timeout handling."""
    client = dms_client or get_client("dms")
    started = clock()
    while True:
        info = get_task_status(task_arn, client)
        if info["status"] == target_status:
            return info
        if info["status"] in FAILURE_STATES:
            reason = info.get("stop_reason") or "No stop reason returned"
            raise RuntimeError(f"DMS task failed: {reason}")
        if clock() - started >= timeout_seconds:
            raise TimeoutError(f"DMS task did not reach {target_status} within {timeout_seconds} seconds")
        sleep(poll_seconds)


def start_task(
    task_arn: str,
    start_type: str = "resume-processing",
    dms_client: Any | None = None,
    allow_full_restart: bool = False,
    wait: bool = True,
) -> dict[str, Any]:
    """Start or resume DMS while guarding destructive full restarts."""
    valid = {"start-replication", "resume-processing", "reload-target"}
    if start_type not in valid:
        raise ValueError(f"Unsupported DMS start type: {start_type}")
    if start_type == "start-replication" and not allow_full_restart:
        raise PermissionError("A full replication restart requires explicit approval")
    client = dms_client or get_client("dms")
    response = client.start_replication_task(
        ReplicationTaskArn=task_arn,
        StartReplicationTaskType=start_type,
    )
    if not wait:
        return response["ReplicationTask"]
    return wait_for_status(task_arn, "running", client)


def stop_task(
    task_arn: str,
    dms_client: Any | None = None,
    wait: bool = True,
) -> dict[str, Any]:
    """Stop a DMS task and optionally wait for the stopped state."""
    client = dms_client or get_client("dms")
    response = client.stop_replication_task(ReplicationTaskArn=task_arn)
    if not wait:
        return response["ReplicationTask"]
    return wait_for_status(task_arn, "stopped", client)


def get_cdc_latency(
    replication_instance_id: str,
    task_identifier: str,
    cloudwatch_client: Any | None = None,
    lookback_minutes: int = 5,
    checked_at: datetime | None = None,
) -> dict[str, Any]:
    """Read the latest source and target DMS latency points."""
    client = cloudwatch_client or get_client("cloudwatch")
    now = checked_at or datetime.now(timezone.utc)

    def metric(name: str) -> float | None:
        response = client.get_metric_statistics(
            Namespace="AWS/DMS",
            MetricName=name,
            Dimensions=[
                {"Name": "ReplicationInstanceIdentifier", "Value": replication_instance_id},
                {"Name": "ReplicationTaskIdentifier", "Value": task_identifier},
            ],
            StartTime=now - timedelta(minutes=lookback_minutes),
            EndTime=now,
            Period=60,
            Statistics=["Maximum"],
        )
        points = response.get("Datapoints", [])
        if not points:
            return None
        return max(points, key=lambda point: point["Timestamp"])["Maximum"]

    return {
        "source_seconds": metric("CDCLatencySource"),
        "target_seconds": metric("CDCLatencyTarget"),
        "checked_at": now.isoformat(),
    }


def is_cutover_ready(
    task_arn: str,
    replication_instance_id: str,
    task_identifier: str,
    dms_client: Any | None = None,
    cloudwatch_client: Any | None = None,
    maximum_lag_seconds: float = 30,
) -> tuple[bool, dict[str, Any]]:
    """Require a running task, low source and target lag, and no table errors."""
    status = get_task_status(task_arn, dms_client)
    latency = get_cdc_latency(replication_instance_id, task_identifier, cloudwatch_client)
    values = (latency["source_seconds"], latency["target_seconds"])
    ready = (
        status["status"] == "running"
        and status["stats"].get("TablesErrored", 0) == 0
        and all(value is not None and value <= maximum_lag_seconds for value in values)
    )
    return ready, {"task": status, "latency": latency, "maximum_lag_seconds": maximum_lag_seconds}


def get_all_task_health(
    dms_client: Any | None = None,
) -> list[dict[str, Any]]:
    """Read all task summaries using the DMS paginator."""
    client = dms_client or get_client("dms")
    tasks = []
    paginator = client.get_paginator("describe_replication_tasks")
    for page in paginator.paginate():
        for task in page.get("ReplicationTasks", []):
            stats = task.get("ReplicationTaskStats", {})
            tasks.append(
                {
                    "identifier": task["ReplicationTaskIdentifier"],
                    "status": task["Status"],
                    "tables_loaded": stats.get("TablesLoaded", 0),
                    "tables_errored": stats.get("TablesErrored", 0),
                }
            )
    return tasks
