from __future__ import annotations

import csv
import os
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch

from week10.fintrust_migration import __all__ as package_exports
from week10.fintrust_migration.cost_reporting import (
    _report_period,
    get_monthly_spend_by_service,
    get_per_account_spend,
    upload_report_files,
    write_csv_report,
    write_html_report,
)
from week12.scheduled_cost_report import lambda_handler


ROOT = Path(__file__).resolve().parents[2]


class CostExplorerClient:
    def __init__(self, response):
        self.response = response
        self.requests = []

    def get_cost_and_usage(self, **kwargs):
        self.requests.append(kwargs)
        return self.response


class OrganizationsClient:
    def list_accounts(self):
        return {
            "Accounts": [
                {"Id": "account-one", "Name": "FinTrust Production"},
                {"Id": "account-two", "Name": "FinTrust Sandbox"},
            ]
        }


class S3Client:
    def __init__(self):
        self.uploads = []

    def upload_file(self, filename, bucket, key):
        self.uploads.append((filename, bucket, key))


SERVICE_RESPONSE = {
    "ResultsByTime": [
        {
            "TimePeriod": {"Start": "2026-08-01"},
            "Groups": [
                {"Keys": ["Amazon EC2"], "Metrics": {"UnblendedCost": {"Amount": "18.50"}}},
                {"Keys": ["Amazon S3"], "Metrics": {"UnblendedCost": {"Amount": "2.25"}}},
            ],
        }
    ]
}


ACCOUNT_RESPONSE = {
    "ResultsByTime": [
        {
            "TimePeriod": {"Start": "2026-08-01"},
            "Groups": [
                {
                    "Keys": ["account-one", "Amazon EC2"],
                    "Metrics": {"UnblendedCost": {"Amount": "18.50"}},
                }
            ],
        }
    ]
}


class WeekTwelveTests(unittest.TestCase):
    def test_report_period_starts_on_month_boundary(self):
        period = _report_period(2, date(2026, 9, 20))
        self.assertEqual(period, {"Start": "2026-07-01", "End": "2026-09-20"})

    def test_report_period_rejects_zero_months(self):
        with self.assertRaises(ValueError):
            _report_period(0, date(2026, 9, 20))

    def test_service_report_uses_cost_explorer_shape(self):
        client = CostExplorerClient(SERVICE_RESPONSE)
        rows = get_monthly_spend_by_service(1, client, date(2026, 9, 20))
        self.assertEqual(rows[0], {"period": "2026-08-01", "service": "Amazon EC2", "cost_usd": 18.5})
        self.assertEqual(client.requests[0]["GroupBy"][0]["Key"], "SERVICE")
        self.assertEqual(client.requests[0]["TimePeriod"]["Start"], "2026-08-01")

    def test_account_report_joins_organization_names(self):
        rows = get_per_account_spend(
            1,
            CostExplorerClient(ACCOUNT_RESPONSE),
            OrganizationsClient(),
            date(2026, 9, 20),
        )
        self.assertEqual(rows[0]["account_name"], "FinTrust Production")
        self.assertEqual(rows[0]["service"], "Amazon EC2")

    def test_csv_report_writes_expected_fields(self):
        with tempfile.TemporaryDirectory() as directory:
            path = write_csv_report(
                [{"period": "2026-08-01", "service": "Amazon S3", "cost_usd": 2.25}],
                Path(directory) / "report.csv",
            )
            with path.open(encoding="utf-8") as report_file:
                reader = csv.reader(report_file)
                self.assertEqual(next(reader), ["period", "service", "cost_usd"])
                self.assertEqual(next(reader), ["2026-08-01", "Amazon S3", "2.25"])

    def test_html_report_escapes_service_content(self):
        with tempfile.TemporaryDirectory() as directory:
            path = write_html_report(
                [{"period": "2026-08-01", "service": "<unsafe>", "cost_usd": 2.5}],
                Path(directory) / "report.html",
            )
            content = path.read_text(encoding="utf-8")
        self.assertIn("&lt;unsafe&gt;", content)
        self.assertNotIn("<td><unsafe></td>", content)

    def test_upload_uses_monthly_cost_report_prefix(self):
        s3 = S3Client()
        keys = upload_report_files(
            "fintrust-reports",
            "cost_report.csv",
            "cost_report.html",
            date(2026, 9, 20),
            s3,
        )
        self.assertEqual(keys, [
            "cost-reports/2026/09/cost_report.csv",
            "cost-reports/2026/09/cost_report.html",
        ])
        self.assertEqual(s3.uploads[0][1], "fintrust-reports")

    def test_upload_requires_bucket_name(self):
        with self.assertRaises(ValueError):
            upload_report_files("", "report.csv", "report.html", s3_client=S3Client())

    def test_scheduled_handler_requires_configured_bucket(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(RuntimeError, "FINTRUST_COST_REPORT_BUCKET"):
                lambda_handler({}, None)

    def test_scheduled_handler_returns_uploaded_keys(self):
        with patch.dict(os.environ, {"FINTRUST_COST_REPORT_BUCKET": "fintrust-reports"}, clear=True):
            with patch("week12.scheduled_cost_report.get_monthly_spend_by_service", return_value=[{"service": "S3"}]), \
                 patch("week12.scheduled_cost_report.write_csv_report", return_value=Path("report.csv")), \
                 patch("week12.scheduled_cost_report.write_html_report", return_value=Path("report.html")), \
                 patch("week12.scheduled_cost_report.upload_report_files", return_value=["cost-reports/2026/09/report.csv"]):
                result = lambda_handler({"months_back": 2}, None)
        self.assertEqual(result["statusCode"], 200)
        self.assertEqual(result["report_count"], 1)

    def test_package_exports_cost_reporting_functions(self):
        self.assertIn("get_monthly_spend_by_service", package_exports)
        self.assertIn("get_per_account_spend", package_exports)
        self.assertIn("write_csv_report", package_exports)

    def test_sql_contains_targeted_index_and_explain_plan(self):
        sql = (ROOT / "week12" / "sql" / "fintrust_views.sql").read_text(encoding="utf-8")
        self.assertIn("CREATE INDEX CONCURRENTLY IF NOT EXISTS", sql)
        self.assertIn("WHERE status IN ('PENDING', 'PROCESSING')", sql)
        self.assertIn("EXPLAIN (ANALYZE, BUFFERS)", sql)

    def test_schedule_uses_first_monday_at_eight_sast(self):
        template = (ROOT / "week12" / "infrastructure" / "cost-report-schedule.yaml").read_text(encoding="utf-8")
        self.assertIn("cron(0 6 ? * 2#1 *)", template)
        self.assertIn("AWS::Lambda::Permission", template)

    def test_scp_examples_contain_only_guardrail_denies(self):
        region_scp = (ROOT / "week12" / "policies" / "approved-regions.json").read_text(encoding="utf-8")
        audit_scp = (ROOT / "week12" / "policies" / "protect-audit-controls.json").read_text(encoding="utf-8")
        self.assertIn('"Effect": "Deny"', region_scp)
        self.assertIn('"aws:RequestedRegion"', region_scp)
        self.assertIn('"cloudtrail:StopLogging"', audit_scp)


if __name__ == "__main__":
    unittest.main()
