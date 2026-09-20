"""Lambda entry point for a scheduled FinTrust cost report."""

from __future__ import annotations

import os
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from week10.fintrust_migration.cost_reporting import (
    get_monthly_spend_by_service,
    upload_report_files,
    write_csv_report,
    write_html_report,
)


def lambda_handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    """Generate service spend reports and upload them to the configured bucket."""
    del context
    bucket = os.getenv("FINTRUST_COST_REPORT_BUCKET")
    if not bucket:
        raise RuntimeError("FINTRUST_COST_REPORT_BUCKET is required")
    months_back = int(event.get("months_back", 1))
    data = get_monthly_spend_by_service(months_back=months_back)
    with TemporaryDirectory() as directory:
        csv_path = write_csv_report(data, Path(directory) / "cost_report.csv")
        html_path = write_html_report(data, Path(directory) / "cost_report.html")
        keys = upload_report_files(bucket, csv_path, html_path)
    return {"statusCode": 200, "report_count": len(data), "keys": keys}
