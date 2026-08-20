# Week 8 Preparation

## Batch and stream processing

Batch processing collects a bounded set of data and processes it on a schedule. FinTrust could run a nightly job over the day's settled transactions to produce a compliance report. Stream processing handles records continuously as they arrive. A live card transaction feed can score each payment within seconds and update fraud monitoring without waiting for the nightly batch.

## Data lake and data warehouse

A data lake stores large volumes of raw and curated data in object storage, usually before every future use is known. It suits FinTrust transaction events, application logs, model features, and archived documents. A data warehouse stores structured, modelled data optimised for repeatable analytics and business reporting. FinTrust would use the lake for flexible exploration and machine-learning inputs, then publish controlled reporting datasets to a warehouse for finance and regulatory dashboards.

## Athena file format

Athena performs well with Parquet because it is columnar, compressed, and stores data types with the file. A query can read only the required columns rather than scanning each field in every CSV row. Partitioning Parquet files by a useful date field can reduce the scanned data and cost further.
