"""Read Application Migration Service source server readiness."""

from __future__ import annotations

from typing import Any

from ..utils.sessions import get_client


def list_source_servers(mgn_client: Any | None = None) -> list[dict[str, Any]]:
    """Return all MGN source servers with replication and launch state."""
    client = mgn_client or get_client("mgn")
    request = {}
    servers = []
    while True:
        response = client.describe_source_servers(**request)
        for item in response.get("items", []):
            data = item.get("dataReplicationInfo", {})
            launch = item.get("lifeCycle", {})
            servers.append(
                {
                    "source_server_id": item["sourceServerID"],
                    "hostname": item.get("sourceProperties", {}).get("identificationHints", {}).get("hostname"),
                    "replication_state": data.get("dataReplicationState", "UNKNOWN"),
                    "lag_seconds": data.get("lagDuration"),
                    "lifecycle_state": launch.get("state", "UNKNOWN"),
                }
            )
        token = response.get("nextToken")
        if not token:
            break
        request["nextToken"] = token
    return servers
