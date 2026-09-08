"""Summarise recent FinTrust Fault Injection Service experiments."""

from __future__ import annotations

from datetime import datetime
from typing import Any


def format_start_time(value: Any) -> str:
    if isinstance(value, datetime):
        return value.strftime("%H:%M %Y-%m-%d")
    return "not started" if value is None else str(value)


def summarise_fis_experiments(fis_client: Any, max_results: int = 10) -> list[dict[str, str]]:
    """Return recent experiment state and the configured stop condition."""
    response = fis_client.list_experiments(maxResults=max_results)
    results = []
    for item in response.get("experiments", [])[:max_results]:
        detail = fis_client.get_experiment(id=item["id"])["experiment"]
        conditions = detail.get("stopConditions", [])
        results.append(
            {
                "experiment_id": item["id"][-16:],
                "template_id": detail.get("experimentTemplateId", "unknown"),
                "state": detail.get("state", {}).get("status", "unknown"),
                "start_time": format_start_time(detail.get("startTime")),
                "stop_condition": conditions[0].get("value", "none") if conditions else "none",
            }
        )
    return results
