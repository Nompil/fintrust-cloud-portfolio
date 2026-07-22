"""
clean_transactions_v2.py

Transaction pipeline with error handling and logging.
"""

import csv
import json
import logging
from datetime import datetime
from pathlib import Path

# Logging setup
LOG_DIR = Path("logs")
DATA_DIR = Path("data")

LOG_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(LOG_DIR / "pipeline.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("fintrust.pipeline")

# File locations
RAW_INPUT = DATA_DIR / "raw_transactions.csv"
CLEAN_CSV = DATA_DIR / "clean_transactions.csv"
SUMMARY_JSON = DATA_DIR / "daily_summary.json"


def normalise_date(date_str):
    """Convert dates into YYYY-MM-DD format."""

    formats = (
        "%Y-%m-%d",
        "%d/%m/%y",
        "%d/%m/%Y",
    )

    date_str = date_str.strip()

    for fmt in formats:
        try:
            return (
                datetime.strptime(date_str, fmt)
                .strftime("%Y-%m-%d")
            )
        except ValueError:
            continue

    logger.warning(
        "Unrecognised date format '%s'",
        date_str
    )

    return date_str


def clean_transaction(row, row_num):
    """Validate and clean a transaction record."""

    try:
        return {
            "transaction_id":
                int(row["TxID"].strip()),

            "account_id":
                int(row["AcctID"].strip()),

            "type":
                row["TYPE"]
                .strip()
                .lower(),

            "amount":
                float(
                    row["Amount"]
                    .strip()
                ),

            "date":
                normalise_date(
                    row["Date"]
                ),

            "description":
                row["Desc"].strip()
                or "No description"
        }

    except (KeyError, ValueError) as exc:
        raise ValueError(
            f"Row {row_num}: {exc}"
        ) from exc


def build_summary(transactions):
    """Generate summary statistics."""

    deposits = [
        tx for tx in transactions
        if tx["type"] == "deposit"
    ]

    withdrawals = [
        tx for tx in transactions
        if tx["type"] == "withdrawal"
    ]

    return {
        "run_timestamp":
            datetime.now().isoformat(),

        "total_transactions":
            len(transactions),

        "total_deposits":
            len(deposits),

        "total_withdrawals":
            len(withdrawals),

        "sum_deposits":
            round(
                sum(
                    tx["amount"]
                    for tx in deposits
                ),
                2
            ),

        "sum_withdrawals":
            round(
                sum(
                    tx["amount"]
                    for tx in withdrawals
                ),
                2
            )
    }


def main():

    logger.info(
        "=== FinTrust Transaction Pipeline Starting ==="
    )

    if not RAW_INPUT.exists():
        logger.critical(
            "Input file not found: %s",
            RAW_INPUT
        )
        return

    transactions = []
    skipped = 0

    try:

        with open(
            RAW_INPUT,
            "r",
            newline="",
            encoding="utf-8"
        ) as fin:

            reader = csv.DictReader(fin)

            for row_num, row in enumerate(
                reader,
                start=2
            ):
                try:
                    tx = clean_transaction(
                        row,
                        row_num
                    )

                    transactions.append(tx)

                except ValueError as exc:

                    logger.warning(
                        "Skipped row: %s",
                        exc
                    )

                    skipped += 1

    except PermissionError:

        logger.error(
            "Permission denied reading file"
        )

        return

    except UnicodeDecodeError as exc:

        logger.error(
            "Encoding error: %s",
            exc
        )

        return

    logger.info(
        "Processed %d rows, skipped %d",
        len(transactions),
        skipped
    )

    try:

        fieldnames = [
            "transaction_id",
            "account_id",
            "type",
            "amount",
            "date",
            "description"
        ]

        with open(
            CLEAN_CSV,
            "w",
            newline="",
            encoding="utf-8"
        ) as fout:

            writer = csv.DictWriter(
                fout,
                fieldnames=fieldnames
            )

            writer.writeheader()
            writer.writerows(
                transactions
            )

        logger.info(
            "Clean CSV written: %s",
            CLEAN_CSV
        )

    except OSError as exc:

        logger.error(
            "Failed to write CSV: %s",
            exc
        )

    try:

        summary = build_summary(
            transactions
        )

        summary["skipped_rows"] = skipped

        with open(
            SUMMARY_JSON,
            "w",
            encoding="utf-8"
        ) as fout:

            json.dump(
                summary,
                fout,
                indent=2
            )

        logger.info(
            "Summary JSON written: %s",
            SUMMARY_JSON
        )

        logger.info(
            "Deposits: %d | Withdrawals: %d",
            summary["total_deposits"],
            summary["total_withdrawals"]
        )

        logger.info(
            "Output files generated successfully"
        )

        logger.info(
            "=== Pipeline Complete ==="
        )

    except OSError as exc:

        logger.error(
            "Failed to write summary: %s",
            exc
        )


if __name__ == "__main__":
    main()