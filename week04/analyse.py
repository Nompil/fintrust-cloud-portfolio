import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_FILE = BASE_DIR / "fintrust_analytics.db"

conn = sqlite3.connect(DB_FILE)
df = pd.read_sql_query("SELECT * FROM transactions", conn)
conn.close()

print("=== DataFrame Shape ===")
print(f"Rows: {len(df)}  Columns: {len(df.columns)}")
print()

print("=== Column Types ===")
print(df.dtypes)
print()

print("=== First 3 Rows ===")
print(df.head(3))
print()

completed_transfers = df[
    (df["status"] == "COMPLETED") & (df["type"] == "TRANSFER")
]
print(f"Completed transfers: {len(completed_transfers)}")
print(f"Total volume: ZAR {completed_transfers['amount'].sum():,.2f}")
print()

by_status = df.groupby("status").agg(
    count=("transaction_id", "count"),
    total_volume=("amount", "sum"),
    avg_amount=("amount", "mean"),
).round(2)
print("=== By Status ===")
print(by_status)
print()

df["high_value"] = df["amount"] > 2000
df["txn_date"] = pd.to_datetime(df["timestamp"]).dt.date

df.to_csv(BASE_DIR / "transactions_enriched.csv", index=False)
print("Exported to transactions_enriched.csv")