# Week 4: Databases and Transaction Pipelines

Week 4 covers custom exceptions, debugging, relational database availability, and a local CSV-to-SQLite transaction pipeline.

## Deliverables

- [Custom transaction exceptions](python/transactions.py)
- [Debugging exercise](python/debug_me.py)
- [Pipeline entry point](main.py)
- [`fintrust_pipeline` package](fintrust_pipeline/)
- [Pandas analysis](analyse.py)
- [Smoke-test runner](run_smoke_tests.py)
- [Pipeline architecture PDF](diagrams/week04_pipeline_architecture.pdf)
- Sample input: `transactions.csv`
- Sample outputs: `daily_report.txt` and `transactions_enriched.csv`

## Pipeline

The pipeline validates CSV rows, inserts valid transactions into SQLite without duplicating transaction IDs, and writes a summary report. The analysis script reads the same database and exports an enriched CSV.

## Run

```powershell
python -m pip install -r week04\requirements.txt
python week04\run_smoke_tests.py
```

The SQLite database is generated locally and excluded from version control.
