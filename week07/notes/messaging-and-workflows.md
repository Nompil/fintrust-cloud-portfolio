# Messaging and Workflow Decisions

## Service selection

| Requirement | Choice | FinTrust use |
| --- | --- | --- |
| One consumer processes each task | SQS | Payment events wait safely for the fraud scorer |
| Ordered processing for one account | SQS FIFO | `MessageGroupId` keeps each account's transfers in sequence |
| One event reaches several consumers | SNS with an SQS queue per subscriber | Fraud, ledger, and notification teams process independently |
| Route events by JSON content | EventBridge | RDS failover events invoke the operations notification function |
| Coordinate business steps and compensation | Step Functions Standard | International wire transfers keep an audit history and reverse completed steps after failure |
| Human activity on an external workstation | SWF | The existing KYC officer workflow continues to poll for review tasks |

## Payment queue configuration

The payment queue is FIFO because processing order matters within an account. Different accounts can still run in parallel because the account ID is the message group. The transaction ID is the deduplication ID. The queue uses a 120 second visibility timeout, 14 day retention, 20 second long polling, and a FIFO dead-letter queue after three failed receives.

For an SQS event source mapping, failed messages belong in the SQS dead-letter queue. An asynchronously invoked Lambda from S3 or SNS uses the Lambda function's failure destination or dead-letter queue instead.

## Fan-out

The transaction service publishes one confirmed event to an SNS topic. Separate SQS subscriptions serve fraud review, ledger posting, and customer notification. Each subscriber controls its own retry rate and scaling. The fraud subscription can filter for transactions of at least R50,000 before the event enters its queue.

## Event routing

EventBridge uses an event bus, a pattern, and a target. The FinTrust RDS rule matches failover events and invokes the operations Lambda. EventBridge Scheduler starts nightly reconciliation at 22:00 SAST. These are event and time-based triggers, while CloudWatch alarms remain responsible for metric thresholds.

## Wire transfer workflow

The wire transfer uses Step Functions Standard because it is a critical business workflow that may run longer than five minutes and needs a complete execution history. Compliance hold, currency conversion, SWIFT dispatch, and recipient credit run in sequence. A failure starts the relevant compensating actions in reverse order. The executable state-machine definition is in [`wire_transfer.asl.json`](../infrastructure/wire_transfer.asl.json).
