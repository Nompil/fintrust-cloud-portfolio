# Week 8 Portfolio Evidence

## Included in this repository

| Requirement | Evidence |
| --- | --- |
| Analytics data flow | Five-page FinTrust architecture PDF |
| Athena query code | Compliance reporter with polling, CSV output and S3 upload support |
| Kinesis producer | Single and batch publishing with `account_id` partitioning |
| Kinesis consumer | Lambda-style base64 record decoding |
| Parquet processing | CSV validation, date partitioning and Snappy output |
| OpenSearch integration | IAM-signed client and security event indexing |
| SageMaker integration | Real-time endpoint request and decision thresholds |
| Rekognition integration | KYC face comparison with a 95 percent threshold |
| Comprehend integration | PII redaction, sentiment detection and SQS routing |
| Service decisions | Data lake, streaming, EMR, QuickSight and intelligent-services notes |
| Self assessment and reflection | Week 8 topic review and cost decision |

## AWS session captures for the LMS

Capture these from the learner account during the practical sessions:

1. Athena result from `fintrust_curated`, including the columns and data-scanned value
2. `transaction-stream` showing eight shards and seven-day retention
3. OpenSearch Dashboards showing the security-log index and a saved visualisation
4. EMR configuration showing Primary, Core and Task instance choices
5. QuickSight chart with the completed SPICE refresh status
6. `fintrust-fraud-endpoint` in `InService`
7. Rekognition `FaceMatches` output with the customer image locations redacted
8. Original and redacted Comprehend support-ticket text
9. Week 8 mock score and the two topics selected for revision
