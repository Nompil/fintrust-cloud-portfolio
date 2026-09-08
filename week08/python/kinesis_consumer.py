"""Decode the Kinesis records delivered to a Lambda function."""

from __future__ import annotations

import base64
import json
from typing import Any


REQUIRED_FIELDS = {"transaction_id", "account_id", "amount", "currency", "type"}


def decode_record(record: dict[str, Any]) -> dict[str, Any]:
    encoded = record["kinesis"]["data"]
    transaction = json.loads(base64.b64decode(encoded).decode("utf-8"))
    missing = REQUIRED_FIELDS.difference(transaction)
    if missing:
        raise ValueError(f"Kinesis transaction is missing: {', '.join(sorted(missing))}")
    return transaction


def decode_event(event: dict[str, Any]) -> list[dict[str, Any]]:
    return [decode_record(record) for record in event.get("Records", [])]


def lambda_handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    transactions = decode_event(event)
    for transaction in transactions:
        print(
            f"Received {transaction['transaction_id']} for {transaction['account_id']}: "
            f"{transaction['amount']} {transaction['currency']}"
        )
    return {"processed": len(transactions)}
