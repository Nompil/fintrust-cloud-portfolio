"""FinTrust exports a transaction CSV from its legacy system each night.
This script validates every row before storing suitable records in SQLite.
It then writes a daily report that operations can check before the next load.
"""

import csv
import sqlite3
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "transactions.csv"
DB_FILE = BASE_DIR / "fintrust_analytics.db"
REPORT_FILE = BASE_DIR / "daily_report.txt"

VALID_TYPES = {"TRANSFER", "DEPOSIT", "WITHDRAWAL"}
VALID_STATUSES = {"COMPLETED", "FAILED", "PENDING"}
VALID_CURRENCIES = {"ZAR"}
REQUIRED_COLUMNS = {
    "transaction_id",
    "account_from",
    "account_to",
    "amount",
    "currency",
    "type",
    "status",
    "timestamp",
}


def validate_row(row):
    """Return whether a transaction row is suitable for loading."""
    missing = REQUIRED_COLUMNS.difference(row)
    if missing:
        return False, f"missing columns: {', '.join(sorted(missing))}"

    cleaned = {
        key: value.strip() if isinstance(value, str) else value
        for key, value in row.items()
    }
    cleaned["type"] = cleaned["type"].upper()
    cleaned["status"] = cleaned["status"].upper()
    cleaned["currency"] = cleaned["currency"].upper()
    row.update(cleaned)

    if not row["account_from"]:
        return False, "missing account_from"

    try:
        amount = float(row["amount"])
    except (TypeError, ValueError):
        return False, f"invalid amount: {row['amount']!r}"

    if amount <= 0:
        return False, f"amount must be positive, got {amount}"
    if row["type"] not in VALID_TYPES:
        return False, f"unknown type: {row['type']!r}"
    if row["status"] not in VALID_STATUSES:
        return False, f"unknown status: {row['status']!r}"
    if row["currency"] not in VALID_CURRENCIES:
        return False, f"unsupported currency: {row['currency']!r}"

    return True, None


def load_csv(filepath):
    """Read the source CSV and separate valid and invalid rows."""
    valid_rows = []
    invalid_rows = []

    with Path(filepath).open("r", newline="", encoding="utf-8") as source:
        reader = csv.DictReader(source)
        if reader.fieldnames is None:
            raise ValueError("CSV file has no header row")

        missing = REQUIRED_COLUMNS.difference(reader.fieldnames)
        if missing:
            names = ", ".join(sorted(missing))
            raise ValueError(f"CSV header is missing required columns: {names}")

        for row in reader:
            valid, reason = validate_row(row)
            if valid:
                valid_rows.append(row)
            else:
                invalid_rows.append({"row": row, "reason": reason})

    return valid_rows, invalid_rows


def setup_database(db_path):
    """Create the local transaction table and return its connection."""
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


def generate_report(connection, report_path):
    """Query the database and write the FinTrust daily report."""
    lines = [
        "=" * 60,
        "FINTRUST DAILY TRANSACTION REPORT",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "=" * 60,
    ]

    summary = connection.execute(
        """
        SELECT
            COUNT(*) AS total_count,
            ROUND(SUM(amount), 2) AS total_volume,
            ROUND(AVG(amount), 2) AS average_amount,
            ROUND(MIN(amount), 2) AS minimum_amount,
            ROUND(MAX(amount), 2) AS maximum_amount
        FROM transactions
        """
    ).fetchone()

    lines.extend(
        [
            "",
            "SUMMARY",
            f"  Total transactions : {summary['total_count']}",
            f"  Total volume       : ZAR {summary['total_volume']:,.2f}",
            f"  Average amount     : ZAR {summary['average_amount']:,.2f}",
            "  Min / Max          : "
            f"ZAR {summary['minimum_amount']:,.2f} / "
            f"ZAR {summary['maximum_amount']:,.2f}",
            "",
            "BREAKDOWN BY TYPE",
        ]
    )

    type_rows = connection.execute(
        """
        SELECT type, COUNT(*) AS count, ROUND(SUM(amount), 2) AS volume
        FROM transactions
        GROUP BY type
        ORDER BY volume DESC
        """
    ).fetchall()
    for row in type_rows:
        lines.append(
            f"  {row['type']:<12}  {row['count']:>3} txns   "
            f"ZAR {row['volume']:>10,.2f}"
        )

    lines.extend(["", "BREAKDOWN BY STATUS"])
    status_rows = connection.execute(
        """
        SELECT status, COUNT(*) AS count, ROUND(SUM(amount), 2) AS volume
        FROM transactions
        GROUP BY status
        ORDER BY count DESC, status
        """
    ).fetchall()
    for row in status_rows:
        lines.append(
            f"  {row['status']:<12}  {row['count']:>3} txns   "
            f"ZAR {row['volume']:>10,.2f}"
        )

    lines.extend(["", "TOP 3 LARGEST TRANSACTIONS"])
    largest_rows = connection.execute(
        """
        SELECT transaction_id, account_from, amount, type, status
        FROM transactions
        ORDER BY amount DESC
        LIMIT 3
        """
    ).fetchall()
    for position, row in enumerate(largest_rows, start=1):
        lines.append(
            f"  #{position}  {row['transaction_id']}  {row['account_from']}  "
            f"ZAR {row['amount']:,.2f}  [{row['type']} / {row['status']}]"
        )

    lines.extend(["", "=" * 60])
    report_text = "\n".join(lines)
    Path(report_path).write_text(report_text + "\n", encoding="utf-8")
    return report_text


def run_pipeline():
    """Run all three phases and return the load counts."""
    print("=== Phase 1: Loading CSV ===")
    valid_rows, invalid_rows = load_csv(CSV_FILE)
    print(f"Valid rows:   {len(valid_rows)}")
    print(f"Invalid rows: {len(invalid_rows)}")
    for entry in invalid_rows:
        transaction_id = entry["row"].get("transaction_id", "?")
        print(f"  {transaction_id}: {entry['reason']}")

    print("\n=== Phase 2: Loading into SQLite ===")
    connection = setup_database(DB_FILE)
    try:
        inserted, skipped = insert_transactions(connection, valid_rows)
        print(f"Inserted: {inserted}")
        print(f"Skipped (duplicates): {skipped}")

        print("\n=== Phase 3: Generating Report ===")
        report = generate_report(connection, REPORT_FILE)
        print(report)
        print(f"\nReport saved to: {REPORT_FILE.name}")
    finally:
        connection.close()

    return inserted, skipped, invalid_rows


if __name__ == "__main__":
    run_pipeline()
