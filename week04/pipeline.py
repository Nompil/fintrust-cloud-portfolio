"""
FinTrust CSV to SQLite Dashboard Pipeline


"""

import csv
import sqlite3
from datetime import datetime
from pathlib import Path

CSV_FILE = Path("week04/transactions.csv")
DB_FILE = Path("week04/fintrust_analytics.db")
REPORT_FILE = Path("week04/daily_report.txt")

VALID_TYPES = {"TRANSFER", "DEPOSIT", "WITHDRAWAL"}
VALID_STATUSES = {"COMPLETED", "FAILED", "PENDING"}


def validate_row(row):
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
    valid = []
    invalid = []

    with open(filepath, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            ok, reason = validate_row(row)

            if ok:
                valid.append(row)
            else:
                invalid.append({"row": row, "reason": reason})

    return valid, invalid


def setup_database(db_path):
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
    loaded_at = datetime.now().isoformat(timespec="seconds")

    inserted = 0
    skipped = 0

    for row in valid_rows:
        try:
            conn.execute(
                """
                INSERT INTO transactions (
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


def generate_report(conn):
    lines = []

    lines.append("=" * 60)
    lines.append("FINTRUST DAILY TRANSACTION REPORT")
    lines.append(
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    lines.append("=" * 60)

    summary = conn.execute("""
        SELECT
            COUNT(*),
            ROUND(SUM(amount), 2),
            ROUND(AVG(amount), 2),
            ROUND(MIN(amount), 2),
            ROUND(MAX(amount), 2)
        FROM transactions
    """).fetchone()

    lines.append("")
    lines.append("SUMMARY")
    lines.append("-" * 40)

    lines.append(f"Total transactions : {summary[0]}")
    lines.append(f"Total volume       : ZAR {summary[1]:,.2f}")
    lines.append(f"Average amount     : ZAR {summary[2]:,.2f}")
    lines.append(f"Min / Max          : ZAR {summary[3]:,.2f} / ZAR {summary[4]:,.2f}")

    lines.append("")
    lines.append("BREAKDOWN BY TYPE")
    lines.append("-" * 40)

    rows = conn.execute("""
        SELECT
            type,
            COUNT(*),
            ROUND(SUM(amount), 2)
        FROM transactions
        GROUP BY type
        ORDER BY SUM(amount) DESC
    """).fetchall()

    for row in rows:
        lines.append(
            f"{row[0]:<12}  {row[1]:>3} txns   ZAR {row[2]:>10,.2f}"
        )

    lines.append("")
    lines.append("BREAKDOWN BY STATUS")
    lines.append("-" * 40)

    rows = conn.execute("""
        SELECT
            status,
            COUNT(*),
            ROUND(SUM(amount), 2)
        FROM transactions
        GROUP BY status
        ORDER BY COUNT(*) DESC
    """).fetchall()

    for row in rows:
        lines.append(
            f"{row[0]:<12}  {row[1]:>3} txns   ZAR {row[2]:>10,.2f}"
        )

    lines.append("")
    lines.append("TOP 3 LARGEST TRANSACTIONS")
    lines.append("-" * 40)

    rows = conn.execute("""
        SELECT
            transaction_id,
            account_from,
            amount,
            type,
            status
        FROM transactions
        ORDER BY amount DESC
        LIMIT 3
    """).fetchall()

    for i, row in enumerate(rows, start=1):
        lines.append(
            f"#{i}  {row[0]}  {row[1]}  ZAR {row[2]:,.2f}  [{row[3]} / {row[4]}]"
        )

    lines.append("")
    lines.append("=" * 60)

    report_text = "\n".join(lines)
    REPORT_FILE.write_text(report_text, encoding="utf-8")

    return report_text


if __name__ == "__main__":
    print("=== Phase 1: Loading CSV ===")
    valid_rows, invalid_rows = load_csv(CSV_FILE)

    print(f"Valid rows:   {len(valid_rows)}")
    print(f"Invalid rows: {len(invalid_rows)}")

    if invalid_rows:
        print("\nInvalid row details:")
        for entry in invalid_rows:
            txn_id = entry["row"]["transaction_id"]
            print(f"  {txn_id}: {entry['reason']}")

    print("\n=== Phase 2: Loading into SQLite ===")
    conn = setup_database(DB_FILE)
    inserted, skipped = insert_transactions(conn, valid_rows)

    print(f"Inserted: {inserted}")
    print(f"Skipped (duplicates): {skipped}")

    print("\n=== Phase 3: Generating Report ===")
    report = generate_report(conn)

    print(report)
    print(f"\nReport saved to: {REPORT_FILE}")

    conn.close()