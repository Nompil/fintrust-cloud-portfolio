\# Week 4 Day 3 Reflection



\## What would break if two processes ran this pipeline at the same time against the same SQLite file?



SQLite supports limited concurrent write access. If two processes attempted to load transactions into the same database simultaneously, file locking and write contention could occur. This could result in delays, lock errors or failed inserts.



\## How would RDS Multi-AZ handle this differently?



Amazon RDS Multi-AZ is designed for concurrent access and high availability. Multiple clients can access the database simultaneously while AWS manages replication and failover between Availability Zones. This provides better fault tolerance, scalability and reliability than a local SQLite database.



\## Key Lessons Learned



\- Validate data before loading into a database.

\- Use parameterized SQL queries.

\- Use primary keys to prevent duplicates.

\- Design idempotent ETL pipelines.

\- Separate validation, persistence and reporting into different functions.

