# Week 3 Reflection

1) What I built this week (3–5 sentences):

I developed and refined data-cleaning utilities for FinTrust transaction data (`clean_transactions_v2.py`), created helper scripts to prepare directory structures, and experimented with CSV/JSON test data for the pipeline. I also documented storage design choices and created diagrams that show how raw data flows into cleaned datasets for later analytics.

2) Key technical decisions and why (3–5 sentences):

I focused on deterministic, idempotent cleaning steps: normalise date/time, enforce numeric types for amounts, and drop or tag malformed rows so downstream analytics can handle them. The approach improves reproducibility and makes debugging ETL issues easier in later pipeline stages.

3) What I struggled with and how I resolved it (2–4 sentences):

Error handling and logging were new challenges; I moved from print-based debugging to structured logging and explicit exception handling in the cleaning scripts. This made it easier to trace failures and keep data validation visible in pipeline logs.

4) What I'd add to make this portfolio artifact stronger (1–2 bullet points):

- Add a small sample dataset and a short notebook or script that demonstrates the cleaning steps end-to-end.
- Export diagrams from `week03/diagrams/` and reference them from the README.
