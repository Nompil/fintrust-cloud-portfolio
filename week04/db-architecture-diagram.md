# FinTrust Seven-Layer Database Architecture

This design maps each FinTrust data requirement to the AWS database service that best fits its access pattern, scale and recovery needs.

| Layer | AWS service | Region | FinTrust role | Why this service fits |
| --- | --- | --- | --- | --- |
| 1 | RDS PostgreSQL Multi-AZ | `af-south-1`, primary and standby in separate Availability Zones | Account balances, payments and transfers | ACID transactions protect financial integrity. Multi-AZ synchronously maintains a standby and keeps the same database endpoint during automatic failover. |
| 2 | Aurora PostgreSQL reporting replica | `af-south-1` | Balance sheets, transaction exports and reporting queries | Aurora keeps six storage copies across three Availability Zones. Its replicas share the cluster volume, which supports fast failover and separates reporting from transaction processing. |
| 3 | DynamoDB Global Tables | `af-south-1` and `eu-west-1` | Customer session tokens and login state | Both Regions accept writes, and active-active replication keeps session data close to users. On-Demand capacity suits unpredictable login spikes. |
| 4 | Amazon QLDB | `af-south-1` | Regulatory transaction history | The append-only journal and cryptographic digest provide verifiable evidence that transaction history has not been altered. |
| 5 | Amazon DocumentDB | `af-south-1` | Trade confirmation documents | The document model supports different JSON fields for equity, bond, foreign exchange and derivative trades through a MongoDB-compatible API. |
| 6 | ElastiCache for Redis | `af-south-1` | Homepage foreign exchange rates and ranked rate data | In-memory access gives sub-millisecond reads. Redis provides sorted sets, persistence and Multi-AZ failover, which are not available together in Memcached. |
| 7 | Amazon Redshift | `af-south-1` | Five years of portfolio and risk analytics | Columnar storage and massively parallel processing suit OLAP queries over billions of rows. Redshift Spectrum can query older data in S3 without loading it into the cluster. |

## Migration path

`Flat-file NAS` → `AWS DMS full load and CDC` → `RDS PostgreSQL Multi-AZ`

The full load copies the existing transaction history. Change Data Capture keeps applying inserts, updates and deletes while the source remains in use, allowing cutover after the target catches up. The course scenario treats this as a homogeneous PostgreSQL migration, so Schema Conversion Tool is not required.

## Design boundaries

RDS Multi-AZ provides availability, while the reporting replica handles read scaling. DynamoDB Global Tables provide multi-Region writes for sessions, whereas Aurora Global Database would retain one write Region. Redshift is reserved for analytics and does not process customer transactions.
