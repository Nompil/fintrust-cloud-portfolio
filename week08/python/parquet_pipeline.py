"""Convert FinTrust transaction CSV data into date-partitioned Parquet."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import boto3
import pandas as pd


REQUIRED_COLUMNS = {
    "transaction_id",
    "account_id",
    "amount",
    "currency",
    "timestamp",
    "status",
    "region",
}


def load_transactions(csv_path: str | Path) -> pd.DataFrame:
    data = pd.read_csv(csv_path)
    missing = REQUIRED_COLUMNS.difference(data.columns)
    if missing:
        raise ValueError(f"CSV is missing columns: {', '.join(sorted(missing))}")
    data["amount"] = pd.to_numeric(data["amount"], errors="raise")
    data["timestamp"] = pd.to_datetime(data["timestamp"], errors="raise")
    if data["transaction_id"].duplicated().any():
        raise ValueError("transaction_id values must be unique")
    if (data["amount"] <= 0).any():
        raise ValueError("amount values must be positive")
    return data


def prepare_transactions(data: pd.DataFrame) -> pd.DataFrame:
    prepared = data.copy()
    prepared["currency"] = prepared["currency"].str.upper()
    prepared["status"] = prepared["status"].str.upper()
    prepared["year"] = prepared["timestamp"].dt.year.astype(str)
    prepared["month"] = prepared["timestamp"].dt.month.astype(str).str.zfill(2)
    prepared["is_high_value"] = prepared["amount"] > 50_000
    return prepared


def write_partitions(data: pd.DataFrame, output_root: str | Path) -> list[Path]:
    root = Path(output_root)
    written: list[Path] = []
    for (year, month), group in data.groupby(["year", "month"], sort=True):
        destination = root / f"year={year}" / f"month={month}" / "transactions.parquet"
        destination.parent.mkdir(parents=True, exist_ok=True)
        group.drop(columns=["year", "month"]).to_parquet(
            destination,
            engine="pyarrow",
            compression="snappy",
            index=False,
        )
        written.append(destination)
    return written


def upload_partitions(
    files: list[Path],
    output_root: str | Path,
    bucket: str,
    *,
    prefix: str = "transactions",
    s3_client: Any | None = None,
) -> list[str]:
    s3 = s3_client or boto3.client("s3", region_name="af-south-1")
    root = Path(output_root)
    keys: list[str] = []
    for file_path in files:
        relative = file_path.relative_to(root).as_posix()
        key = f"{prefix.strip('/')}/{relative}"
        s3.upload_file(str(file_path), bucket, key)
        keys.append(key)
    return keys


def summarise(data: pd.DataFrame) -> dict[str, Any]:
    return {
        "rows": int(len(data)),
        "high_value": int(data["is_high_value"].sum()),
        "total_by_currency": {
            currency: round(float(total), 2)
            for currency, total in data.groupby("currency")["amount"].sum().items()
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build FinTrust Parquet partitions")
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("output_root", type=Path)
    args = parser.parse_args()

    prepared = prepare_transactions(load_transactions(args.csv_path))
    files = write_partitions(prepared, args.output_root)
    summary = summarise(prepared)
    print(f"Processed {summary['rows']} transactions across {len(files)} partition(s).")
    for file_path in files:
        print(f"Written: {file_path}")


if __name__ == "__main__":
    main()
