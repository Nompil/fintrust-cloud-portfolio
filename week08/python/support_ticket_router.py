"""Redact PII and route FinTrust support tickets by sentiment."""

from __future__ import annotations

import json
from typing import Any


def redact_pii(text: str, comprehend_client: Any) -> tuple[str, list[str]]:
    response = comprehend_client.detect_pii_entities(Text=text, LanguageCode="en")
    entities = sorted(
        response.get("Entities", []),
        key=lambda entity: entity["BeginOffset"],
        reverse=True,
    )
    redacted = text
    for entity in entities:
        label = f"[{entity['Type']}]"
        redacted = redacted[: entity["BeginOffset"]] + label + redacted[entity["EndOffset"] :]
    types = sorted({entity["Type"] for entity in entities})
    return redacted, types


class SupportTicketRouter:
    def __init__(
        self,
        comprehend_client: Any,
        sqs_client: Any,
        urgent_queue_url: str,
        standard_queue_url: str,
    ) -> None:
        self.comprehend = comprehend_client
        self.sqs = sqs_client
        self.urgent_queue_url = urgent_queue_url
        self.standard_queue_url = standard_queue_url

    def process(self, ticket_text: str) -> dict[str, Any]:
        if not ticket_text.strip():
            raise ValueError("ticket_text is required")
        redacted_text, pii_types = redact_pii(ticket_text, self.comprehend)
        sentiment_response = self.comprehend.detect_sentiment(
            Text=ticket_text,
            LanguageCode="en",
        )
        sentiment = sentiment_response["Sentiment"]
        priority = "HIGH" if sentiment == "NEGATIVE" else "STANDARD"
        queue_url = self.urgent_queue_url if priority == "HIGH" else self.standard_queue_url
        message = {
            "redacted_text": redacted_text,
            "sentiment": sentiment,
            "pii_types_found": pii_types,
            "priority": priority,
        }
        self.sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(message))
        return message
