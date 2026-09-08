"""Start, throttle and monitor FinTrust DataSync task executions."""

from __future__ import annotations

import os
import time
from typing import Any, Callable

from ..utils.sessions import get_client


TERMINAL_STATES = {"SUCCESS", "ERROR"}
MBPS_TO_BYTES_PER_SECOND = 1_000_000 / 8


def start_task_execution(task_arn: str, datasync_client: Any | None = None) -> str:
    """Start one DataSync execution and return its execution ARN."""
    client = datasync_client or get_client("datasync")
    response = client.start_task_execution(TaskArn=task_arn)
    return response["TaskExecutionArn"]


def get_execution_status(
    execution_arn: str,
    datasync_client: Any | None = None,
) -> dict[str, Any]:
    """Return the progress fields used by operations and audit reports."""
    client = datasync_client or get_client("datasync")
    response = client.describe_task_execution(TaskExecutionArn=execution_arn)
    result = response.get("Result", {})
    return {
        "execution_arn": execution_arn,
        "status": response["Status"],
        "files_transferred": response.get("FilesTransferred", 0),
        "bytes_transferred": response.get("BytesTransferred", 0),
        "files_verified": response.get("FilesVerified", 0),
        "files_failed": result.get("FilesTransferFailed", 0),
        "prepare_milliseconds": result.get("PrepareDuration", 0),
        "transfer_milliseconds": result.get("TransferDuration", 0),
        "verify_milliseconds": result.get("VerifyDuration", 0),
    }


def wait_for_execution(
    execution_arn: str,
    datasync_client: Any | None = None,
    timeout_seconds: int = 21_600,
    poll_seconds: int = 60,
    sleep: Callable[[float], None] = time.sleep,
    clock: Callable[[], float] = time.monotonic,
) -> dict[str, Any]:
    """Wait for a terminal execution state with an explicit timeout."""
    client = datasync_client or get_client("datasync")
    started = clock()
    while True:
        result = get_execution_status(execution_arn, client)
        if result["status"] in TERMINAL_STATES:
            return result
        if clock() - started >= timeout_seconds:
            raise TimeoutError(f"DataSync execution did not finish within {timeout_seconds} seconds")
        sleep(poll_seconds)


def set_task_throttle(
    task_arn: str,
    bandwidth_mbps: int,
    datasync_client: Any | None = None,
) -> int:
    """Set a validated DataSync bandwidth limit and return bytes per second."""
    if bandwidth_mbps < 0:
        raise ValueError("Bandwidth cannot be negative")
    bytes_per_second = int(bandwidth_mbps * MBPS_TO_BYTES_PER_SECOND) if bandwidth_mbps else 0
    client = datasync_client or get_client("datasync")
    client.update_task(TaskArn=task_arn, Options={"BytesPerSecond": bytes_per_second})
    return bytes_per_second


def lambda_handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    """Apply a daytime or overnight throttle from EventBridge Scheduler."""
    del context
    task_arn = os.getenv("DATASYNC_TASK_ARN")
    if not task_arn:
        raise RuntimeError("DATASYNC_TASK_ARN is required")
    mode = event.get("mode", "daytime")
    limits = {"daytime": 500, "overnight": 9000}
    if mode not in limits:
        raise ValueError(f"Unknown throttle mode: {mode}")
    bandwidth = limits[mode]
    applied = set_task_throttle(task_arn, bandwidth)
    return {"statusCode": 200, "mode": mode, "bandwidth_mbps": bandwidth, "bytes_per_second": applied}


def monitor_nightly_transfers(
    task_arns: list[str],
    datasync_client: Any | None = None,
    timeout_seconds: int = 21_600,
    poll_seconds: int = 60,
    sleep: Callable[[float], None] = time.sleep,
    clock: Callable[[], float] = time.monotonic,
) -> dict[str, dict[str, Any]]:
    """Start several tasks together and return their final execution results."""
    client = datasync_client or get_client("datasync")
    executions = [start_task_execution(task_arn, client) for task_arn in task_arns]
    pending = list(executions)
    final: dict[str, dict[str, Any]] = {}
    started = clock()
    while pending:
        for execution_arn in tuple(pending):
            info = get_execution_status(execution_arn, client)
            if info["status"] in TERMINAL_STATES:
                final[execution_arn] = info
                pending.remove(execution_arn)
        if not pending:
            break
        if clock() - started >= timeout_seconds:
            raise TimeoutError("Nightly DataSync tasks exceeded the monitoring window")
        sleep(poll_seconds)
    return final
