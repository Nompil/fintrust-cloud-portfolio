"""Retry, logging and concurrent S3 metadata helpers for Week 11.

The functions accept an already-created boto3 client. They do not create a client,
read credentials or contact AWS during import.
"""

from __future__ import annotations

import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from functools import wraps
from typing import Any, Callable, ParamSpec, TypeVar


P = ParamSpec("P")
T = TypeVar("T")
LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class MetadataBenchmark:
    """Measured metadata collection timings from one local run."""

    sequential_seconds: float
    concurrent_seconds: float
    speedup: float | None
    object_count: int


def retry(
    max_attempts: int = 3,
    delay_seconds: float = 1.0,
    retry_on: tuple[type[BaseException], ...] = (Exception,),
    sleep: Callable[[float], None] | None = None,
    logger: logging.Logger | None = None,
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """Retry selected transient errors with exponential backoff.

    The final failure is raised unchanged. Callers should choose `retry_on` narrowly
    when an operation can also raise permanent business validation errors.
    """
    if max_attempts < 1:
        raise ValueError("max_attempts must be at least 1")
    if delay_seconds < 0:
        raise ValueError("delay_seconds cannot be negative")
    if not retry_on:
        raise ValueError("retry_on must contain at least one exception type")

    active_logger = logger or LOGGER

    def decorate(function: Callable[P, T]) -> Callable[P, T]:
        @wraps(function)
        def wrapped(*args: P.args, **kwargs: P.kwargs) -> T:
            for attempt in range(1, max_attempts + 1):
                try:
                    return function(*args, **kwargs)
                except retry_on as error:
                    if attempt == max_attempts:
                        raise
                    wait_seconds = delay_seconds * (2 ** (attempt - 1))
                    active_logger.warning(
                        "%s failed on attempt %s of %s: %s. Retrying in %.2f seconds.",
                        function.__name__,
                        attempt,
                        max_attempts,
                        error,
                        wait_seconds,
                    )
                    (sleep or time.sleep)(wait_seconds)
            raise RuntimeError("Retry loop ended unexpectedly")

        return wrapped

    return decorate


def log_call(
    function: Callable[P, T] | None = None,
    *,
    logger: logging.Logger | None = None,
) -> Callable[[Callable[P, T]], Callable[P, T]] | Callable[P, T]:
    """Log the call and result of a function.

    Do not use this decorator around functions that receive credentials, tokens or
    personal data because those values would enter the application log.
    """
    active_logger = logger or LOGGER

    def decorate(target: Callable[P, T]) -> Callable[P, T]:
        @wraps(target)
        def wrapped(*args: P.args, **kwargs: P.kwargs) -> T:
            active_logger.info("Calling %s with args=%r kwargs=%r", target.__name__, args, kwargs)
            result = target(*args, **kwargs)
            active_logger.info("%s returned %r", target.__name__, result)
            return result

        return wrapped

    return decorate if function is None else decorate(function)


def memoize(function: Callable[P, T]) -> Callable[P, T]:
    """Cache results for functions whose arguments are hashable."""
    cache: dict[tuple[tuple[Any, ...], tuple[tuple[str, Any], ...]], T] = {}

    @wraps(function)
    def wrapped(*args: P.args, **kwargs: P.kwargs) -> T:
        key = (args, tuple(sorted(kwargs.items())))
        if key not in cache:
            cache[key] = function(*args, **kwargs)
        return cache[key]

    return wrapped


def timer(function: Callable[P, T]) -> Callable[P, T]:
    """Log elapsed wall-clock time after a function completes."""
    @wraps(function)
    def wrapped(*args: P.args, **kwargs: P.kwargs) -> T:
        started = time.perf_counter()
        result = function(*args, **kwargs)
        LOGGER.info("%s completed in %.3f seconds", function.__name__, time.perf_counter() - started)
        return result

    return wrapped


@retry(max_attempts=3, delay_seconds=1.0)
def get_s3_object_metadata(s3_client: Any, bucket: str, key: str) -> dict[str, Any]:
    """Read metadata for one S3 object through the supplied boto3-compatible client."""
    response = s3_client.head_object(Bucket=bucket, Key=key)
    return {
        "key": key,
        "size_bytes": response["ContentLength"],
        "etag": response.get("ETag"),
        "last_modified": response.get("LastModified"),
    }


def fetch_object_metadata_parallel(
    bucket: str,
    keys: list[str],
    s3_client: Any,
    max_workers: int = 16,
) -> dict[str, Any]:
    """Collect S3 object metadata concurrently and retain individual failures."""
    if not 1 <= max_workers <= 50:
        raise ValueError("max_workers must be between 1 and 50")

    results: list[dict[str, Any]] = []
    errors: dict[str, str] = {}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(get_s3_object_metadata, s3_client, bucket, key): key
            for key in keys
        }
        for future in as_completed(futures):
            key = futures[future]
            try:
                results.append(future.result())
            except Exception as error:
                errors[key] = str(error)

    return {"objects": results, "errors": errors}


def benchmark_metadata_fetch(
    bucket: str,
    keys: list[str],
    metadata_fetcher: Callable[[str, str], Any],
    max_workers: int = 16,
    clock: Callable[[], float] = time.perf_counter,
) -> MetadataBenchmark:
    """Measure sequential and threaded collection with the same metadata function."""
    if not keys:
        return MetadataBenchmark(0.0, 0.0, None, 0)
    if not 1 <= max_workers <= 50:
        raise ValueError("max_workers must be between 1 and 50")

    started = clock()
    for key in keys:
        metadata_fetcher(bucket, key)
    sequential_seconds = clock() - started

    started = clock()
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(metadata_fetcher, bucket, key) for key in keys]
        for future in as_completed(futures):
            future.result()
    concurrent_seconds = clock() - started

    speedup = sequential_seconds / concurrent_seconds if concurrent_seconds > 0 else None
    return MetadataBenchmark(sequential_seconds, concurrent_seconds, speedup, len(keys))
