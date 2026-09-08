"""Event driven migration orchestration without long running Lambda polls."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any

from .ec2.classifier import classify_instances
from .rds.dms_helpers import is_cutover_ready, start_task
from .s3.sync_helpers import get_execution_status, start_task_execution
from .utils.sessions import get_client


def classify_and_start(wave: int) -> dict[str, Any]:
    """Mark Rehost instances in progress and resume the wave DMS task."""
    ec2 = get_client("ec2")
    portfolio, unresolved = classify_instances(ec2)
    instances = [item for item in portfolio["rehost"] if item["wave"] == str(wave)]
    if instances:
        ec2.create_tags(
            Resources=[item["id"] for item in instances],
            Tags=[{"Key": "migration:status", "Value": "in-progress"}],
        )
    task_arn = os.getenv("DMS_TASK_ARN")
    if not task_arn:
        raise RuntimeError("DMS_TASK_ARN is required")
    start_task(task_arn, wait=False)
    return {
        "wave": wave,
        "rehost_instances_started": len(instances),
        "unresolved_instances": len(unresolved),
        "next_action": "check_cutover",
    }


def check_cutover() -> dict[str, Any]:
    """Return the current cutover gate result for a later scheduled invocation."""
    settings = {
        "task_arn": os.getenv("DMS_TASK_ARN"),
        "replication_instance_id": os.getenv("DMS_REPLICATION_INSTANCE_ID"),
        "task_identifier": os.getenv("DMS_TASK_IDENTIFIER"),
    }
    missing = [name for name, value in settings.items() if not value]
    if missing:
        raise RuntimeError(f"Missing configuration: {', '.join(missing)}")
    ready, details = is_cutover_ready(**settings)
    return {
        "ready": ready,
        "next_action": "final_sync" if ready else "check_cutover",
        "details": details,
    }


def final_sync(execution_arn: str | None = None) -> dict[str, Any]:
    """Start or check the final DataSync execution and record a successful result."""
    task_arn = os.getenv("DATASYNC_TASK_ARN")
    report_bucket = os.getenv("MIGRATION_REPORT_BUCKET")
    if not task_arn or not report_bucket:
        raise RuntimeError("DATASYNC_TASK_ARN and MIGRATION_REPORT_BUCKET are required")
    if not execution_arn:
        started = start_task_execution(task_arn)
        return {"status": "STARTED", "execution_arn": started, "next_action": "final_sync"}

    result = get_execution_status(execution_arn)
    if result["status"] not in {"SUCCESS", "ERROR"}:
        return {"status": result["status"], "execution_arn": execution_arn, "next_action": "final_sync"}
    if result["status"] == "ERROR" or result["files_failed"]:
        return {"status": "ERROR", "execution_arn": execution_arn, "details": result}

    completed = datetime.now(timezone.utc)
    key = f"cutovers/{completed:%Y-%m-%d}/{execution_arn.rsplit('/', 1)[-1]}.json"
    get_client("s3").put_object(
        Bucket=report_bucket,
        Key=key,
        Body=json.dumps({"completed_at": completed.isoformat(), "result": result}).encode("utf-8"),
        ContentType="application/json",
        ServerSideEncryption="AES256",
    )
    return {"status": "SUCCESS", "execution_arn": execution_arn, "report_key": key}


def lambda_handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    """Route one short migration action per Lambda invocation."""
    del context
    action = event.get("action")
    if action == "classify_and_start":
        return classify_and_start(int(event.get("wave", 1)))
    if action == "check_cutover":
        return check_cutover()
    if action == "final_sync":
        return final_sync(event.get("execution_arn"))
    raise ValueError(f"Unknown migration action: {action}")
