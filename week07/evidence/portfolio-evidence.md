# Week 7 Portfolio Evidence

## Included in this repository

| Requirement | Evidence |
| --- | --- |
| Event-driven architecture | Five-page PDF covering messaging, APIs, Lambda, infrastructure and the complete application path |
| Flask or FastAPI application | Both implementations, endpoint notes and local tests |
| Lambda fraud scorer | Rule-based scorer with SNS alerts and partial batch failure handling |
| SQS FIFO design | CloudFormation with ordering, encryption, long polling, retention and a dead-letter queue |
| SNS fan-out design | Architecture notes and an encrypted alert topic in CloudFormation |
| Infrastructure protection | Aurora template with snapshot retention policies |
| Mock exam review | Ten scenario answers with short reasons |
| Self-assessment | Confidence ratings and a focused revision plan |
| Reflection | Week 7 reflection within the requested length |
| Week 8 preparation | Batch, stream, data lake, warehouse and Parquet questions answered |

## Console captures for the LMS

Capture these during the AWS lab so they show the resources in the learner account:

1. SQS FIFO queue with at least one visible message
2. SNS topic subscriber list showing the SQS subscription
3. CloudWatch Logs entry showing a transaction and its fraud score
