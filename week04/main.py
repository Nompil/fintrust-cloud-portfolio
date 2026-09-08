"""Run the packaged version of the FinTrust transaction pipeline."""

from pathlib import Path

from fintrust_pipeline import (
    generate_report,
    insert_transactions,
    load_csv,
    setup_database,
)


BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "transactions.csv"
DB_FILE = BASE_DIR / "fintrust_analytics.db"
REPORT_FILE = BASE_DIR / "daily_report.txt"


def run_pipeline():
    """Validate the CSV, load SQLite and refresh the daily report."""
    valid_rows, invalid_rows = load_csv(CSV_FILE)
    print(f"Valid: {len(valid_rows)}  Invalid: {len(invalid_rows)}")
    for entry in invalid_rows:
        txn_id = entry["row"].get("transaction_id", "?")
        print(f"  {txn_id}: {entry['reason']}")

    connection = setup_database(DB_FILE)
    try:
        inserted, skipped = insert_transactions(connection, valid_rows)
        print(f"Inserted: {inserted}  Skipped: {skipped}")
        report = generate_report(connection, REPORT_FILE)
        print(report)
    finally:
        connection.close()

    return inserted, skipped, invalid_rows


if __name__ == "__main__":
    run_pipeline()
