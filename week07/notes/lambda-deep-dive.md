# Lambda Deep Dive

Day 3 covers Lambda performance, invocation models, VPC networking, configuration, and observability.

## Performance and concurrency

Cold starts occur when Lambda creates a new execution environment. Module-level clients and configuration can be reused by warm environments, so they should not be recreated in every handler call. Provisioned Concurrency keeps a chosen number of environments initialised for latency-sensitive work. Reserved Concurrency limits and reserves capacity but does not remove cold starts.

Memory also controls CPU allocation. At approximately 1,769 MB, a function receives the equivalent of one vCPU. Memory should be selected using measured duration and cost rather than assuming that the smallest setting is cheapest.

## Invocation models

| Invocation | Example | Failure handling |
| --- | --- | --- |
| Synchronous | API Gateway request | Caller receives the response and decides whether to retry |
| Asynchronous | S3 or SNS event | Lambda retries, then sends the event to its configured failure destination or dead-letter queue |
| Event source mapping | Lambda polling SQS | Failed messages return to the queue; the queue redrive policy moves repeated failures to its dead-letter queue |

The fraud scorer returns `batchItemFailures`. That allows the event source mapping to retry only malformed records instead of making every successful message in the batch visible again.

## VPC networking

A Lambda function attached to private VPC subnets does not receive a public IP address. Internet access requires a route from each private subnet to a NAT Gateway in the same Availability Zone. Calls to S3 and DynamoDB can use gateway VPC endpoints instead, which avoids NAT processing and keeps traffic on the AWS network. Interface endpoints are appropriate for supported services such as Secrets Manager.

## Configuration and observability

Non-secret settings such as threshold values and queue URLs belong in environment variables. Passwords and tokens belong in Secrets Manager or Parameter Store `SecureString`. Structured logs should include the request ID, transaction ID, function version, and remaining time. The handler should stop before the platform timeout when there is not enough time to complete safely.
