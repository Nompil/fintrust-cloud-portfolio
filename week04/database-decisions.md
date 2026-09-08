# FinTrust Database Decisions

These decisions come from the Week 4 FinTrust scenarios.

## Day 1: RDS PostgreSQL

FinTrust's relational transaction store uses Amazon RDS for PostgreSQL in `af-south-1`. PostgreSQL was selected for its JSON support and complex financial queries.

| Requirement | Decision |
| --- | --- |
| High availability | Multi-AZ deployment with a synchronous standby in a second Availability Zone |
| Reporting | Read Replica for reporting queries so dashboards do not add load to the primary |
| Encryption | AWS KMS encryption at rest and TLS for connections |
| Network access | Private subnets with TCP 5432 allowed from the application Security Group only |
| Recovery | 35 days of automated backups for point-in-time recovery and monthly manual snapshots retained for 180 days |

Multi-AZ and Read Replicas solve different problems. Multi-AZ provides automatic failover and keeps the same database endpoint. A Read Replica is independently addressable and serves read traffic; promotion is a separate recovery action.

## Day 2: Aurora and DynamoDB

Aurora PostgreSQL is the reporting design because replicas share the cluster volume and do not each maintain a separate copy of the data. Aurora stores six copies across three Availability Zones and can fail over to a replica more quickly than a standard RDS Multi-AZ deployment.

DynamoDB Global Tables store user session tokens in `af-south-1` and `eu-west-1`. Sessions are key-value lookups, and active-active replication means either Region can accept a session update. DAX was considered but not selected because the expected session load does not need a separate microsecond cache.

## Day 3: Purpose-built services

| Requirement | Selected service | Reason |
| --- | --- | --- |
| Immutable transaction history with cryptographic verification | Amazon QLDB | The journal is append-only and its digest can prove that history was not altered |
| Trade confirmations with different JSON fields | Amazon DocumentDB | It provides a document model and a MongoDB-compatible API |
| Product rates and account summaries cached for 60 seconds | ElastiCache for Redis | It reduces repeated reads against RDS and supports richer data structures than Memcached |

Neptune was deferred because the fraud relationship graph has not been scoped. Keyspaces is not needed because FinTrust has no Cassandra workload. Managed Blockchain is not appropriate for a ledger owned by one organisation, and DAX cannot be used as a cache for RDS.

## Day 4: Redshift and migration

Amazon Redshift stores five years of historical portfolio and risk data for business intelligence queries. Its columnar storage and massively parallel processing architecture suit large OLAP aggregations, while Redshift Spectrum can query older data in S3 without first loading it into the cluster. Customer transactions remain on RDS PostgreSQL because Redshift is not designed for high-frequency OLTP writes.

The FinTrust migration design uses AWS Database Migration Service with a full load followed by Change Data Capture. CDC keeps the target current while the source remains in use and supports cutover after replication catches up. The course scenario describes a homogeneous PostgreSQL migration, so AWS Schema Conversion Tool is not required.
