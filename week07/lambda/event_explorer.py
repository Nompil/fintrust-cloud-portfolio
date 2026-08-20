"""Inspect API Gateway, SQS, and S3 Lambda event shapes safely."""

import json
import logging


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


def event_source(event):
    """Identify the source represented by a Lambda event payload."""
    records = event.get("Records", [])
    if records:
        source = records[0].get("eventSource", "")
        if source == "aws:sqs":
            return "sqs"
        if source == "aws:s3":
            return "s3"
    if "httpMethod" in event or "requestContext" in event:
        return "api_gateway"
    return "unknown"


def lambda_handler(event, context):
    """Return a compact event summary and log runtime context."""
    source = event_source(event)
    summary = {
        "source": source,
        "record_count": len(event.get("Records", [])),
        "function_name": getattr(context, "function_name", "local"),
        "aws_request_id": getattr(context, "aws_request_id", "local"),
    }
    remaining_time = getattr(context, "get_remaining_time_in_millis", lambda: 0)()
    summary["remaining_time_ms"] = remaining_time
    LOGGER.info("Event summary: %s", json.dumps(summary))
    return {"statusCode": 200, "body": json.dumps(summary)}
