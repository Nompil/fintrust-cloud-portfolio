"""
FinTrust CSV to SQLite Pipeline
"""

import csv
import sqlite3
from datetime import datetime
from pathlib import Path

CSV_FILE = Path("week04/transactions.csv")
DB_FILE = Path("week04/fintrust_analytics.db")

VALID_TYPES = {"TRANSFER", "DEPOSIT", "WITHDRAWAL"}
VALID_STATUSES = {"COMPLETED", "FAILED", "PENDING"}


def validate_row(row):
    """Return (True, None) if valid, otherwise (False, reason)."""

    if not row["account_from"].strip():
        return False, "missing account_from"

    try:
        amount = float(row["amount"])
    except (ValueError, TypeError):
        return False, f"invalid amount: {row['amount']!r}"

    if amount <= 0:
        return False, f"amount must be positive, got {amount}"

    if row["type"] not in VALID_TYPES:
        return False, f"unknown type: {row['type']!r}"

    if row["status"] not in VALID_STATUSES:
        return False, f"unknown status: {row['status']!r}"

    return True, None


def load_csv(filepath):
    """Read CSV and return valid and invalid rows."""

    valid = []
    invalid = []

    with open(filepath, newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for row in reader:

            ok, reason = validate_row(row)

            if ok:
                valid.append(row)
            else:
                invalid.append(
                    {
                        "row": row,
                        "reason": reason
                    }
                )

    return valid, invalid


def setup_database(db_path):
    """Create transactions table if it doesn't exist."""

    conn = sqlite3.connect(db_path)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id TEXT PRIMARY KEY,
            account_from TEXT NOT NULL,
            account_to TEXT,
            amount REAL NOT NULL,
            currency TEXT NOT NULL,
            type TEXT NOT NULL,
            status TEXT NOT NULL,
            timestamp TEXT,
            loaded_at TEXT NOT NULL
        )
    """)

    conn.commit()

    return conn


def insert_transactions(conn, valid_rows):
    """Insert valid rows and skip duplicates."""

    loaded_at = datetime.now().isoformat(timespec="seconds")

    inserted = 0
    skipped = 0

    for row in valid_rows:

        try:

            conn.execute(
                """
                INSERT INTO transactions
                (
                    transaction_id,
                    account_from,
                    account_to,
                    amount,
                    currency,
                    type,
                    status,
                    timestamp,
                    loaded_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    row["transaction_id"],
                    row["account_from"],
                    row["account_to"] or None,
                    float(row["amount"]),
                    row["currency"],
                    row["type"],
                    row["status"],
                    row["timestamp"],
                    loaded_at
                )
            )

            inserted += 1

        except sqlite3.IntegrityError:
            skipped += 1

    conn.commit()

    return inserted, skipped


if __name__ == "__main__":

    print("=== Phase 1: Loading CSV ===")

    valid_rows, invalid_rows = load_csv(CSV_FILE)

    print(f"Valid rows:   {len(valid_rows)}")
    print(f"Invalid rows: {len(invalid_rows)}")

    if invalid_rows:

        print("\nInvalid row details:")

        for entry in invalid_rows:

            txn_id = entry["row"].get(
                "transaction_id",
                "UNKNOWN"
            )

            print(
                f"  {txn_id}: {entry['reason']}"
            )

    print("\n=== Phase 2: Loading into SQLite ===")

    conn = setup_database(DB_FILE)

    inserted, skipped = insert_transactions(
        conn,
        valid_rows
    )

    print(f"Inserted: {inserted}")
    print(f"Skipped (duplicates): {skipped}")

    conn.close()