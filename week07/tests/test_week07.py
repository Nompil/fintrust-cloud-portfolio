"""Local tests for the Week 7 APIs and event pipeline."""

import importlib
import json
import unittest

from fastapi.testclient import TestClient

from week07.api.fastapi_app import app as fastapi_app
from week07.api.flask_app import create_app
from week07.messaging.payment_publisher import PaymentPublisher


event_explorer = importlib.import_module("week07.lambda.event_explorer")
fraud_scorer = importlib.import_module("week07.lambda.fraud_scorer")
transaction_handler = importlib.import_module("week07.lambda.transaction_handler")


class RecordingSQS:
    def __init__(self):
        self.requests = []

    def send_message(self, **request):
        self.requests.append(request)
        return {"MessageId": "message-001"}


class RecordingSNS:
    def __init__(self):
        self.requests = []

    def publish(self, **request):
        self.requests.append(request)
        return {"MessageId": "alert-001"}


class LambdaContext:
    function_name = "fintrust-local-test"
    aws_request_id = "request-001"

    @staticmethod
    def get_remaining_time_in_millis():
        return 20_000


class WeekSevenTests(unittest.TestCase):
    def test_flask_transaction_lifecycle_and_request_id(self):
        sqs = RecordingSQS()
        app = create_app(PaymentPublisher(sqs, "queue-url"))
        client = app.test_client()

        created = client.post(
            "/transactions",
            json={"account_id": "ACC-001", "amount": 500, "currency": "ZAR"},
        )
        self.assertEqual(created.status_code, 201)
        self.assertIn("X-Request-ID", created.headers)
        transaction = created.get_json()
        self.assertEqual(sqs.requests[0]["MessageGroupId"], "ACC-001")

        updated = client.patch(
            f"/transactions/{transaction['id']}/status",
            json={"status": "approved"},
        )
        self.assertEqual(updated.get_json()["status"], "approved")
        self.assertEqual(
            client.get(f"/transactions/{transaction['id']}").status_code,
            200,
        )

    def test_flask_rejects_invalid_transaction(self):
        response = create_app().test_client().post(
            "/transactions",
            json={"account_id": "ACC-001", "amount": -1, "currency": "zar"},
        )
        self.assertEqual(response.status_code, 400)

    def test_fastapi_extension_endpoints(self):
        fastapi_app.state.transactions = []
        client = TestClient(fastapi_app)
        created = client.post(
            "/transactions",
            json={"account_id": "ACC-002", "amount": 1200, "currency": "ZAR"},
        )
        self.assertEqual(created.status_code, 201)
        self.assertIn("X-Request-ID", created.headers)
        transaction_id = created.json()["id"]
        self.assertEqual(
            client.patch(
                f"/transactions/{transaction_id}/status",
                json={"status": "rejected"},
            ).json()["status"],
            "rejected",
        )
        self.assertEqual(client.get("/transactions/missing").status_code, 404)

    def test_fastapi_pydantic_validation(self):
        fastapi_app.state.transactions = []
        response = TestClient(fastapi_app).post(
            "/transactions",
            json={"account_id": "", "amount": 0, "currency": "zar"},
        )
        self.assertEqual(response.status_code, 422)

    def test_fifo_publisher_uses_account_group_and_transaction_deduplication(self):
        sqs = RecordingSQS()
        publisher = PaymentPublisher(sqs, "queue-url")
        message_id = publisher.publish({"id": "txn-001", "account_id": "ACC-009"})
        self.assertEqual(message_id, "message-001")
        self.assertEqual(sqs.requests[0]["MessageGroupId"], "ACC-009")
        self.assertEqual(sqs.requests[0]["MessageDeduplicationId"], "txn-001")

    def test_high_risk_transaction_scores_95(self):
        score, reasons = fraud_scorer.calculate_risk_score(
            {
                "amount": 75000,
                "currency": "USD",
                "description": "urgent crypto wire transfer",
            }
        )
        self.assertEqual(score, 95)
        self.assertIn("cross-border currency", reasons)

    def test_scorer_publishes_alert_and_reports_only_failed_message(self):
        sns = RecordingSNS()
        event = {
            "Records": [
                {
                    "messageId": "good",
                    "body": json.dumps(
                        {
                            "id": "txn-002",
                            "account_id": "ACC-999",
                            "amount": 75000,
                            "currency": "USD",
                            "description": "urgent crypto wire transfer",
                        }
                    ),
                },
                {"messageId": "bad", "body": "not-json"},
            ]
        }
        with self.assertLogs(fraud_scorer.LOGGER, level="ERROR"):
            result = fraud_scorer.process_records(event, sns, "topic-arn")
        self.assertEqual(result, {"batchItemFailures": [{"itemIdentifier": "bad"}]})
        self.assertEqual(len(sns.requests), 1)
        self.assertEqual(json.loads(sns.requests[0]["Message"])["risk_score"], 95)

    def test_transaction_handler_validates_api_gateway_body(self):
        accepted = transaction_handler.lambda_handler(
            {"body": json.dumps({"account_id": "ACC-001", "amount": 250})},
            LambdaContext(),
        )
        self.assertEqual(accepted["statusCode"], 200)
        rejected = transaction_handler.lambda_handler(
            {"body": json.dumps({"account_id": "ACC-001"})},
            LambdaContext(),
        )
        self.assertEqual(rejected["statusCode"], 400)

    def test_event_explorer_identifies_sqs_event(self):
        event = {"Records": [{"eventSource": "aws:sqs", "body": "{}"}]}
        response = event_explorer.lambda_handler(event, LambdaContext())
        self.assertEqual(json.loads(response["body"])["source"], "sqs")


if __name__ == "__main__":
    unittest.main()
