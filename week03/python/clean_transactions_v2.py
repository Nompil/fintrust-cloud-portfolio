#!/usr/bin/env python3
"""Clean FinTrust transaction data and write a daily summary."""

import csv
import json
import logging
from datetime import datetime
from pathlib import Path

LOG_DIR = Path(__file__).parent / "logs"
DATA_DIR = Path(__file__).parent / "data"
LOG_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(LOG_DIR / "pipeline.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("fintrust.pipeline")

RAW_INPUT = DATA_DIR / "raw_transactions.csv"
CLEAN_CSV = DATA_DIR / "clean_transactions.csv"
SUMMARY_JSON = DATA_DIR / "daily_summary.json"
REQUIRED_COLUMNS = {"TxID", "AcctID", "TYPE", "Amount", "Date", "Desc"}


def validate_headers(fieldnames):
    """Raise ValueError when the input CSV is missing a required column."""
    if fieldnames is None:
        raise ValueError("CSV file has no header row")

    missing = REQUIRED_COLUMNS.difference(fieldnames)
    if missing:
        raise ValueError(f"CSV header is missing: {', '.join(sorted(missing))}")


def normalise_date(date_str):
    """Return a supported date in ISO format."""
    for date_format in ("%Y-%m-%d", "%d/%m/%y", "%d/%m/%Y"):
        try:
            return datetime.strptime(date_str.strip(), date_format).strftime("%Y-%m-%d")
        except ValueError:
            continue
    raise ValueError(f"unrecognised date format: {date_str!r}")


def clean_transaction(row, row_num):
    """Return a cleaned transaction or raise ValueError for unsuitable data."""
    try:
        return {
            "transaction_id": int(row["TxID"].strip()),
            "account_id": int(row["AcctID"].strip()),
            "type": row["TYPE"].strip().lower(),
            "amount": float(row["Amount"].strip()),
            "date": normalise_date(row["Date"]),
            "description": row.get("Desc", "").strip() or "No description",
        }
    except (KeyError, ValueError) as error:
        raise ValueError(f"Row {row_num}: {error}") from error


def main():
    logger.info("FinTrust transaction pipeline starting")
    logger.info("Input: %s", RAW_INPUT)

    if not RAW_INPUT.exists():
        logger.critical("Input file not found: %s", RAW_INPUT)
        return

    transactions = []
    skipped = 0

    try:
        with RAW_INPUT.open("r", newline="", encoding="utf-8") as input_file:
            reader = csv.DictReader(input_file)
            validate_headers(reader.fieldnames)
            for row_num, row in enumerate(reader, start=2):
                try:
                    transaction = clean_transaction(row, row_num)
                    transactions.append(transaction)
                    logger.debug(
                        "Processed row %d: transaction_id=%s",
                        row_num,
                        transaction["transaction_id"],
                    )
                except ValueError as error:
                    logger.warning("Skipped: %s", error)
                    skipped += 1
    except PermissionError:
        logger.error("Permission denied reading %s", RAW_INPUT)
        return
    except UnicodeDecodeError as error:
        logger.error("Encoding error in %s: %s", RAW_INPUT, error)
        return
    except ValueError as error:
        logger.error("Invalid CSV: %s", error)
        return

    logger.info("Processed: %d rows, skipped: %d", len(transactions), skipped)

    fieldnames = [
        "transaction_id",
        "account_id",
        "type",
        "amount",
        "date",
        "description",
    ]
    try:
        with CLEAN_CSV.open("w", newline="", encoding="utf-8") as output_file:
            writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(transactions)
        logger.info("Clean CSV written: %s", CLEAN_CSV)
    except OSError as error:
        logger.error("Failed to write CSV: %s", error)
        return

    deposits = [item for item in transactions if item["type"] == "deposit"]
    withdrawals = [item for item in transactions if item["type"] == "withdrawal"]
    summary = {
        "run_timestamp": datetime.now().isoformat(),
        "total": len(transactions),
        "deposits": len(deposits),
        "withdrawals": len(withdrawals),
        "sum_deposits": round(sum(item["amount"] for item in deposits), 2),
        "sum_withdrawals": round(sum(item["amount"] for item in withdrawals), 2),
        "skipped_rows": skipped,
    }
    try:
        with SUMMARY_JSON.open("w", encoding="utf-8") as summary_file:
            json.dump(summary, summary_file, indent=2)
        logger.info("Summary JSON written: %s", SUMMARY_JSON)
        logger.info("Pipeline complete")
    except OSError as error:
        logger.error("Failed to write summary: %s", error)


if __name__ == "__main__":
    main()
