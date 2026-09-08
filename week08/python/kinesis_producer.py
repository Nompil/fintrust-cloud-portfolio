"""Publish FinTrust transaction events to Kinesis Data Streams."""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from typing import Any, Iterable

import boto3


STREAM_NAME = "transaction-stream"


def build_transaction(
    account_id: str,
    amount: float,
    currency: str,
    transaction_type: str,
    *,
    transaction_id: str | None = None,
    timestamp: str | None = None,
) -> dict[str, Any]:
    if not account_id.strip():
        raise ValueError("account_id is required")
    if amount <= 0:
        raise ValueError("amount must be positive")
    return {
        "transaction_id": transaction_id or str(uuid.uuid4()),
        "account_id": account_id,
        "amount": round(float(amount), 2),
        "currency": currency.upper(),
        "type": transaction_type.upper(),
        "timestamp": timestamp or datetime.now(timezone.utc).isoformat(),
    }


class TransactionProducer:
    def __init__(
        self,
        stream_name: str = STREAM_NAME,
        region: str = "af-south-1",
        *,
        kinesis_client: Any | None = None,
    ) -> None:
        self.stream_name = stream_name
        self.kinesis = kinesis_client or boto3.client("kinesis", region_name=region)

    def publish_transaction(self, transaction: dict[str, Any]) -> dict[str, str]:
        account_id = transaction.get("account_id", "")
        if not account_id:
            raise ValueError("Transaction must contain account_id")
        response = self.kinesis.put_record(
            StreamName=self.stream_name,
            Data=json.dumps(transaction, separators=(",", ":")).encode("utf-8"),
            PartitionKey=account_id,
        )
        return {
            "sequence_number": response["SequenceNumber"],
            "shard_id": response["ShardId"],
        }

    def publish_batch(self, transactions: Iterable[dict[str, Any]]) -> dict[str, Any]:
        items = list(transactions)
        if not items:
            return {"sent": 0, "failed": 0, "failures": []}
        if len(items) > 500:
            raise ValueError("A Kinesis batch cannot contain more than 500 records")

        records = []
        for transaction in items:
            account_id = transaction.get("account_id", "")
            if not account_id:
                raise ValueError("Every transaction must contain account_id")
            records.append(
                {
                    "Data": json.dumps(transaction, separators=(",", ":")).encode("utf-8"),
                    "PartitionKey": account_id,
                }
            )

        response = self.kinesis.put_records(StreamName=self.stream_name, Records=records)
        failures = [
            {"index": index, **result}
            for index, result in enumerate(response.get("Records", []))
            if "ErrorCode" in result
        ]
        failed = response.get("FailedRecordCount", len(failures))
        return {"sent": len(records) - failed, "failed": failed, "failures": failures}
