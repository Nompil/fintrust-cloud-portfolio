import sqlite3
import pandas as pd
from pathlib import Path

DB_FILE = Path("fintrust_analytics.db")

conn = sqlite3.connect(DB_FILE)

df = pd.read_sql_query(
    "SELECT * FROM transactions",
    conn
)

conn.close()

print("=== DataFrame Shape ===")
print(f"Rows: {len(df)}  Columns: {len(df.columns)}")

print("\n=== Column Types ===")
print(df.dtypes)

print("\n=== First 3 Rows ===")
print(df.head(3))

completed_transfers = df[
    (df["status"] == "COMPLETED")
    & (df["type"] == "TRANSFER")
]

print(
    f"\nCompleted transfers: {len(completed_transfers)}"
)

print(
    f"Total volume: "
    f"ZAR {completed_transfers['amount'].sum():,.2f}"
)

by_status = (
    df.groupby("status")
      .agg(
          count=("transaction_id", "count"),
          total_volume=("amount", "sum"),
          avg_amount=("amount", "mean")
      )
      .round(2)
)

print("\n=== By Status ===")
print(by_status)

df["high_value"] = df["amount"] > 2000
df["txn_date"] = pd.to_datetime(
    df["timestamp"]
).dt.date

df.to_csv(
    "transactions_enriched.csv",
    index=False
)

print("\nExported to transactions_enriched.csv")