"""Index FinTrust security events into Amazon OpenSearch Service."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import boto3
from opensearchpy import AWSV4SignerAuth, OpenSearch, RequestsHttpConnection


def build_opensearch_client(endpoint: str, region: str = "af-south-1") -> OpenSearch:
    credentials = boto3.Session().get_credentials()
    if credentials is None:
        raise RuntimeError("AWS credentials are required to sign OpenSearch requests")
    auth = AWSV4SignerAuth(credentials, region, "es")
    return OpenSearch(
        hosts=[{"host": endpoint.removeprefix("https://").rstrip("/"), "port": 443}],
        http_auth=auth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection,
    )


def index_security_event(
    client: Any,
    event: dict[str, Any],
    *,
    recorded_at: datetime | None = None,
) -> dict[str, Any]:
    if "event_type" not in event or "risk_score" not in event:
        raise ValueError("Security event requires event_type and risk_score")
    timestamp = recorded_at or datetime.now(timezone.utc)
    document = {**event, "timestamp": event.get("timestamp", timestamp.isoformat())}
    index_name = f"fintrust-security-{timestamp:%Y-%m}"
    response = client.index(index=index_name, body=document)
    return {"index": index_name, "document_id": response["_id"]}


def find_high_risk_events(client: Any, index_pattern: str, minimum_score: int = 80) -> list[dict[str, Any]]:
    query = {"query": {"range": {"risk_score": {"gte": minimum_score}}}}
    response = client.search(index=index_pattern, body=query)
    return [hit["_source"] for hit in response.get("hits", {}).get("hits", [])]
