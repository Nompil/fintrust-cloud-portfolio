"""Analyse the validated FinTrust transactions with pandas."""

import sqlite3
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
DB_FILE = BASE_DIR / "fintrust_analytics.db"
OUTPUT_FILE = BASE_DIR / "transactions_enriched.csv"


def load_transactions(db_path=DB_FILE):
    """Load the SQLite transaction table into a DataFrame."""
    if not Path(db_path).exists():
        raise FileNotFoundError("Run main.py first to create fintrust_analytics.db")

    connection = sqlite3.connect(db_path)
    try:
        return pd.read_sql_query("SELECT * FROM transactions", connection)
    finally:
        connection.close()


def analyse_transactions(dataframe):
    """Print the required filters and groupings, then add two columns."""
    print("=== DataFrame Shape ===")
    print(f"Rows: {len(dataframe)}  Columns: {len(dataframe.columns)}")
    print("\n=== Column Types ===")
    print(dataframe.dtypes)
    print("\n=== First 3 Rows ===")
    print(dataframe.head(3))

    completed_transfers = dataframe[
        (dataframe["status"] == "COMPLETED")
        & (dataframe["type"] == "TRANSFER")
    ]
    print(f"\nCompleted transfers: {len(completed_transfers)}")
    print(
        "Total volume: "
        f"ZAR {completed_transfers['amount'].sum():,.2f}"
    )

    average = dataframe["amount"].mean()
    large = dataframe[dataframe["amount"] > average]
    print(f"\nAbove-average transactions (>{average:,.2f}):")
    print(large[["transaction_id", "amount", "type", "status"]])

    by_status = dataframe.groupby("status").agg(
        count=("transaction_id", "count"),
        total_volume=("amount", "sum"),
        average_amount=("amount", "mean"),
    ).round(2)
    print("\n=== By Status ===")
    print(by_status)

    by_type = (
        dataframe.groupby("type")["amount"]
        .sum()
        .sort_values(ascending=False)
    )
    print("\n=== Volume by Type ===")
    print(by_type)

    enriched = dataframe.copy()
    enriched["high_value"] = enriched["amount"] > 2000
    enriched["txn_date"] = pd.to_datetime(enriched["timestamp"]).dt.date
    return enriched, by_status, by_type


def run_analysis(db_path=DB_FILE, output_path=OUTPUT_FILE):
    """Run the analysis and export the enriched transaction data."""
    dataframe = load_transactions(db_path)
    enriched, by_status, by_type = analyse_transactions(dataframe)
    enriched.to_csv(output_path, index=False)
    print(f"\nExported to {Path(output_path).name}")
    return enriched, by_status, by_type


if __name__ == "__main__":
    run_analysis()
