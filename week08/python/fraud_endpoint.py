"""Invoke the FinTrust SageMaker fraud endpoint."""

from __future__ import annotations

import json
from typing import Any, Iterable


def classify_probability(probability: float) -> str:
    if not 0 <= probability <= 1:
        raise ValueError("Fraud probability must be between 0 and 1")
    if probability < 0.3:
        return "ACCEPT"
    if probability <= 0.7:
        return "REVIEW"
    return "REJECT"


def invoke_fraud_endpoint(
    sagemaker_runtime: Any,
    endpoint_name: str,
    features: Iterable[float],
) -> dict[str, Any]:
    values = [float(value) for value in features]
    if len(values) != 28:
        raise ValueError("The FinTrust model expects 28 feature values")
    body = ",".join(str(value) for value in values).encode("utf-8")
    response = sagemaker_runtime.invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType="text/csv",
        Accept="application/json",
        Body=body,
    )
    payload = json.loads(response["Body"].read().decode("utf-8"))
    if isinstance(payload, list):
        probability = float(payload[0])
    elif isinstance(payload, dict):
        probability = float(payload.get("fraud_probability", payload.get("score")))
    else:
        probability = float(payload)
    return {
        "fraud_probability": round(probability, 6),
        "decision": classify_probability(probability),
    }
