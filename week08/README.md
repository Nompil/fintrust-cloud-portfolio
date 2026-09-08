# Week 8: Analytics and Intelligent Services

Week 8 adds the analytics and intelligence layer to FinTrust. Transaction data moves from the raw S3 zone into partitioned Parquet, Athena supplies serverless SQL, Kinesis handles the live transaction stream, and EMR prepares monthly fraud features. QuickSight serves the reporting layer, while SageMaker, Rekognition and Comprehend support fraud scoring, KYC and customer service.

## Architecture

- [FinTrust analytics architecture](diagrams/fintrust-analytics-architecture.pdf)
- [Data lake and Athena decisions](notes/data-lake-and-athena.md)
- [Streaming and search decisions](notes/streaming-and-search.md)
- [EMR and QuickSight decisions](notes/emr-and-quicksight.md)
- [Machine learning service decisions](notes/intelligent-services.md)

## Python work

| File | FinTrust purpose |
| --- | --- |
| [Athena compliance reporter](python/athena_reporter.py) | Runs a compliance query asynchronously, writes the result to CSV and can upload the report to S3 |
| [Kinesis producer](python/kinesis_producer.py) | Publishes transactions using `account_id` as the partition key so one account's events stay ordered |
| [Kinesis consumer](python/kinesis_consumer.py) | Decodes the base64 records delivered to a Lambda event source mapping |
| [Security event indexer](python/security_event_indexer.py) | Writes searchable risk events to OpenSearch using IAM request signing |
| [Parquet pipeline](python/parquet_pipeline.py) | Validates the sample CSV and writes Snappy-compressed, year and month partitioned Parquet |
| [Fraud endpoint client](python/fraud_endpoint.py) | Invokes a SageMaker endpoint and maps its probability to an accept, review or reject decision |
| [KYC verification](python/kyc_verification.py) | Uses Rekognition face comparison and the FinTrust 95 percent review threshold |
| [Support ticket router](python/support_ticket_router.py) | Redacts detected PII before routing a ticket according to Comprehend sentiment |
| [Tests](tests/test_week08.py) | Checks the local behaviour with small in-memory AWS client substitutes |

The reporter uses the partition-aware [compliance query](sql/compliance_report.sql) from the Day 1 exercise.

The AWS clients use the normal boto3 credential chain. No credentials, account numbers or customer images are stored in the repository.

## Sample data and local checks

The sample file contains invented FinTrust case-study transactions and no customer information. Build the local Parquet partition with:

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r week08\requirements.txt
python week08\python\parquet_pipeline.py week08\data\transactions.csv week08\data\processed
```

Run the full Week 8 test suite:

```powershell
python -m unittest week08.tests.test_week08 -v
```

## Review work

- [Pandas and Athena comparison](notes/pandas-and-athena.md)
- [Week 9 preparation](notes/week09-preparation.md)
- [Week 8 self assessment](self-assessment.md)
- [Week 8 cost reflection](reflection.md)
- [Portfolio evidence](evidence/portfolio-evidence.md)
- [Local checks](evidence/local-checks.md)

The architecture and code use the same FinTrust paths throughout: compliance reporting, real-time fraud detection, KYC checks and support-ticket routing.
