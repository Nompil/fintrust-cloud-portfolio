# Week 4 Reflection

1) What I built this week (3–5 sentences):

I implemented an end-to-end local ETL pipeline that reads `week04/transactions.csv`, validates and loads transactions into a local SQLite store, and generates a daily report (`daily_report.txt`). I added enrichment steps in `analyse.py` to produce `transactions_enriched.csv` and built the `fintrust_pipeline` package to separate loader, database and reporter responsibilities. I also produced a consolidated Week 4 guide exported to DOCX and HTML for portfolio submission.

2) Key technical decisions and why (3–5 sentences):

SQLite was chosen for local reproducibility and minimal setup; production would use RDS Multi-AZ for concurrency and availability. The pipeline is designed to be idempotent and to validate rows before insertion to avoid duplicate or malformed data. Splitting validation, persistence, and reporting into modules improves maintainability and testability.

3) What I struggled with and how I resolved it (2–4 sentences):

Initial dependency issues (missing `pandas`) prevented local analysis; I fixed this by installing dependencies in a temporary virtual environment and re-running `analyse.py`. I also ran into PDF conversion limitations with `pandoc` + no LaTeX engine, so I exported the guide as DOCX and HTML instead and documented the PDF requirements.

4) What I'd add to make this portfolio artifact stronger (1–2 bullet points):

- Add a small integration test that runs `week04/main.py` in a temporary directory to verify end-to-end behaviour.
- Replace SQLite with a small Dockerized RDS-compatible instance for testing concurrent access scenarios if needed.
