# Week 4 Reflection

## What would break if two processes ran this pipeline at the same time against the same SQLite file?

If two processes ran this pipeline at exactly the same time against the same SQLite database file, write operations could conflict because SQLite allows only one writer at a time. One process could successfully obtain the write lock while the second process encounters a "database is locked" error when attempting to insert records.

## How would RDS Multi-AZ handle this differently?

Amazon RDS Multi-AZ is designed for concurrent access and high availability. Multiple clients can access the database simultaneously while the database engine manages transactions, locking, and consistency. AWS also manages replication and failover between Availability Zones, providing better fault tolerance, scalability, and reliability than a local SQLite database.

## Key Lessons Learned

In a production environment, RDS Multi-AZ provides higher availability through synchronous replication to a standby instance and automatic failover during infrastructure problems. This makes it more reliable and scalable than a file-based SQLite database for enterprise workloads.

- Validate data before loading into a database.
- Use parameterized SQL queries.
- Use primary keys to prevent duplicates.
- Design idempotent ETL pipelines.
- Separate validation, persistence, and reporting into different functions.

## boto3 and Parameterisation

boto3 does not use SQL placeholders such as `?` or `%s` because services like S3 and DynamoDB do not use SQL queries. Instead, boto3 sends structured API requests using Python dictionaries and method parameters.

This reduces the risk of injection issues because requests are built from strongly defined API inputs rather than dynamically constructed query strings. Validation and parameter handling occur at the SDK and AWS service level rather than through SQL parameterisation.