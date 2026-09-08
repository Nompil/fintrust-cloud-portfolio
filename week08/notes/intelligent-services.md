# Machine Learning Service Decisions

## Fraud scoring

The payment API sends 28 transaction features through API Gateway to `fintrust-fraud-scorer`. The Lambda function calls the `fintrust-fraud-endpoint` SageMaker real-time endpoint and maps the returned probability to three outcomes: accept below `0.3`, manual review from `0.3` to `0.7`, and reject above `0.7`. Two `ml.m5.xlarge` instances provide endpoint availability. Provisioned Concurrency on the Lambda reduces cold starts on the live payment path, while SageMaker data capture supplies samples for drift monitoring.

SageMaker is justified here because FinTrust owns labelled fraud history and needs a bank-specific model. Batch Transform is better for rescoring a large S3 archive, but the customer payment path needs a real-time endpoint.

## KYC

A customer uploads a selfie and ID image to a private S3 bucket through pre-signed URLs. An S3 event invokes `fintrust-kyc-check`, which calls `rekognition:CompareFaces` with a 95 percent threshold. Results below the approval threshold go to manual review. Every outcome is written to `kyc-audit-log` in DynamoDB, and the images follow the seven-year retention policy.

Rekognition fits because face comparison is a pre-built computer-vision task. Training and hosting a custom SageMaker vision model would add work without a FinTrust-specific requirement.

## Support tickets and least privilege

API Gateway sends a new ticket to `fintrust-ticket-router`. The Lambda function calls `comprehend:DetectPiiEntities` before analytics storage, then calls `comprehend:DetectSentiment`. Redacted tickets are sent with `sqs:SendMessage` to either the urgent or standard support queue. The role also needs CloudWatch logging permissions and KMS permissions for the selected queues. It does not receive wildcard access to S3, Comprehend or SQS.

Comprehend handles standard PII and sentiment through managed APIs. A custom classifier is only justified when FinTrust uses its labelled support history to assign bank-specific categories.
