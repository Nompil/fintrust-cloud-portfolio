from __future__ import annotations

import base64
import csv
import io
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from week08.python.athena_reporter import FinTrustComplianceReporter, list_glue_tables
from week08.python.fraud_endpoint import classify_probability, invoke_fraud_endpoint
from week08.python.kinesis_consumer import decode_event
from week08.python.kinesis_producer import TransactionProducer, build_transaction
from week08.python.kyc_verification import kyc_verify
from week08.python.parquet_pipeline import (
    load_transactions,
    prepare_transactions,
    summarise,
    upload_partitions,
    write_partitions,
)
from week08.python.security_event_indexer import (
    find_high_risk_events,
    index_security_event,
)
from week08.python.support_ticket_router import SupportTicketRouter, redact_pii


class FakeAthena:
    def __init__(self, final_state: str = "SUCCEEDED") -> None:
        self.final_state = final_state
        self.status_checks = 0
        self.started: dict = {}

    def start_query_execution(self, **request):
        self.started = request
        return {"QueryExecutionId": "query-123"}

    def get_query_execution(self, **request):
        self.status_checks += 1
        state = "RUNNING" if self.status_checks == 1 else self.final_state
        status = {"State": state}
        if state == "FAILED":
            status["StateChangeReason"] = "Invalid table"
        return {"QueryExecution": {"Status": status}}

    def get_query_results(self, **request):
        return {
            "ResultSet": {
                "Rows": [
                    {"Data": [{"VarCharValue": "account_id"}, {"VarCharValue": "total"}]},
                    {"Data": [{"VarCharValue": "ACC-0002"}, {"VarCharValue": "87000.00"}]},
                    {"Data": [{"VarCharValue": "ACC-0004"}, {"VarCharValue": "56000.00"}]},
                ]
            }
        }


class FakeS3:
    def __init__(self) -> None:
        self.uploads: list[tuple[str, str, str]] = []

    def upload_file(self, local_path, bucket, key):
        self.uploads.append((local_path, bucket, key))


class FakeGlue:
    def get_tables(self, **request):
        return {
            "TableList": [
                {
                    "Name": "transactions",
                    "StorageDescriptor": {
                        "Location": "s3://fintrust-processed/transactions/",
                        "Columns": [{"Name": "amount", "Type": "decimal(18,2)"}],
                    },
                    "PartitionKeys": [
                        {"Name": "year", "Type": "string"},
                        {"Name": "month", "Type": "string"},
                    ],
                }
            ]
        }


class FakeKinesis:
    def __init__(self) -> None:
        self.single_request: dict = {}
        self.batch_request: dict = {}

    def put_record(self, **request):
        self.single_request = request
        return {"SequenceNumber": "1001", "ShardId": "shardId-000000000003"}

    def put_records(self, **request):
        self.batch_request = request
        return {
            "FailedRecordCount": 1,
            "Records": [
                {"SequenceNumber": "1001", "ShardId": "shardId-000000000001"},
                {"ErrorCode": "ProvisionedThroughputExceededException", "ErrorMessage": "retry"},
            ],
        }


class FakeOpenSearch:
    def __init__(self) -> None:
        self.index_request: dict = {}

    def index(self, **request):
        self.index_request = request
        return {"_id": "security-1"}

    def search(self, **request):
        return {
            "hits": {
                "hits": [
                    {"_source": {"event_type": "SUSPICIOUS_LOGIN", "risk_score": 87}}
                ]
            }
        }


class FakeBody:
    def __init__(self, value) -> None:
        self.value = value

    def read(self):
        return json.dumps(self.value).encode("utf-8")


class FakeSageMakerRuntime:
    def __init__(self, probability: float) -> None:
        self.probability = probability
        self.request: dict = {}

    def invoke_endpoint(self, **request):
        self.request = request
        return {"Body": FakeBody({"fraud_probability": self.probability})}


class FakeRekognition:
    def __init__(self, similarity: float | None) -> None:
        self.similarity = similarity
        self.request: dict = {}

    def compare_faces(self, **request):
        self.request = request
        matches = [] if self.similarity is None else [{"Similarity": self.similarity}]
        return {"FaceMatches": matches}


class FakeComprehend:
    def __init__(self, sentiment: str = "NEGATIVE") -> None:
        self.sentiment = sentiment

    def detect_pii_entities(self, Text, LanguageCode):
        name = "Nomsa"
        phone = "083 555 1234"
        return {
            "Entities": [
                {
                    "Type": "NAME",
                    "BeginOffset": Text.index(name),
                    "EndOffset": Text.index(name) + len(name),
                },
                {
                    "Type": "PHONE",
                    "BeginOffset": Text.index(phone),
                    "EndOffset": Text.index(phone) + len(phone),
                },
            ]
        }

    def detect_sentiment(self, Text, LanguageCode):
        return {"Sentiment": self.sentiment}


class FakeSQS:
    def __init__(self) -> None:
        self.request: dict = {}

    def send_message(self, **request):
        self.request = request
        return {"MessageId": "message-1"}


class WeekEightTests(unittest.TestCase):
    def test_athena_report_writes_csv(self):
        athena = FakeAthena()
        s3 = FakeS3()
        reporter = FinTrustComplianceReporter(
            "fintrust_curated",
            "fintrust-curated",
            athena_client=athena,
            s3_client=s3,
            poll_seconds=0,
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            rows = reporter.run_report("high_value", "SELECT 1", temp_dir)
            with (Path(temp_dir) / "high_value.csv").open(encoding="utf-8") as report:
                saved = list(csv.reader(report))
        self.assertEqual(rows, 2)
        self.assertEqual(saved[0], ["account_id", "total"])
        self.assertEqual(athena.started["QueryExecutionContext"]["Database"], "fintrust_curated")

    def test_athena_failure_includes_reason(self):
        reporter = FinTrustComplianceReporter(
            "fintrust_curated",
            "fintrust-curated",
            athena_client=FakeAthena("FAILED"),
            s3_client=FakeS3(),
            poll_seconds=0,
        )
        with self.assertRaisesRegex(RuntimeError, "Invalid table"):
            reporter.run_report("failed_report", "SELECT bad")

    def test_glue_catalog_details(self):
        tables = list_glue_tables("fintrust_curated", glue_client=FakeGlue())
        self.assertEqual(tables[0]["name"], "transactions")
        self.assertEqual([key["Name"] for key in tables[0]["partition_keys"]], ["year", "month"])

    def test_transaction_builder_validates_amount(self):
        with self.assertRaisesRegex(ValueError, "positive"):
            build_transaction("ACC-0001", 0, "ZAR", "PAYMENT")

    def test_kinesis_uses_account_partition_key(self):
        kinesis = FakeKinesis()
        producer = TransactionProducer(kinesis_client=kinesis)
        transaction = build_transaction(
            "ACC-0001",
            1500,
            "zar",
            "payment",
            transaction_id="txn-001",
            timestamp="2026-08-24T09:15:33+00:00",
        )
        result = producer.publish_transaction(transaction)
        self.assertEqual(kinesis.single_request["PartitionKey"], "ACC-0001")
        self.assertEqual(result["shard_id"], "shardId-000000000003")

    def test_kinesis_batch_reports_failed_records(self):
        kinesis = FakeKinesis()
        producer = TransactionProducer(kinesis_client=kinesis)
        result = producer.publish_batch(
            [
                {"transaction_id": "txn-1", "account_id": "ACC-1", "amount": 10},
                {"transaction_id": "txn-2", "account_id": "ACC-2", "amount": 20},
            ]
        )
        self.assertEqual(result["sent"], 1)
        self.assertEqual(result["failures"][0]["index"], 1)

    def test_kinesis_event_decoding(self):
        transaction = {
            "transaction_id": "txn-1",
            "account_id": "ACC-1",
            "amount": 100,
            "currency": "ZAR",
            "type": "PAYMENT",
        }
        encoded = base64.b64encode(json.dumps(transaction).encode()).decode()
        decoded = decode_event({"Records": [{"kinesis": {"data": encoded}}]})
        self.assertEqual(decoded, [transaction])

    def test_security_event_uses_monthly_index(self):
        client = FakeOpenSearch()
        result = index_security_event(
            client,
            {"event_type": "SUSPICIOUS_LOGIN", "risk_score": 87},
            recorded_at=datetime(2026, 8, 25, tzinfo=timezone.utc),
        )
        self.assertEqual(result["index"], "fintrust-security-2026-08")
        self.assertEqual(client.index_request["body"]["risk_score"], 87)

    def test_high_risk_search_returns_sources(self):
        results = find_high_risk_events(FakeOpenSearch(), "fintrust-security-*")
        self.assertEqual(results[0]["risk_score"], 87)

    def test_parquet_pipeline_writes_date_partitions(self):
        source = Path(__file__).parents[1] / "data" / "transactions.csv"
        prepared = prepare_transactions(load_transactions(source))
        with tempfile.TemporaryDirectory() as temp_dir:
            files = write_partitions(prepared, temp_dir)
            frames = [pd.read_parquet(file_path) for file_path in files]
        combined = pd.concat(frames, ignore_index=True)
        self.assertEqual(len(files), 2)
        self.assertEqual(len(combined), 8)
        self.assertEqual(int(combined["is_high_value"].sum()), 3)

    def test_parquet_summary(self):
        source = Path(__file__).parents[1] / "data" / "transactions.csv"
        summary = summarise(prepare_transactions(load_transactions(source)))
        self.assertEqual(summary["rows"], 8)
        self.assertEqual(summary["total_by_currency"]["ZAR"], 218695.5)

    def test_partition_upload_keeps_hive_path(self):
        s3 = FakeS3()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            file_path = root / "year=2026" / "month=08" / "transactions.parquet"
            file_path.parent.mkdir(parents=True)
            file_path.touch()
            keys = upload_partitions([file_path], root, "fintrust-processed", s3_client=s3)
        self.assertEqual(keys, ["transactions/year=2026/month=08/transactions.parquet"])

    def test_fraud_probability_boundaries(self):
        self.assertEqual(classify_probability(0.29), "ACCEPT")
        self.assertEqual(classify_probability(0.3), "REVIEW")
        self.assertEqual(classify_probability(0.7), "REVIEW")
        self.assertEqual(classify_probability(0.71), "REJECT")

    def test_sagemaker_request_uses_28_features(self):
        client = FakeSageMakerRuntime(0.82)
        result = invoke_fraud_endpoint(client, "fintrust-fraud-endpoint", range(28))
        self.assertEqual(result["decision"], "REJECT")
        self.assertEqual(client.request["ContentType"], "text/csv")

    def test_kyc_face_match(self):
        client = FakeRekognition(97.4)
        result = kyc_verify(client, "kyc", "selfie.jpg", "kyc", "id.jpg")
        self.assertEqual(result["decision"], "APPROVE")
        self.assertEqual(client.request["SimilarityThreshold"], 95.0)

    def test_kyc_no_match_is_rejected(self):
        result = kyc_verify(FakeRekognition(None), "kyc", "selfie.jpg", "kyc", "id.jpg")
        self.assertEqual(result["decision"], "REJECT")

    def test_pii_is_redacted_from_ticket(self):
        text = "Nomsa called from 083 555 1234 about a payment."
        redacted, types = redact_pii(text, FakeComprehend())
        self.assertEqual(redacted, "[NAME] called from [PHONE] about a payment.")
        self.assertEqual(types, ["NAME", "PHONE"])

    def test_negative_ticket_uses_urgent_queue(self):
        comprehend = FakeComprehend("NEGATIVE")
        sqs = FakeSQS()
        router = SupportTicketRouter(comprehend, sqs, "urgent-url", "standard-url")
        message = router.process("Nomsa called from 083 555 1234 about a payment.")
        self.assertEqual(message["priority"], "HIGH")
        self.assertEqual(sqs.request["QueueUrl"], "urgent-url")
        self.assertNotIn("083 555 1234", sqs.request["MessageBody"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
