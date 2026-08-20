# Week 7 Validation Record

**Date:** 20 August 2026

## Python applications

The Week 7 code was compiled and tested in an isolated Python environment using the declared requirements.

| Check | Result |
| --- | --- |
| Flask create, retrieve, update, and request ID behaviour | Passed |
| Flask input validation | Passed |
| FastAPI extension endpoints | Passed |
| Pydantic input validation | Passed |
| SQS FIFO group and deduplication values | Passed |
| Fraud score for supplied high-risk example | Passed with score 95 |
| SNS alert and partial batch failure behaviour | Passed |
| API Gateway Lambda transaction validation | Passed |
| Lambda SQS event identification | Passed |

Nine tests completed with no failures.

## Infrastructure definitions

| Check | Result |
| --- | --- |
| `event_pipeline.yaml` CloudFormation lint | Passed with no findings |
| `protected_aurora.yaml` CloudFormation lint | Passed with no findings |
| `wire_transfer.asl.json` JSON validation | Passed |
| Aurora deletion and replacement protection | Snapshot policy present |
| Pipeline permissions | Scoped to the payment queue and alert topic |

## Diagram PDFs

| File | Pages | Result |
| --- | ---: | --- |
| `diagrams/week07_architecture_diagrams.pdf` | 5 | Valid PDF |
