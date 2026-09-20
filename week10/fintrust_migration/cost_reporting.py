"""Cost Explorer reporting helpers added during Week 12.

Clients are supplied by the caller or created lazily through the existing session
factory. Importing this module does not contact AWS.
"""

from __future__ import annotations

import csv
from datetime import date, timedelta
from html import escape
from pathlib import Path
from typing import Any, Iterable

from .utils.sessions import get_client


COST_EXPLORER_REGION = "us-east-1"
REPORT_FIELDS = ["period", "service", "cost_usd"]
ACCOUNT_REPORT_FIELDS = ["period", "account_id", "account_name", "service", "cost_usd"]


def _report_period(months_back: int, today: date | None = None) -> dict[str, str]:
    """Return a Cost Explorer time period that starts on a calendar month boundary."""
    if months_back < 1:
        raise ValueError("months_back must be at least 1")
    current = today or date.today()
    first_of_current_month = current.replace(day=1)
    start_candidate = first_of_current_month - timedelta(days=1)
    for _ in range(months_back - 1):
        start_candidate = start_candidate.replace(day=1) - timedelta(days=1)
    start = start_candidate.replace(day=1)
    return {"Start": start.isoformat(), "End": current.isoformat()}


def _cost_rows(response: dict[str, Any], account_names: dict[str, str] | None = None) -> list[dict[str, Any]]:
    """Flatten Cost Explorer groups into report rows."""
    rows: list[dict[str, Any]] = []
    for period in response.get("ResultsByTime", []):
        period_start = period.get("TimePeriod", {}).get("Start", "")
        for group in period.get("Groups", []):
            keys = group.get("Keys", [])
            amount = float(group.get("Metrics", {}).get("UnblendedCost", {}).get("Amount", 0))
            if account_names is None:
                service = keys[0] if keys else "Unclassified"
                rows.append({"period": period_start, "service": service, "cost_usd": amount})
            else:
                account_id = keys[0] if keys else "Unknown"
                service = keys[1] if len(keys) > 1 else "Unclassified"
                rows.append(
                    {
                        "period": period_start,
                        "account_id": account_id,
                        "account_name": account_names.get(account_id, "Unknown account"),
                        "service": service,
                        "cost_usd": amount,
                    }
                )
    return rows


def get_monthly_spend_by_service(
    months_back: int = 1,
    cost_explorer_client: Any | None = None,
    today: date | None = None,
) -> list[dict[str, Any]]:
    """Return monthly unblended spend grouped by AWS service.

    Cost Explorer is a global billing endpoint and must use the `us-east-1` client
    region even when the workload runs in another AWS Region.
    """
    client = cost_explorer_client or get_client("ce", region=COST_EXPLORER_REGION)
    response = client.get_cost_and_usage(
        TimePeriod=_report_period(months_back, today),
        Granularity="MONTHLY",
        Metrics=["UnblendedCost"],
        GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}],
    )
    return _cost_rows(response)


def _account_name_map(organizations_client: Any) -> dict[str, str]:
    """Get account names from Organizations, using a paginator when available."""
    accounts: list[dict[str, str]] = []
    if hasattr(organizations_client, "get_paginator"):
        paginator = organizations_client.get_paginator("list_accounts")
        for page in paginator.paginate():
            accounts.extend(page.get("Accounts", []))
    else:
        response = organizations_client.list_accounts()
        accounts.extend(response.get("Accounts", []))
    return {account["Id"]: account["Name"] for account in accounts}


def get_per_account_spend(
    months_back: int = 1,
    cost_explorer_client: Any | None = None,
    organizations_client: Any | None = None,
    today: date | None = None,
) -> list[dict[str, Any]]:
    """Return consolidated billing spend joined to member-account names."""
    cost_client = cost_explorer_client or get_client("ce", region=COST_EXPLORER_REGION)
    organization_client = organizations_client or get_client("organizations", region=COST_EXPLORER_REGION)
    response = cost_client.get_cost_and_usage(
        TimePeriod=_report_period(months_back, today),
        Granularity="MONTHLY",
        Metrics=["UnblendedCost", "UsageQuantity"],
        GroupBy=[
            {"Type": "DIMENSION", "Key": "LINKED_ACCOUNT"},
            {"Type": "DIMENSION", "Key": "SERVICE"},
        ],
    )
    return _cost_rows(response, _account_name_map(organization_client))


def write_csv_report(data: Iterable[dict[str, Any]], output_path: str | Path = "cost_report.csv") -> Path:
    """Write service or account report rows as UTF-8 CSV and return the path."""
    rows = list(data)
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = ACCOUNT_REPORT_FIELDS if any("account_id" in row for row in rows) else REPORT_FIELDS
    with path.open("w", newline="", encoding="utf-8") as report_file:
        writer = csv.DictWriter(report_file, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    return path


def write_html_report(data: Iterable[dict[str, Any]], output_path: str | Path = "cost_report.html") -> Path:
    """Write an escaped, sorted HTML table and return the output path."""
    rows = sorted(data, key=lambda row: float(row.get("cost_usd", 0)), reverse=True)
    account_report = any("account_id" in row for row in rows)
    headings = ACCOUNT_REPORT_FIELDS if account_report else REPORT_FIELDS
    body_rows = []
    for row in rows:
        values = []
        for heading in headings:
            value = f"{float(row[heading]):.2f}" if heading == "cost_usd" else str(row.get(heading, ""))
            values.append(f"<td>{escape(value)}</td>")
        body_rows.append("<tr>" + "".join(values) + "</tr>")
    header = "".join(f"<th>{escape(heading.replace('_', ' ').title())}</th>" for heading in headings)
    html = """<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>FinTrust Cost Report</title></head>
<body><h1>FinTrust Cost Report</h1><table border="1"><thead><tr>""" + header + "</tr></thead><tbody>" + "".join(body_rows) + "</tbody></table></body></html>"
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    return path


def upload_report_files(
    bucket: str,
    csv_path: str | Path,
    html_path: str | Path,
    report_date: date | None = None,
    s3_client: Any | None = None,
) -> list[str]:
    """Upload report files to the agreed date-based S3 prefix and return their keys."""
    if not bucket:
        raise ValueError("bucket is required")
    report_day = report_date or date.today()
    prefix = f"cost-reports/{report_day.year}/{report_day.month:02d}"
    client = s3_client or get_client("s3")
    paths = [Path(csv_path), Path(html_path)]
    keys = [f"{prefix}/{path.name}" for path in paths]
    for path, key in zip(paths, keys, strict=True):
        client.upload_file(str(path), bucket, key)
    return keys
