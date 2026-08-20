"""Enrich the SQL risk-score export with recent customer S3 activity."""

import argparse
import csv
import json
from datetime import datetime, timedelta, timezone
from decimal import Decimal


def load_risk_rows(csv_path):
    """Load and validate the columns exported by day5_risk_score.sql."""
    required = {"customer_id", "risk_score", "spike_flag"}
    with open(csv_path, encoding="utf-8", newline="") as source:
        rows = list(csv.DictReader(source))
    if not rows or not required.issubset(rows[0]):
        raise ValueError(f"Input CSV must contain: {', '.join(sorted(required))}")
    return rows


def has_recent_activity(s3_client, bucket, customer_id, cutoff):
    """Return True if the customer prefix contains an object newer than cutoff."""
    prefix = f"customers/{customer_id}/"
    paginator = s3_client.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for item in page.get("Contents", []):
            modified = item["LastModified"]
            if modified.tzinfo is None:
                modified = modified.replace(tzinfo=timezone.utc)
            if modified >= cutoff:
                return True
    return False


def enrich_rows(s3_client, bucket, rows, now=None):
    """Add the required seven-day activity flag to each risk row."""
    current_time = now or datetime.now(timezone.utc)
    cutoff = current_time - timedelta(days=7)
    enriched = []
    for row in rows:
        score = Decimal(row["risk_score"])
        if score < 0 or score > 1:
            raise ValueError(f"Risk score outside 0 to 1 for customer {row['customer_id']}")
        enriched.append(
            {
                "customer_id": int(row["customer_id"]),
                "risk_score": float(score),
                "spike_flag": int(row["spike_flag"]),
                "s3_activity_7d": has_recent_activity(
                    s3_client, bucket, row["customer_id"], cutoff
                ),
            }
        )
    return enriched


def upload_report(s3_client, bucket, rows, now=None):
    """Save the combined report to the protected audit prefix."""
    current_time = now or datetime.now(timezone.utc)
    key = f"fraud-risk/{current_time:%Y/%m/%d}/customer-risk.json"
    document = {
        "report_date": current_time.isoformat(),
        "customer_count": len(rows),
        "customers": rows,
    }
    s3_client.put_object(
        Bucket=bucket,
        Key=key,
        Body=json.dumps(document, indent=2),
        ContentType="application/json",
        ServerSideEncryption="aws:kms",
    )
    return f"s3://{bucket}/{key}"


def main():
    import boto3

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_csv", help="CSV exported from day5_risk_score.sql")
    parser.add_argument("--source-bucket", default="fintrust-transactions-prod")
    parser.add_argument("--report-bucket", required=True)
    args = parser.parse_args()

    s3_client = boto3.client("s3", region_name="af-south-1")
    rows = enrich_rows(
        s3_client,
        args.source_bucket,
        load_risk_rows(args.input_csv),
    )
    print(upload_report(s3_client, args.report_bucket, rows))


if __name__ == "__main__":
    main()
