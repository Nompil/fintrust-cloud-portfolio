# Week 4: Databases and Transaction Pipelines

This folder contains the Week 4 portfolio work for AWS database selection, Python exceptions, debugging, packaging, data analysis and the three-phase CSV to SQLite pipeline.

## Portfolio work

| File | Evidence |
| --- | --- |
| [Seven-layer database design](db-architecture-diagram.md) | Required service, Region and selection reason for all seven database layers, plus the DMS migration path |
| [Database architecture PDF](diagrams/fintrust_database_architecture.pdf) | Detailed visual version of the seven-layer design |
| [Database decisions](database-decisions.md) | RDS, Aurora, DynamoDB, purpose-built databases, Redshift and DMS choices |
| [Custom exceptions](python/transactions.py) | Banking exception hierarchy and transaction validation |
| [Debugging exercise](python/debug_me.py) | Corrected payment processor with all five lab bugs fixed |
| [Original pipeline](pipeline.py) | Single-file CSV validation, SQLite loading and daily reporting |
| [Pipeline package](fintrust_pipeline/) | Loader, database and reporter modules created during the refactoring exercise |
| [Package entry point](main.py) | Runs the refactored pipeline from the repository root or Week 4 folder |
| [pandas analysis](analyse.py) | DataFrame filtering, grouping, enrichment and CSV export |
| [Pinned dependencies](requirements.txt) | Reproducible boto3 and pandas environment |
| [Daily report](daily_report.txt) | Summary, type and status breakdowns, and the three largest transactions |
| [Enriched transactions](transactions_enriched.csv) | Validated rows with the high-value flag and transaction date |
| [Validation tests](test_week04.py) | Repeatable checks for the supplied data and Python exercises |
| [Reflection](reflection.md) | All four Day 5 questions plus the boto3 parameterisation note |

## Run the work

Use Python 3.11 or later to create a virtual environment, then install the pinned Week 4 dependencies.

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r week04\requirements.txt
```

Run the original exercises and the packaged pipeline.

```powershell
python week04\python\transactions.py
python week04\python\debug_me.py
python week04\pipeline.py
python week04\main.py
python week04\analyse.py
python week04\test_week04.py
```

The pipeline reads ten source rows, rejects the two invalid amounts and loads eight rows. Running it again skips the existing transaction IDs instead of creating duplicates. The pandas analysis reads those eight rows and writes `transactions_enriched.csv` with `high_value` and `txn_date` columns.

The SQLite database, virtual environment and Python cache folders are generated locally and excluded by `.gitignore`.
