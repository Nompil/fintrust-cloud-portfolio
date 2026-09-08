"""Read and validate the nightly FinTrust transaction export."""

import csv
from pathlib import Path


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
    """Read a CSV and separate valid rows from rejected rows."""
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
