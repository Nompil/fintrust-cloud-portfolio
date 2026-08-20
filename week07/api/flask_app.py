"""Flask implementation of the FinTrust transaction API."""

import os
import uuid
from datetime import datetime, timezone

from flask import Flask, jsonify, request

from week07.messaging.payment_publisher import PaymentPublisher


ALLOWED_STATUSES = {"approved", "rejected"}


def _validate_transaction(data):
    required = ("account_id", "amount", "currency")
    missing = [field for field in required if field not in data]
    if missing:
        return f"Missing fields: {', '.join(missing)}"
    try:
        amount = float(data["amount"])
    except (TypeError, ValueError):
        return "Amount must be a number"
    if amount <= 0 or amount > 1_000_000:
        return "Amount must be between 0 and 1,000,000"
    currency = str(data["currency"])
    if len(currency) != 3 or not currency.isalpha() or not currency.isupper():
        return "Currency must be a three-letter uppercase code"
    if not str(data["account_id"]).strip():
        return "Account ID is required"
    return None


def create_app(publisher=None):
    """Create an isolated Flask app suitable for local use and testing."""
    app = Flask(__name__)
    app.config["TRANSACTIONS"] = []
    app.config["PUBLISHER"] = publisher

    @app.after_request
    def add_request_id(response):
        response.headers["X-Request-ID"] = request.headers.get(
            "X-Request-ID", str(uuid.uuid4())
        )
        return response

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    @app.post("/transactions")
    def create_transaction():
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify({"error": "A JSON request body is required"}), 400
        error = _validate_transaction(data)
        if error:
            return jsonify({"error": error}), 400

        transaction = {
            "id": str(uuid.uuid4()),
            "account_id": str(data["account_id"]),
            "amount": float(data["amount"]),
            "currency": str(data["currency"]),
            "description": str(data.get("description", "")),
            "status": "pending",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        app.config["TRANSACTIONS"].append(transaction)
        if app.config["PUBLISHER"]:
            app.config["PUBLISHER"].publish(transaction)
        return jsonify(transaction), 201

    @app.get("/transactions")
    def list_transactions():
        account_id = request.args.get("account_id")
        transactions = app.config["TRANSACTIONS"]
        if account_id:
            transactions = [
                item for item in transactions if item["account_id"] == account_id
            ]
        return jsonify(transactions)

    @app.get("/transactions/<transaction_id>")
    def get_transaction(transaction_id):
        transaction = next(
            (
                item
                for item in app.config["TRANSACTIONS"]
                if item["id"] == transaction_id
            ),
            None,
        )
        if transaction is None:
            return jsonify({"error": "Transaction not found"}), 404
        return jsonify(transaction)

    @app.patch("/transactions/<transaction_id>/status")
    def update_status(transaction_id):
        data = request.get_json(silent=True) or {}
        if data.get("status") not in ALLOWED_STATUSES:
            return jsonify({"error": "Status must be approved or rejected"}), 400
        transaction = next(
            (
                item
                for item in app.config["TRANSACTIONS"]
                if item["id"] == transaction_id
            ),
            None,
        )
        if transaction is None:
            return jsonify({"error": "Transaction not found"}), 404
        transaction["status"] = data["status"]
        return jsonify(transaction)

    return app


def _publisher_from_environment():
    queue_url = os.environ.get("PAYMENT_QUEUE_URL")
    if not queue_url:
        return None
    import boto3

    return PaymentPublisher(
        boto3.client("sqs", region_name=os.environ.get("AWS_REGION", "af-south-1")),
        queue_url,
    )


app = create_app(_publisher_from_environment())


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
