import csv
from pathlib import Path

VALID_TYPES = {"TRANSFER", "DEPOSIT", "WITHDRAWAL"}
VALID_STATUSES = {"COMPLETED", "FAILED", "PENDING"}
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
    missing_columns = REQUIRED_COLUMNS.difference(row)
    if missing_columns:
        return False, f"missing columns: {', '.join(sorted(missing_columns))}"

    for key, value in row.items():
        row[key] = value.strip() if isinstance(value, str) else value

    row["type"] = row["type"].upper()
    row["status"] = row["status"].upper()
    row["currency"] = row["currency"].upper()

    if not row["transaction_id"]:
        return False, "missing transaction_id"

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


def load_csv(filepath: Path):
    valid = []
    invalid = []

    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        if reader.fieldnames is None:
            raise ValueError("CSV file has no header row")

        missing_columns = REQUIRED_COLUMNS.difference(reader.fieldnames)
        if missing_columns:
            missing = ", ".join(sorted(missing_columns))
            raise ValueError(f"CSV header is missing required columns: {missing}")

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
