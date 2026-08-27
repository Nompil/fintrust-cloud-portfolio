# Week 4: Databases and Transaction Pipelines

This folder contains the portfolio work for the supplied Week 4 Days 1 to 3 sessions. It covers AWS database selection, custom Python exceptions, debugging and a three-phase CSV to SQLite pipeline.

## Portfolio work

| File | Evidence |
| --- | --- |
| [Database decisions](database-decisions.md) | RDS, Aurora, DynamoDB and purpose-built database choices |
| [Database architecture](diagrams/fintrust_database_architecture.pdf) | Source-backed FinTrust database design for Days 1 to 3 |
| [Custom exceptions](python/transactions.py) | Banking exception hierarchy and transaction validation |
| [Debugging exercise](python/debug_me.py) | Corrected payment processor with all five lab bugs fixed |
| [Three-phase pipeline](pipeline.py) | CSV validation, SQLite loading and daily reporting |
| [Daily report](daily_report.txt) | Summary, type and status breakdowns, and the three largest transactions |
| [Validation tests](test_week04.py) | Repeatable checks for the supplied data and Python exercises |
| [Reflection](reflection.md) | SQLite concurrency compared with RDS Multi-AZ |

## Run the work

The Week 4 code uses only the Python standard library.

```powershell
python week04\python\transactions.py
python week04\python\debug_me.py
python week04\pipeline.py
python week04\test_week04.py
```

The pipeline reads ten source rows, rejects the two invalid amounts and loads eight rows. Running it again skips the existing transaction IDs instead of creating duplicates. The SQLite database is a local runtime file and remains excluded by `.gitignore`.
