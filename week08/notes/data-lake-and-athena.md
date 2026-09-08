# Data Lake and Athena Decisions

## Data flow

FinTrust keeps three S3 zones in `af-south-1`. Source systems write immutable CSV records to the raw zone. Glue crawls the new objects, registers the schema and runs the CSV-to-Parquet job. The processed zone stores Snappy-compressed Parquet under `year=` and `month=` partitions. Curated compliance summaries and fraud features are written to the final zone for Athena and QuickSight.

| Zone | Main content | Retention choice |
| --- | --- | --- |
| `fintrust-raw` | Daily source exports and Kinesis backup | Versioned; Glacier Instant Retrieval after 90 days; expire after seven years |
| `fintrust-processed` | Validated, partitioned Parquet | S3 Infrequent Access after 12 months; rebuildable from raw data |
| `fintrust-curated` | Compliance aggregates and fraud features | Frequently queried data stays online; Athena results expire after 30 days |

Writes only move from raw to processed to curated. The Glue role can read raw and write processed, while the EMR role can read processed and write curated. Neither role can overwrite the raw evidence.

## Athena configuration

The `fintrust-queries` workgroup writes encrypted results to `s3://fintrust-curated/athena-results/` and rejects a query after 10 GB has been scanned. Compliance queries filter by `year` and `month`, so Athena reads only the required Parquet partitions. Columnar storage, compression and partition pruning reduce both scan time and cost compared with the original CSV exports.

The Glue Data Catalog is shared by Athena, EMR and Redshift Spectrum. The daily crawler updates `transactions_raw`, while the processed `transactions` table keeps `year` and `month` as partition keys.

## Asynchronous work

Athena and EMR both use a submit-and-poll pattern. An EMR feature-engineering job may process years of transaction history and run for several hours, so keeping one client connection open for the whole job would be unreliable. Submitting the work first also lets monitoring and retry logic operate independently from the person or process that started it.
