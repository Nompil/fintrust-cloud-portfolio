"""Run FinTrust Athena reports and inspect the Glue catalog."""

from __future__ import annotations

import argparse
import csv
import re
import time
from pathlib import Path
from typing import Any

import boto3


TERMINAL_STATES = {"SUCCEEDED", "FAILED", "CANCELLED"}
REPORT_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*$")


def rows_to_table(rows: list[dict[str, Any]]) -> tuple[list[str], list[list[str]]]:
    """Convert Athena Row objects into a header and ordinary string rows."""
    if not rows:
        return [], []

    header = [cell.get("VarCharValue", "") for cell in rows[0].get("Data", [])]
    records: list[list[str]] = []
    for row in rows[1:]:
        values = [cell.get("VarCharValue", "") for cell in row.get("Data", [])]
        values.extend([""] * (len(header) - len(values)))
        records.append(values[: len(header)])
    return header, records


class FinTrustComplianceReporter:
    """Submit Athena queries, wait for completion, and save CSV reports."""

    def __init__(
        self,
        database: str,
        output_bucket: str,
        region: str = "af-south-1",
        *,
        athena_client: Any | None = None,
        s3_client: Any | None = None,
        poll_seconds: float = 1.0,
        max_polls: int = 300,
    ) -> None:
        self.database = database
        self.output_bucket = output_bucket.removeprefix("s3://").rstrip("/")
        self.region = region
        self.athena = athena_client or boto3.client("athena", region_name=region)
        self.s3 = s3_client or boto3.client("s3", region_name=region)
        self.poll_seconds = poll_seconds
        self.max_polls = max_polls

    def _wait_for_query(self, query_id: str) -> None:
        for _ in range(self.max_polls):
            response = self.athena.get_query_execution(QueryExecutionId=query_id)
            status = response["QueryExecution"]["Status"]
            state = status["State"]
            if state in TERMINAL_STATES:
                if state != "SUCCEEDED":
                    reason = status.get("StateChangeReason", "No reason returned")
                    raise RuntimeError(f"Athena query {state.lower()}: {reason}")
                return
            time.sleep(self.poll_seconds)
        raise TimeoutError(f"Athena query did not finish after {self.max_polls} checks")

    def _get_rows(self, query_id: str) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        token: str | None = None
        while True:
            request: dict[str, Any] = {"QueryExecutionId": query_id}
            if token:
                request["NextToken"] = token
            response = self.athena.get_query_results(**request)
            page_rows = response["ResultSet"].get("Rows", [])
            if token and page_rows:
                page_rows = page_rows[1:] if page_rows[0] == rows[0] else page_rows
            rows.extend(page_rows)
            token = response.get("NextToken")
            if not token:
                return rows

    def run_report(self, report_name: str, sql: str, output_dir: str | Path = ".") -> int:
        if not REPORT_NAME.fullmatch(report_name):
            raise ValueError("Report name may contain only letters, numbers, underscores, and hyphens")

        response = self.athena.start_query_execution(
            QueryString=sql,
            QueryExecutionContext={"Database": self.database},
            ResultConfiguration={
                "OutputLocation": f"s3://{self.output_bucket}/athena-results/"
            },
        )
        query_id = response["QueryExecutionId"]
        self._wait_for_query(query_id)
        header, records = rows_to_table(self._get_rows(query_id))

        destination = Path(output_dir) / f"{report_name}.csv"
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("w", newline="", encoding="utf-8") as report_file:
            writer = csv.writer(report_file)
            writer.writerow(header)
            writer.writerows(records)

        print(f"Report '{report_name}' complete: {len(records)} rows written to {destination}.")
        return len(records)

    def save_to_s3(self, bucket: str, key: str, local_path: str | Path) -> None:
        self.s3.upload_file(str(local_path), bucket, key)


def list_glue_tables(
    database: str,
    region: str = "af-south-1",
    *,
    glue_client: Any | None = None,
) -> list[dict[str, Any]]:
    """Return table names, locations, columns, and partition keys from Glue."""
    glue = glue_client or boto3.client("glue", region_name=region)
    tables: list[dict[str, Any]] = []
    token: str | None = None
    while True:
        request: dict[str, Any] = {"DatabaseName": database}
        if token:
            request["NextToken"] = token
        response = glue.get_tables(**request)
        for table in response.get("TableList", []):
            storage = table.get("StorageDescriptor", {})
            tables.append(
                {
                    "name": table["Name"],
                    "location": storage.get("Location", ""),
                    "columns": storage.get("Columns", []),
                    "partition_keys": table.get("PartitionKeys", []),
                }
            )
        token = response.get("NextToken")
        if not token:
            return tables


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a FinTrust Athena compliance report")
    parser.add_argument("report_name")
    parser.add_argument("sql_file", type=Path)
    parser.add_argument("--database", default="fintrust_curated")
    parser.add_argument("--output-bucket", required=True)
    parser.add_argument("--output-dir", type=Path, default=Path.cwd())
    args = parser.parse_args()

    reporter = FinTrustComplianceReporter(args.database, args.output_bucket)
    reporter.run_report(
        args.report_name,
        args.sql_file.read_text(encoding="utf-8"),
        args.output_dir,
    )


if __name__ == "__main__":
    main()
