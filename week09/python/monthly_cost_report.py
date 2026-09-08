"""Create a three month FinTrust cost report and optionally store it in S3."""

from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from typing import Any


def month_bounds(year: int, month: int) -> tuple[str, str]:
    """Return an inclusive start and exclusive end for one calendar month."""
    if not 1 <= month <= 12:
        raise ValueError("Month must be between 1 and 12")
    end_year, end_month = (year + 1, 1) if month == 12 else (year, month + 1)
    return f"{year:04d}-{month:02d}-01", f"{end_year:04d}-{end_month:02d}-01"


def previous_complete_months(reference_date: date, count: int = 3) -> list[tuple[int, int]]:
    """Return complete calendar months from oldest to newest."""
    if count < 1:
        raise ValueError("Count must be positive")
    year, month = reference_date.year, reference_date.month
    result = []
    for _ in range(count):
        month -= 1
        if month == 0:
            year -= 1
            month = 12
        result.append((year, month))
    return list(reversed(result))


def get_monthly_spend_by_service(client: Any, year: int, month: int) -> dict[str, Decimal]:
    """Return positive UnblendedCost totals grouped by service."""
    start, end = month_bounds(year, month)
    request = {
        "TimePeriod": {"Start": start, "End": end},
        "Granularity": "MONTHLY",
        "Metrics": ["UnblendedCost"],
        "GroupBy": [{"Type": "DIMENSION", "Key": "SERVICE"}],
    }
    totals: defaultdict[str, Decimal] = defaultdict(Decimal)
    while True:
        response = client.get_cost_and_usage(**request)
        for period in response.get("ResultsByTime", []):
            for group in period.get("Groups", []):
                service = group["Keys"][0]
                amount = Decimal(group["Metrics"]["UnblendedCost"]["Amount"])
                if amount > Decimal("0.01"):
                    totals[service] += amount
        token = response.get("NextPageToken")
        if not token:
            break
        request["NextPageToken"] = token
    return dict(sorted(totals.items(), key=lambda item: item[1], reverse=True))


class FinTrustMonthlyCostReport:
    """Query, format and store a compact organisation cost summary."""

    def __init__(self, cost_explorer_client: Any, s3_client: Any | None = None):
        self.cost_explorer = cost_explorer_client
        self.s3 = s3_client

    def collect(self, reference_date: date) -> tuple[list[tuple[int, int]], list[dict[str, Decimal]]]:
        periods = previous_complete_months(reference_date)
        spend = [
            get_monthly_spend_by_service(self.cost_explorer, year, month)
            for year, month in periods
        ]
        return periods, spend

    @staticmethod
    def render(
        periods: list[tuple[int, int]],
        spend: list[dict[str, Decimal]],
        top_count: int = 5,
    ) -> str:
        if len(periods) != 3 or len(spend) != 3:
            raise ValueError("The report requires exactly three monthly results")
        services = set().union(*(month.keys() for month in spend))
        ranked = sorted(
            services,
            key=lambda service: sum(month.get(service, Decimal(0)) for month in spend) / 3,
            reverse=True,
        )[:top_count]
        labels = [f"{year:04d}-{month:02d}" for year, month in periods]
        lines = [
            "FinTrust Monthly AWS Cost Report",
            "=" * 96,
            f"{'Service':36} {labels[0]:>13} {labels[1]:>13} {labels[2]:>13} {'Monthly change':>15}",
            "=" * 96,
        ]
        for service in ranked:
            values = [month.get(service, Decimal(0)) for month in spend]
            if values[1] == 0:
                change = "new" if values[2] else "0.0%"
            else:
                percent = (values[2] - values[1]) / values[1] * 100
                change = f"{percent:+.1f}%"
            lines.append(
                f"{service[:36]:36} "
                f"${values[0]:>12,.2f} ${values[1]:>12,.2f} ${values[2]:>12,.2f} {change:>15}"
            )
        totals = [sum(month.values(), Decimal(0)) for month in spend]
        lines.extend(
            [
                "=" * 96,
                f"{'All services':36} ${totals[0]:>12,.2f} ${totals[1]:>12,.2f} ${totals[2]:>12,.2f}",
            ]
        )
        return "\n".join(lines) + "\n"

    def upload(self, report: str, reference_date: date, bucket: str) -> str:
        if self.s3 is None:
            raise RuntimeError("An S3 client is required for upload")
        key = f"{reference_date:%Y-%m}/monthly_summary.txt"
        self.s3.put_object(
            Bucket=bucket,
            Key=key,
            Body=report.encode("utf-8"),
            ContentType="text/plain; charset=utf-8",
            ServerSideEncryption="AES256",
        )
        return f"s3://{bucket}/{key}"


def main() -> None:
    import boto3

    parser = argparse.ArgumentParser(description="Write the FinTrust monthly AWS cost report")
    parser.add_argument("--bucket", help="S3 bucket for the finished report")
    parser.add_argument("--as-of", type=date.fromisoformat, default=date.today())
    args = parser.parse_args()
    report_builder = FinTrustMonthlyCostReport(
        boto3.client("ce", region_name="us-east-1"),
        boto3.client("s3") if args.bucket else None,
    )
    periods, spend = report_builder.collect(args.as_of)
    report = report_builder.render(periods, spend)
    print(report)
    if args.bucket:
        print(f"Stored at {report_builder.upload(report, args.as_of, args.bucket)}")


if __name__ == "__main__":
    main()
