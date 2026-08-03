from pathlib import Path

from fintrust_pipeline.loader import load_csv
from fintrust_pipeline.database import setup_database, insert_transactions
from fintrust_pipeline.reporter import generate_report

BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "transactions.csv"
DB_FILE = BASE_DIR / "fintrust_analytics.db"
REPORT_FILE = BASE_DIR / "daily_report.txt"

if __name__ == "__main__":
    print("=== Phase 1: Loading CSV ===")
    valid_rows, invalid_rows = load_csv(CSV_FILE)
    print(f"Valid rows:   {len(valid_rows)}")
    print(f"Invalid rows: {len(invalid_rows)}")

    if invalid_rows:
        print("\nInvalid row details:")
        for entry in invalid_rows:
            txn_id = entry["row"].get("transaction_id", "?")
            print(f"  {txn_id}: {entry['reason']}")

    print("\n=== Phase 2: Loading into SQLite ===")
    conn = setup_database(DB_FILE)
    inserted, skipped = insert_transactions(conn, valid_rows)
    print(f"Inserted: {inserted}")
    print(f"Skipped (duplicates): {skipped}")

    print("\n=== Phase 3: Generating Report ===")
    report = generate_report(conn, REPORT_FILE)
    print(report)
    print(f"\nReport saved to: {REPORT_FILE}")

    conn.close()
