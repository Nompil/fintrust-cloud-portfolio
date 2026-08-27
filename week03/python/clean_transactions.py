"""Clean the FinTrust transaction CSV and create a JSON summary."""

import csv
import json
from datetime import datetime
from pathlib import Path


DATA_DIR = Path(__file__).parent / "data"
RAW_INPUT = DATA_DIR / "raw_transactions.csv"
CLEAN_CSV = DATA_DIR / "clean_transactions.csv"
SUMMARY_JSON = DATA_DIR / "daily_summary.json"


def normalise_date(value):
    """Return a supported date in ISO format."""
    for date_format in ("%Y-%m-%d", "%d/%m/%y", "%d/%m/%Y"):
        try:
            return datetime.strptime(value.strip(), date_format).strftime("%Y-%m-%d")
        except ValueError:
            continue
    raise ValueError(f"unrecognised date format: {value!r}")


def clean_transaction(row):
    """Convert one raw CSV row into the clean output shape."""
    return {
        "transaction_id": int(row["TxID"].strip()),
        "account_id": int(row["AcctID"].strip()),
        "type": row["TYPE"].strip().lower(),
        "amount": float(row["Amount"].strip()),
        "date": normalise_date(row["Date"]),
        "description": row.get("Desc", "").strip() or "No description",
    }


def build_summary(transactions):
    """Calculate the transaction counts and Rand totals."""
    deposits = [item for item in transactions if item["type"] == "deposit"]
    withdrawals = [item for item in transactions if item["type"] == "withdrawal"]
    return {
        "total_transactions": len(transactions),
        "total_deposits": len(deposits),
        "total_withdrawals": len(withdrawals),
        "sum_deposits": round(sum(item["amount"] for item in deposits), 2),
        "sum_withdrawals": round(sum(item["amount"] for item in withdrawals), 2),
    }


def main():
    transactions = []

    with RAW_INPUT.open("r", newline="", encoding="utf-8") as input_file:
        reader = csv.DictReader(input_file)
        for row_number, row in enumerate(reader, start=2):
            try:
                transactions.append(clean_transaction(row))
            except (KeyError, ValueError) as error:
                print(f"Skipped row {row_number}: {error}")

    CLEAN_CSV.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "transaction_id",
        "account_id",
        "type",
        "amount",
        "date",
        "description",
    ]
    with CLEAN_CSV.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(transactions)

    summary = build_summary(transactions)
    with SUMMARY_JSON.open("w", encoding="utf-8") as summary_file:
        json.dump(summary, summary_file, indent=2)

    print(f"Clean CSV: {CLEAN_CSV.name} ({len(transactions)} rows)")
    print(f"Summary JSON: {SUMMARY_JSON.name}")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
