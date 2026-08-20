# FinTrust Lambda Design

## Fraud-scoring function

| Setting | Decision |
| --- | --- |
| Function name | `fintrust-fraud-scorer` |
| Trigger | DynamoDB Streams event for a newly written transaction |
| Runtime | Python 3.12 |
| Memory | 512 MB |
| Timeout | 30 seconds |
| Concurrency | 10 provisioned execution environments |
| Region | `af-south-1` |

The event flow is shown in the [Week 2 architecture diagrams PDF](diagrams/week02_architecture_diagrams.pdf).

## Cold-start strategy

The fraud scorer is latency-sensitive, so Provisioned Concurrency keeps ten execution environments initialised and ready during the initial design. CloudWatch concurrency and duration metrics must be reviewed before changing that number. Database clients and model data should be initialised outside the handler so a warm environment can reuse them.

The monthly compliance report does not need Provisioned Concurrency because its scheduled workload can tolerate a cold start.

## Service limits and fit

- Lambda has a maximum execution time of 15 minutes.
- The fraud scorer is short-lived, stateless, and event-driven, which makes Lambda suitable.
- A four-hour fraud batch job does not fit Lambda and should run as an ECS Fargate task.
- An S3 event can invoke a separate Lambda function when a transaction CSV is uploaded.
- EventBridge Scheduler can invoke the compliance-report function each month.
