"""Lazy boto3 session creation for the FinTrust migration package."""

from __future__ import annotations

import os
from typing import Any, Callable

import boto3


_sessions: dict[tuple[str, str | None], boto3.Session] = {}


def get_session(region: str | None = None, profile: str | None = None) -> boto3.Session:
    """Return a cached session without making a network call during import."""
    selected_region = region or os.getenv("AWS_DEFAULT_REGION", "af-south-1")
    selected_profile = profile if profile is not None else os.getenv("AWS_PROFILE")
    key = (selected_region, selected_profile)
    if key not in _sessions:
        kwargs: dict[str, str] = {"region_name": selected_region}
        if selected_profile:
            kwargs["profile_name"] = selected_profile
        _sessions[key] = boto3.Session(**kwargs)
    return _sessions[key]


def get_client(service: str, region: str | None = None) -> Any:
    """Return a client from the shared regional session."""
    return get_session(region=region).client(service)


def get_resource(service: str, region: str | None = None) -> Any:
    """Return a resource from the shared regional session."""
    return get_session(region=region).resource(service)


def get_cross_account_session(
    role_arn: str,
    session_name: str = "fintrust-migration",
    external_id: str | None = None,
    base_session: Any | None = None,
    session_factory: Callable[..., Any] = boto3.Session,
) -> Any:
    """Assume a migration role and return a short lived boto3 session."""
    source = base_session or get_session()
    request = {"RoleArn": role_arn, "RoleSessionName": session_name}
    if external_id:
        request["ExternalId"] = external_id
    response = source.client("sts").assume_role(**request)
    credentials = response["Credentials"]
    return session_factory(
        aws_access_key_id=credentials["AccessKeyId"],
        aws_secret_access_key=credentials["SecretAccessKey"],
        aws_session_token=credentials["SessionToken"],
        region_name=source.region_name,
    )


def clear_session_cache() -> None:
    """Clear cached sessions for isolated local tests."""
    _sessions.clear()
