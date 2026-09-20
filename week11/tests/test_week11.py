from __future__ import annotations

import logging
import unittest
from pathlib import Path
from unittest.mock import patch

from week11.python.pipeline_resilience import (
    benchmark_metadata_fetch,
    fetch_object_metadata_parallel,
    get_s3_object_metadata,
    log_call,
    memoize,
    retry,
)


ROOT = Path(__file__).resolve().parents[2]


class TemporaryError(Exception):
    pass


class FakeS3:
    def __init__(self, responses: dict[str, list[object]]):
        self.responses = {key: list(value) for key, value in responses.items()}
        self.calls: list[tuple[str, str]] = []

    def head_object(self, *, Bucket: str, Key: str):
        self.calls.append((Bucket, Key))
        response = self.responses[Key].pop(0)
        if isinstance(response, Exception):
            raise response
        return response


class Clock:
    def __init__(self, values: list[float]):
        self.values = iter(values)

    def __call__(self) -> float:
        return next(self.values)


class WeekElevenTests(unittest.TestCase):
    def test_retry_returns_after_transient_failure(self):
        attempts = []
        waits = []

        @retry(max_attempts=3, delay_seconds=0.5, retry_on=(TemporaryError,), sleep=waits.append)
        def fetch():
            attempts.append("call")
            if len(attempts) < 3:
                raise TemporaryError("temporarily unavailable")
            return "ready"

        self.assertEqual(fetch(), "ready")
        self.assertEqual(len(attempts), 3)
        self.assertEqual(waits, [0.5, 1.0])

    def test_retry_raises_the_final_error(self):
        @retry(max_attempts=2, delay_seconds=0, retry_on=(TemporaryError,), sleep=lambda _: None)
        def fetch():
            raise TemporaryError("still unavailable")

        with self.assertRaisesRegex(TemporaryError, "still unavailable"):
            fetch()

    def test_retry_rejects_invalid_configuration(self):
        with self.assertRaises(ValueError):
            retry(max_attempts=0)
        with self.assertRaises(ValueError):
            retry(delay_seconds=-1)
        with self.assertRaises(ValueError):
            retry(retry_on=())

    def test_decorator_preserves_function_name(self):
        @retry(max_attempts=1)
        def named_function():
            return "ok"

        self.assertEqual(named_function.__name__, "named_function")

    def test_metadata_fetch_retries_throttled_call(self):
        client = FakeS3(
            {
                "daily.csv": [
                    TemporaryError("throttled"),
                    {"ContentLength": 12, "ETag": "etag-1", "LastModified": "2026-09-20"},
                ]
            }
        )
        with patch("week11.python.pipeline_resilience.time.sleep"):
            result = get_s3_object_metadata(client, "fintrust-raw", "daily.csv")
        self.assertEqual(result["size_bytes"], 12)
        self.assertEqual(len(client.calls), 2)

    def test_parallel_fetch_returns_successes_and_errors(self):
        client = FakeS3(
            {
                "one.csv": [{"ContentLength": 1}],
                "two.csv": [ValueError("not found"), ValueError("not found"), ValueError("not found")],
            }
        )
        with patch("week11.python.pipeline_resilience.time.sleep"):
            result = fetch_object_metadata_parallel(
                "fintrust-raw", ["one.csv", "two.csv"], client, max_workers=2
            )
        self.assertEqual(result["objects"][0]["key"], "one.csv")
        self.assertIn("two.csv", result["errors"])

    def test_parallel_fetch_validates_worker_limit(self):
        client = FakeS3({})
        with self.assertRaises(ValueError):
            fetch_object_metadata_parallel("bucket", [], client, max_workers=0)
        with self.assertRaises(ValueError):
            fetch_object_metadata_parallel("bucket", [], client, max_workers=51)

    def test_memoize_runs_function_once_for_matching_arguments(self):
        calls = []

        @memoize
        def calculate(value, multiplier=1):
            calls.append(value)
            return value * multiplier

        self.assertEqual(calculate(4, multiplier=2), 8)
        self.assertEqual(calculate(4, multiplier=2), 8)
        self.assertEqual(calls, [4])

    def test_log_call_preserves_result_and_writes_log(self):
        logger = logging.getLogger("week11.test")

        @log_call(logger=logger)
        def add(left, right):
            return left + right

        with self.assertLogs("week11.test", level="INFO") as captured:
            self.assertEqual(add(2, 3), 5)
        self.assertIn("Calling add", captured.output[0])
        self.assertIn("add returned 5", captured.output[1])

    def test_benchmark_uses_measured_clock_values(self):
        calls = []

        def fetch(bucket, key):
            calls.append((bucket, key))
            return {"key": key}

        result = benchmark_metadata_fetch(
            "fintrust-raw",
            ["one", "two"],
            fetch,
            max_workers=2,
            clock=Clock([0, 8, 10, 12]),
        )
        self.assertEqual(result.sequential_seconds, 8)
        self.assertEqual(result.concurrent_seconds, 2)
        self.assertEqual(result.speedup, 4)
        self.assertEqual(len(calls), 4)

    def test_empty_benchmark_has_no_speedup_claim(self):
        result = benchmark_metadata_fetch("fintrust-raw", [], lambda *_: None)
        self.assertEqual(result.object_count, 0)
        self.assertIsNone(result.speedup)

    def test_sql_includes_required_window_and_cte_patterns(self):
        sql = (ROOT / "week11" / "sql" / "fintrust_window_cte_queries.sql").read_text(encoding="utf-8")
        self.assertIn("ROW_NUMBER() OVER", sql)
        self.assertIn("DENSE_RANK() OVER", sql)
        self.assertIn("LAG(monthly_amount)", sql)
        self.assertIn("WITH monthly_totals AS", sql)
        self.assertIn("monthly_history AS", sql)
        self.assertIn("growth_alerts AS", sql)
        self.assertIn("NTILE(4) OVER", sql)

    def test_waf_mapping_names_each_pillar(self):
        mapping = (ROOT / "week11" / "notes" / "waf-pillar-mapping.md").read_text(encoding="utf-8")
        for pillar in (
            "Operational Excellence",
            "Security",
            "Reliability",
            "Performance Efficiency",
            "Cost Optimisation",
            "Sustainability",
        ):
            self.assertIn(pillar, mapping)


if __name__ == "__main__":
    unittest.main()
