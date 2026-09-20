# Week 11 Data Engineering Notes

## SQL choices

`ROW_NUMBER` assigns a unique ordered position, which makes it appropriate when exactly three rows per account are needed. `DENSE_RANK` gives tied amounts the same rank without gaps. The query file puts both values beside one another so the effect of an equal transaction amount is visible.

The anomaly query uses three named stages. `monthly_totals` aggregates the raw records, `monthly_history` adds the previous month with `LAG`, and `growth_alerts` calculates the percentage change. The final filter happens outside the window expression because PostgreSQL calculates window values after `WHERE`.

## Python choices

The retry decorator preserves the wrapped function's name and documentation with `functools.wraps`. It doubles the wait after each selected exception and re-raises the final error. In production, the exception list should be limited to transient problems such as throttling or temporary network failures. It should not repeatedly retry malformed input or a failed authorisation decision.

The S3 metadata helper takes a client as an argument. This makes it testable without credentials and lets the caller decide which session and Region are appropriate. The concurrent collector uses `ThreadPoolExecutor` because boto3 calls are I/O-bound. It retains individual errors rather than failing silently when one object cannot be read.

The benchmark returns only the timing measured in the local run. It does not include a claimed speedup in this portfolio because no benchmark output from the learner environment was supplied.
