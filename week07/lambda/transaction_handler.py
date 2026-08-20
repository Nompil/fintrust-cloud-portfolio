"""Validate a transaction received through API Gateway."""

import json
import logging
import os


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
ENVIRONMENT = os.environ.get("ENVIRONMENT", "dev")


def _response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }


def lambda_handler(event, context):
    """Return an accepted response for a valid API Gateway transaction."""
    remaining = getattr(context, "get_remaining_time_in_millis", lambda: 30_000)()
    if remaining < 5_000:
        raise TimeoutError("Insufficient remaining time to complete safely")

    try:
        body = json.loads(event.get("body") or "{}")
    except json.JSONDecodeError:
        return _response(400, {"error": "Request body must contain valid JSON"})

    account_id = body.get("account_id")
    amount = body.get("amount")
    if not account_id or amount is None:
        return _response(400, {"error": "account_id and amount are required"})
    try:
        amount = float(amount)
    except (TypeError, ValueError):
        return _response(400, {"error": "amount must be numeric"})
    if amount <= 0:
        return _response(400, {"error": "amount must be positive"})

    LOGGER.info(
        "Accepted transaction for account %s in %s",
        account_id,
        ENVIRONMENT,
    )
    return _response(
        200,
        {
            "status": "accepted",
            "account_id": account_id,
            "amount": amount,
            "environment": ENVIRONMENT,
        },
    )
