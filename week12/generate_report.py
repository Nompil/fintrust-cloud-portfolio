"""Generate local FinTrust cost reports from Cost Explorer data.

Run only from an authorised AWS billing or delegated billing account. The script
does not contain credentials and uses the normal boto3 credential chain.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from week10.fintrust_migration.cost_reporting import (
    get_monthly_spend_by_service,
    get_per_account_spend,
    upload_report_files,
    write_csv_report,
    write_html_report,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate FinTrust Cost Explorer reports.")
    parser.add_argument("--months-back", type=int, default=1, help="Number of calendar months to include.")
    parser.add_argument("--output-dir", type=Path, default=Path("reports"), help="Local report directory.")
    parser.add_argument("--per-account", action="store_true", help="Include linked account and service grouping.")
    parser.add_argument("--upload-bucket", help="Optional bucket for CSV and HTML uploads.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    data = get_per_account_spend(args.months_back) if args.per_account else get_monthly_spend_by_service(args.months_back)
    csv_path = write_csv_report(data, args.output_dir / "cost_report.csv")
    html_path = write_html_report(data, args.output_dir / "cost_report.html")
    print(f"Created {csv_path} and {html_path}.")
    if args.upload_bucket:
        keys = upload_report_files(args.upload_bucket, csv_path, html_path)
        print("Uploaded " + ", ".join(keys))


if __name__ == "__main__":
    main()
