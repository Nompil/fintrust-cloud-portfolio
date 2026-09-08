"""Create and populate the local FinTrust SQLite database."""

import sqlite3
from datetime import datetime


def setup_database(db_path):
    """Create the transactions table and return its connection."""
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id TEXT PRIMARY KEY,
            account_from   TEXT NOT NULL,
            account_to     TEXT,
            amount         REAL NOT NULL,
            currency       TEXT NOT NULL,
            type           TEXT NOT NULL,
            status         TEXT NOT NULL,
            timestamp      TEXT,
            loaded_at      TEXT NOT NULL
        )
        """
    )
    connection.commit()
    return connection


def insert_transactions(connection, valid_rows):
    """Insert valid rows and count transaction IDs already present."""
    loaded_at = datetime.now().isoformat(timespec="seconds")
    inserted = 0
    skipped = 0

    for row in valid_rows:
        try:
            connection.execute(
                """
                INSERT INTO transactions (
                    transaction_id, account_from, account_to, amount,
                    currency, type, status, timestamp, loaded_at
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
                    loaded_at,
                ),
            )
            inserted += 1
        except sqlite3.IntegrityError:
            skipped += 1

    connection.commit()
    return inserted, skipped
