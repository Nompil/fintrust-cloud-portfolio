# Week 4 Reflection

## 1. Database selection

Keeping every workload in one PostgreSQL instance would make transaction processing compete with sessions, reporting, document queries and historical analytics. RDS PostgreSQL protects the ACID transaction workload, DynamoDB Global Tables handle active-active session writes, QLDB provides cryptographic history, DocumentDB stores flexible trade documents, Redis caches frequently read rates, and Redshift handles OLAP queries. Aurora keeps reporting traffic away from the transaction database and provides fast replica failover. The trade-off is operational overhead because seven services mean more IAM policies, monitoring dashboards, backup checks, cost lines and service knowledge to maintain.

## 2. ETL pipeline and availability

If two copies of the pipeline write to the same SQLite file at once, one process can hold the file lock while the other waits or receives a `database is locked` error. The transaction ID primary key stops duplicate inserts, but a report can still run before the other batch finishes. RDS Multi-AZ protects against an Availability Zone or primary database failure by synchronously maintaining a standby and failing over through the same endpoint, usually within 60 to 120 seconds. It does not scale reporting reads, which require a Read Replica, and it does not move a live database, which is the role of DMS with Change Data Capture. Higher concurrent write volume also needs suitable transactions and connection pooling rather than Multi-AZ alone.

## 3. Python package structure

Splitting the pipeline makes each responsibility independently importable and testable. I can test `validate_row()` with an in-memory row without opening SQLite, and I can test `generate_report()` against a temporary database without reading the CSV. Replacing `database.py` with a PostgreSQL implementation would not require changes to the validation rules. The package also lets continuous integration run focused tests without executing the entire pipeline as a script.

## 4. Week 5 network requirements

RDS and ElastiCache should use private subnets without public IP addresses, with Security Groups allowing database or cache traffic only from the application tier. This keeps direct internet traffic away from the data services while still allowing the application to reach the required ports. A DynamoDB Gateway Endpoint gives private subnets a route to DynamoDB through the AWS network without using an Internet Gateway or NAT Gateway. The endpoint policy can further restrict which DynamoDB tables the application is allowed to access.

## boto3 and parameterised requests

boto3 does not use SQL `?` placeholders for S3 or DynamoDB operations. SDK calls pass values in structured Python dictionaries, and boto3 serialises those values into AWS API requests. SQL parameterisation is still required when Python sends queries to SQLite or PostgreSQL.
