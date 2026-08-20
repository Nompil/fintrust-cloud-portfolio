"""Publish validated FinTrust payment events to an SQS FIFO queue."""

import json


class PaymentPublisher:
    """Small SQS adapter that keeps AWS calls outside the API logic."""

    def __init__(self, sqs_client, queue_url):
        if not queue_url:
            raise ValueError("A payment queue URL is required")
        self.sqs_client = sqs_client
        self.queue_url = queue_url

    def publish(self, transaction):
        """Publish one transaction and preserve ordering within its account."""
        response = self.sqs_client.send_message(
            QueueUrl=self.queue_url,
            MessageBody=json.dumps(transaction),
            MessageGroupId=transaction["account_id"],
            MessageDeduplicationId=transaction["id"],
        )
        return response["MessageId"]
