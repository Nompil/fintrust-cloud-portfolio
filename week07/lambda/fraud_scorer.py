"""Score SQS payment events and publish high-risk alerts to SNS."""

import json
import logging
import os


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
RISK_KEYWORDS = {"crypto": 20, "wire": 10, "urgent": 5, "casino": 20}
_SNS_CLIENT = None


def calculate_risk_score(transaction):
    """Return a transparent rule-based score and its contributing reasons."""
    score = 0.0
    reasons = []
    amount = float(transaction.get("amount", 0))
    if amount > 50_000:
        score += 40
        reasons.append("amount above R50,000")
    elif amount > 10_000:
        score += 20
        reasons.append("amount above R10,000")
    elif amount > 1_000:
        score += 5
        reasons.append("amount above R1,000")

    if transaction.get("currency", "ZAR") != "ZAR":
        score += 20
        reasons.append("cross-border currency")

    description = str(transaction.get("description", "")).lower()
    for keyword, points in RISK_KEYWORDS.items():
        if keyword in description:
            score += points
            reasons.append(f"keyword: {keyword}")
    return min(score, 100.0), reasons


def _sns_client():
    global _SNS_CLIENT
    if _SNS_CLIENT is None:
        import boto3

        _SNS_CLIENT = boto3.client(
            "sns", region_name=os.environ.get("AWS_REGION", "af-south-1")
        )
    return _SNS_CLIENT


def process_records(event, sns_client, topic_arn, threshold=75.0):
    """Process an SQS batch and report only the individual failed records."""
    failures = []
    for record in event.get("Records", []):
        message_id = record.get("messageId", "unknown")
        try:
            transaction = json.loads(record["body"])
            transaction_id = transaction["id"]
            score, reasons = calculate_risk_score(transaction)
            LOGGER.info("Transaction %s risk score: %.1f", transaction_id, score)
            if score >= threshold:
                sns_client.publish(
                    TopicArn=topic_arn,
                    Subject=f"HIGH RISK: Transaction {transaction_id}",
                    Message=json.dumps(
                        {
                            "transaction_id": transaction_id,
                            "account_id": transaction.get("account_id"),
                            "amount": transaction.get("amount"),
                            "currency": transaction.get("currency"),
                            "risk_score": score,
                            "reasons": reasons,
                        }
                    ),
                    MessageAttributes={
                        "risk_level": {
                            "DataType": "String",
                            "StringValue": "HIGH",
                        }
                    },
                )
        except (KeyError, TypeError, ValueError, json.JSONDecodeError):
            LOGGER.exception("Unable to process SQS message %s", message_id)
            failures.append({"itemIdentifier": message_id})
    return {"batchItemFailures": failures}


def lambda_handler(event, context):
    """Lambda entry point using execution-role credentials and environment config."""
    topic_arn = os.environ["ALERT_TOPIC_ARN"]
    threshold = float(os.environ.get("HIGH_RISK_THRESHOLD", "75"))
    return process_records(event, _sns_client(), topic_arn, threshold)
