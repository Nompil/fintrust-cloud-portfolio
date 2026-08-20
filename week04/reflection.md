# Week 4 Reflection

This week I built a local transaction pipeline that validates CSV rows, stores valid records in SQLite, and produces a daily summary. I separated loading, database access, and reporting into a package instead of keeping the entire workflow in one script.

SQLite keeps the lab easy to reproduce locally, while the idempotent insert logic prevents a repeated run from duplicating transaction IDs. A production banking workload would need a managed database design with stronger concurrency, availability, backup, and security controls.

The smoke test now runs the core pipeline in a temporary directory and checks validation, duplicate handling, database row counts, and report output. The pandas analysis is also tested when its dependency is installed.
