from __future__ import annotations

import json
import unittest
from datetime import date, datetime, timezone
from decimal import Decimal

from week09.python.budget_controls import create_monthly_budget, describe_budget_usage
from week09.python.dms_monitor import get_table_statistics, get_task_progress, task_health
from week09.python.fis_experiments import summarise_fis_experiments
from week09.python.monthly_cost_report import (
    FinTrustMonthlyCostReport,
    get_monthly_spend_by_service,
    month_bounds,
    previous_complete_months,
)
from week09.python.pricing_and_tco import (
    calculate_savings_plan_savings,
    get_ec2_ondemand_price,
    tco_break_even,
)
from week09.python.snow_transfer_planner import plan_snow_transfer
from week09.python.tag_governance import (
    apply_environment_tag,
    audit_tag_compliance,
    governance_summary,
    list_portfolios,
    write_governance_report,
)


class RecordingClient:
    def __init__(self, responses=None):
        self.responses = list(responses or [])
        self.calls = []

    def __getattr__(self, name):
        def operation(**kwargs):
            self.calls.append((name, kwargs))
            if self.responses:
                return self.responses.pop(0)
            return {}

        return operation


class FakePaginator:
    def __init__(self, pages):
        self.pages = pages
        self.requests = []

    def paginate(self, **kwargs):
        self.requests.append(kwargs)
        yield from self.pages


class FakeTaggingClient(RecordingClient):
    def __init__(self, pages):
        super().__init__()
        self.paginator = FakePaginator(pages)

    def get_paginator(self, operation):
        self.calls.append(("get_paginator", {"operation": operation}))
        return self.paginator


def price_item(price):
    return json.dumps(
        {
            "terms": {
                "OnDemand": {
                    "term": {
                        "priceDimensions": {
                            "dimension": {"pricePerUnit": {"USD": str(price)}}
                        }
                    }
                }
            }
        }
    )


def cost_group(service, amount):
    return {
        "Keys": [service],
        "Metrics": {"UnblendedCost": {"Amount": str(amount), "Unit": "USD"}},
    }


class WeekNineTests(unittest.TestCase):
    def test_pricing_query_uses_global_endpoint_filters(self):
        client = RecordingClient([{"PriceList": [price_item("0.3120")]}])
        price = get_ec2_ondemand_price(client, "m5.xlarge", "af-south-1")
        self.assertEqual(price, Decimal("0.3120"))
        _, request = client.calls[0]
        filters = {item["Field"]: item["Value"] for item in request["Filters"]}
        self.assertEqual(filters["location"], "Africa (Cape Town)")
        self.assertEqual(filters["tenancy"], "Shared")

    def test_pricing_query_handles_unavailable_instance(self):
        client = RecordingClient([{"PriceList": []}])
        self.assertIsNone(get_ec2_ondemand_price(client, "missing.type"))

    def test_savings_plan_calculation_is_traceable(self):
        result = calculate_savings_plan_savings("32.47")
        self.assertEqual(result.ondemand_capacity_per_hour, Decimal("95.50"))
        self.assertEqual(result.total_commitment_cost, Decimal("853311.60"))
        self.assertEqual(result.total_saving, Decimal("1656428.40"))

    def test_unused_savings_plan_can_cost_more(self):
        result = calculate_savings_plan_savings("32.47", utilisation_percent="20")
        self.assertLess(result.total_saving, 0)

    def test_tco_break_even_and_yearly_rows(self):
        month, rows = tco_break_even("4200000", "248000", "850000")
        self.assertEqual(month, 9)
        self.assertEqual([row.month for row in rows], [12, 24, 36, 48, 60])

    def test_month_bounds_handle_december(self):
        self.assertEqual(month_bounds(2026, 12), ("2026-12-01", "2027-01-01"))

    def test_previous_months_cross_year_boundary(self):
        self.assertEqual(
            previous_complete_months(date(2026, 2, 12)),
            [(2025, 11), (2025, 12), (2026, 1)],
        )

    def test_cost_query_combines_pages(self):
        client = RecordingClient(
            [
                {
                    "ResultsByTime": [{"Groups": [cost_group("Amazon EC2", "40.25")]}],
                    "NextPageToken": "next",
                },
                {
                    "ResultsByTime": [
                        {"Groups": [cost_group("Amazon S3", "12.50"), cost_group("Tiny", "0.001")]}
                    ]
                },
            ]
        )
        spend = get_monthly_spend_by_service(client, 2026, 8)
        self.assertEqual(spend, {"Amazon EC2": Decimal("40.25"), "Amazon S3": Decimal("12.50")})
        self.assertEqual(client.calls[1][1]["NextPageToken"], "next")

    def test_monthly_report_ranks_and_calculates_change(self):
        periods = [(2026, 6), (2026, 7), (2026, 8)]
        spend = [
            {"Amazon EC2": Decimal("100"), "Amazon S3": Decimal("20")},
            {"Amazon EC2": Decimal("120"), "Amazon S3": Decimal("20")},
            {"Amazon EC2": Decimal("150"), "Amazon S3": Decimal("10")},
        ]
        report = FinTrustMonthlyCostReport.render(periods, spend)
        self.assertIn("Amazon EC2", report)
        self.assertIn("+25.0%", report)
        self.assertIn("All services", report)

    def test_monthly_report_upload_is_encrypted(self):
        s3 = RecordingClient()
        report = FinTrustMonthlyCostReport(RecordingClient(), s3)
        uri = report.upload("result", date(2026, 9, 8), "fintrust-cost-reports")
        self.assertEqual(uri, "s3://fintrust-cost-reports/2026-09/monthly_summary.txt")
        _, request = s3.calls[0]
        self.assertEqual(request["ServerSideEncryption"], "AES256")
        self.assertEqual(request["Body"], b"result")

    def test_budget_request_has_staged_notifications(self):
        budgets = RecordingClient()
        create_monthly_budget(
            budgets,
            "111122223333",
            "FinTrust-Analytics-Monthly",
            "15000",
            "owner@example.invalid",
        )
        _, request = budgets.calls[0]
        notifications = request["NotificationsWithSubscribers"]
        self.assertEqual([item["Notification"]["Threshold"] for item in notifications], [80.0, 90.0, 100.0])
        self.assertEqual(notifications[-1]["Notification"]["NotificationType"], "FORECASTED")

    def test_budget_usage_supports_pagination(self):
        budgets = RecordingClient(
            [
                {
                    "Budgets": [
                        {
                            "BudgetName": "Analytics",
                            "BudgetLimit": {"Amount": "1000"},
                            "CalculatedSpend": {"ActualSpend": {"Amount": "825"}},
                        }
                    ],
                    "NextToken": "page2",
                },
                {"Budgets": []},
            ]
        )
        result = describe_budget_usage(budgets, "111122223333")
        self.assertEqual(result[0]["used_percent"], Decimal("82.5"))
        self.assertEqual(budgets.calls[1][1]["NextToken"], "page2")

    def test_tag_audit_checks_missing_and_invalid_values(self):
        client = FakeTaggingClient(
            [
                {
                    "ResourceTagMappingList": [
                        {
                            "ResourceARN": "arn:aws:ec2:af-south-1:1111:instance/i-1",
                            "Tags": [
                                {"Key": "CostCentre", "Value": "Analytics"},
                                {"Key": "Team", "Value": "DataEngineering"},
                                {"Key": "Environment", "Value": "Production"},
                            ],
                        },
                        {
                            "ResourceARN": "arn:aws:lambda:af-south-1:1111:function:f",
                            "Tags": [
                                {"Key": "Team", "Value": "UnknownTeam"},
                                {"Key": "Environment", "Value": "Dev"},
                            ],
                        },
                    ]
                }
            ]
        )
        audit = audit_tag_compliance(client)
        self.assertEqual(audit.total_scanned, 2)
        self.assertEqual(audit.compliant, 1)
        self.assertEqual(audit.violations[0].missing, ("CostCentre",))
        self.assertEqual(audit.violations[0].invalid, ("Team",))
        self.assertEqual(governance_summary(audit)["violations_by_service"], {"lambda": 1})

    def test_governance_report_writes_json(self):
        audit = audit_tag_compliance(FakeTaggingClient([{"ResourceTagMappingList": []}]))
        s3 = RecordingClient()
        uri = write_governance_report(s3, "fintrust-governance", audit, date(2026, 9, 8))
        self.assertEqual(uri, "s3://fintrust-governance/tag-audit/2026-09-08.json")
        body = json.loads(s3.calls[0][1]["Body"])
        self.assertEqual(body["total_scanned"], 0)

    def test_tag_change_requires_approval(self):
        client = RecordingClient()
        with self.assertRaises(PermissionError):
            apply_environment_tag(client, ["arn:example"], "Production")
        apply_environment_tag(client, ["arn:example"], "Dev", approved=True)
        self.assertEqual(client.calls[0][1]["Tags"], {"Environment": "Dev"})

    def test_service_catalog_combines_owned_and_shared(self):
        client = RecordingClient(
            [
                {"PortfolioDetails": [{"Id": "port-a", "DisplayName": "DataPlatform"}]},
                {"PortfolioDetails": [{"Id": "port-b", "DisplayName": "InfraOps"}]},
                {
                    "ProductViewDetails": [
                        {"ProductViewSummary": {"Name": "Data Lake", "Owner": "Platform", "Type": "CLOUD_FORMATION_TEMPLATE"}}
                    ]
                },
                {"ProductViewDetails": []},
            ]
        )
        portfolios = list_portfolios(client)
        self.assertEqual([item["display_name"] for item in portfolios], ["DataPlatform", "InfraOps"])
        self.assertEqual(portfolios[0]["products"][0]["name"], "Data Lake")

    def test_dms_progress_reads_terminal_state(self):
        dms = RecordingClient(
            [
                {
                    "ReplicationTasks": [
                        {
                            "ReplicationTaskIdentifier": "oracle-to-aurora",
                            "Status": "stopped",
                            "ReplicationTaskStartDate": datetime(2026, 9, 3, tzinfo=timezone.utc),
                            "ReplicationTaskStats": {"TablesLoaded": 12, "ElapsedTimeMillis": 6500},
                        }
                    ]
                }
            ]
        )
        progress = get_task_progress(dms, "arn:task")
        self.assertTrue(progress.terminal)
        self.assertEqual(progress.elapsed_seconds, 6)

    def test_dms_table_statistics_are_paginated(self):
        dms = RecordingClient(
            [
                {"TableStatistics": [{"TableName": "accounts"}], "Marker": "next"},
                {"TableStatistics": [{"TableName": "transactions"}]},
            ]
        )
        rows = get_table_statistics(dms, "arn:task")
        self.assertEqual([row["TableName"] for row in rows], ["accounts", "transactions"])
        self.assertEqual(dms.calls[1][1]["Marker"], "next")

    def test_dms_health_flags_validation_errors(self):
        dms = RecordingClient(
            [
                {
                    "ReplicationTasks": [
                        {
                            "ReplicationTaskIdentifier": "task",
                            "Status": "running",
                            "ReplicationTaskStats": {},
                        }
                    ]
                },
                {"TableStatistics": [{"TableName": "accounts", "ValidationFailedRecords": 2}]},
            ]
        )
        result = task_health(dms, "arn:task")
        self.assertTrue(result["alert"])
        self.assertEqual(result["validation_failed_records"], 2)

    def test_snow_plan_matches_archive_requirement(self):
        plan = plan_snow_transfer(3000, "archive", 1)
        self.assertEqual(plan.device, "Snowball Edge Storage Optimised")
        self.assertEqual(plan.count, 38)
        self.assertEqual(plan.total_capacity_tb, 3040)
        self.assertEqual(plan.spare_capacity_tb, 40)
        self.assertEqual(plan.internet_days, 277.8)

    def test_snow_planner_selects_edge_compute(self):
        plan = plan_snow_transfer(100, "edge-compute")
        self.assertEqual(plan.device, "Snowball Edge Compute Optimised")
        self.assertEqual(plan.count, 4)

    def test_fis_summary_reads_full_detail(self):
        client = RecordingClient(
            [
                {"experiments": [{"id": "EXP-1234567890ABCDEF"}]},
                {
                    "experiment": {
                        "experimentTemplateId": "EXT-1",
                        "state": {"status": "completed"},
                        "startTime": datetime(2026, 9, 3, 14, 30),
                        "stopConditions": [{"value": "aws:cloudwatch:alarm:payment-errors"}],
                    }
                },
            ]
        )
        result = summarise_fis_experiments(client)
        self.assertEqual(result[0]["state"], "completed")
        self.assertEqual(result[0]["experiment_id"], "1234567890ABCDEF")
        self.assertIn("payment-errors", result[0]["stop_condition"])


if __name__ == "__main__":
    unittest.main()
