import argparse
import sqlite3
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent


def analyse_transactions(db_path: Path, output_path: Path) -> None:
    connection = sqlite3.connect(db_path)
    try:
        transactions = pd.read_sql_query(
            "SELECT * FROM transactions ORDER BY timestamp, transaction_id",
            connection,
        )
    finally:
        connection.close()

    print("=== Dataset ===")
    print(f"Rows: {len(transactions)}  Columns: {len(transactions.columns)}")

    completed_transfers = transactions[
        (transactions["status"] == "COMPLETED")
        & (transactions["type"] == "TRANSFER")
    ]
    print(f"Completed transfers: {len(completed_transfers)}")
    print(f"Completed transfer volume: ZAR {completed_transfers['amount'].sum():,.2f}")

    by_status = transactions.groupby("status").agg(
        count=("transaction_id", "count"),
        total_volume=("amount", "sum"),
        average_amount=("amount", "mean"),
    ).round(2)
    print("\n=== By status ===")
    print(by_status)

    transactions["high_value"] = transactions["amount"] > 2000
    transactions["transaction_date"] = pd.to_datetime(
        transactions["timestamp"], errors="coerce"
    ).dt.date
    transactions.to_csv(output_path, index=False)
    print(f"\nExported: {output_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyse FinTrust SQLite transactions")
    parser.add_argument(
        "--database",
        type=Path,
        default=BASE_DIR / "fintrust_analytics.db",
        help="SQLite database created by main.py",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=BASE_DIR / "transactions_enriched.csv",
        help="Destination for the enriched CSV",
    )
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    if not arguments.database.exists():
        raise SystemExit(
            f"Database not found: {arguments.database}. Run week04/main.py first."
        )
    analyse_transactions(arguments.database, arguments.output)
