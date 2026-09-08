"""Classify EC2 instances using FinTrust migration tags."""

from __future__ import annotations

from typing import Any

from ..utils.sessions import get_client


VALID_STRATEGIES = (
    "refactor",
    "rehost",
    "replatform",
    "repurchase",
    "retain",
    "retire",
)


def _get_tag(tags: list[dict[str, str]] | None, key: str) -> str | None:
    for tag in tags or []:
        if tag.get("Key") == key:
            return tag.get("Value")
    return None


def classify_instances(
    ec2_client: Any | None = None,
    tag_prefix: str = "migration",
) -> tuple[dict[str, list[dict[str, str]]], list[dict[str, str]]]:
    """Return classified and unresolved instances from every API page."""
    client = ec2_client or get_client("ec2")
    portfolio = {strategy: [] for strategy in VALID_STRATEGIES}
    unresolved = []
    paginator = client.get_paginator("describe_instances")
    for page in paginator.paginate():
        for reservation in page.get("Reservations", []):
            for instance in reservation.get("Instances", []):
                tags = instance.get("Tags", [])
                raw_strategy = _get_tag(tags, f"{tag_prefix}:strategy")
                strategy = raw_strategy.lower() if raw_strategy else None
                entry = {
                    "id": instance["InstanceId"],
                    "name": _get_tag(tags, "Name") or instance["InstanceId"],
                    "type": instance["InstanceType"],
                    "state": instance["State"]["Name"],
                    "wave": _get_tag(tags, f"{tag_prefix}:wave") or "unassigned",
                    "strategy": strategy or "unassigned",
                }
                if strategy in portfolio:
                    portfolio[strategy].append(entry)
                else:
                    unresolved.append(entry)
    return portfolio, unresolved


def get_migration_wave(
    wave_number: int,
    ec2_client: Any | None = None,
) -> list[dict[str, str]]:
    """Return all classified instances assigned to one migration wave."""
    if wave_number not in {1, 2, 3}:
        raise ValueError("Migration wave must be 1, 2 or 3")
    portfolio, _ = classify_instances(ec2_client=ec2_client)
    return [
        instance
        for instances in portfolio.values()
        for instance in instances
        if instance["wave"] == str(wave_number)
    ]
