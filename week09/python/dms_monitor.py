"""Read DMS task and table progress without changing the migration."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any


TERMINAL_STATES = {"stopped", "failed", "deleting"}


@dataclass(frozen=True)
class TaskProgress:
    task_id: str
    status: str
    tables_loaded: int
    tables_loading: int
    tables_errored: int
    tables_queued: int
    full_load_percent: int
    elapsed_seconds: int
    start_time: str | None

    @property
    def terminal(self) -> bool:
        return self.status in TERMINAL_STATES


def get_task_progress(dms_client: Any, task_arn: str) -> TaskProgress | None:
    """Return the current summary for one replication task."""
    response = dms_client.describe_replication_tasks(
        Filters=[{"Name": "replication-task-arn", "Values": [task_arn]}]
    )
    tasks = response.get("ReplicationTasks", [])
    if not tasks:
        return None
    task = tasks[0]
    stats = task.get("ReplicationTaskStats", {})
    started = task.get("ReplicationTaskStartDate")
    if isinstance(started, datetime):
        started = started.astimezone(timezone.utc).isoformat()
    return TaskProgress(
        task_id=task["ReplicationTaskIdentifier"],
        status=task["Status"],
        tables_loaded=stats.get("TablesLoaded", 0),
        tables_loading=stats.get("TablesLoading", 0),
        tables_errored=stats.get("TablesErrored", 0),
        tables_queued=stats.get("TablesQueued", 0),
        full_load_percent=stats.get("FullLoadProgressPercent", 0),
        elapsed_seconds=stats.get("ElapsedTimeMillis", 0) // 1000,
        start_time=started,
    )


def get_table_statistics(dms_client: Any, task_arn: str) -> list[dict[str, Any]]:
    """Collect all DMS table statistics pages."""
    request = {"ReplicationTaskArn": task_arn, "MaxRecords": 100}
    rows = []
    while True:
        response = dms_client.describe_table_statistics(**request)
        rows.extend(response.get("TableStatistics", []))
        marker = response.get("Marker")
        if not marker:
            break
        request["Marker"] = marker
    return rows


def task_health(dms_client: Any, task_arn: str) -> dict[str, Any]:
    """Build one EventBridge friendly monitoring result."""
    progress = get_task_progress(dms_client, task_arn)
    if progress is None:
        return {"task_found": False, "alert": True, "reason": "Task not found"}
    tables = get_table_statistics(dms_client, task_arn)
    full_load_errors = sum(row.get("FullLoadErrorRows", 0) for row in tables)
    validation_errors = sum(row.get("ValidationFailedRecords", 0) for row in tables)
    alert = progress.status == "failed" or progress.tables_errored > 0 or full_load_errors > 0 or validation_errors > 0
    return {
        "task_found": True,
        "progress": asdict(progress),
        "table_count": len(tables),
        "full_load_error_rows": full_load_errors,
        "validation_failed_records": validation_errors,
        "alert": alert,
    }
