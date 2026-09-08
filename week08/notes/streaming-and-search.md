# Streaming and Search Decisions

## Transaction stream

`transaction-stream` uses eight provisioned shards and retains records for seven days. The core banking service publishes each transaction with `account_id` as the partition key. This keeps the events for one account on the same shard and in sequence, which is important when the fraud scorer calculates transaction velocity.

A single account sending 10,000 transactions in one minute would concentrate writes on one shard. Changing the key to `account_id#transaction_id` would spread that burst, but it would also remove the per-account ordering guarantee. The safer starting point is to retain `account_id`, monitor `WriteProvisionedThroughputExceeded`, and investigate an account producing that volume. If high-volume business accounts become normal, controlled key bucketing can spread their traffic while the consumer restores order using the event timestamp and sequence number.

## Independent consumers

The fraud-scoring Lambda uses Enhanced Fan-Out for dedicated read throughput. A separate Firehose delivery stream copies the same Kinesis records to `s3://fintrust-raw/kinesis-backup/` with a 60 second or 5 MB buffer. A failure in the fraud consumer does not interrupt the raw backup.

## Security search

VPC Flow Logs and CloudTrail records enter CloudWatch Logs. Subscription filters send relevant events to Firehose, which writes monthly `fintrust-vpc-logs-YYYY-MM` and `fintrust-cloudtrail-YYYY-MM` indices in the `fintrust-security-logs` OpenSearch domain. The domain spans three Availability Zones, encrypts traffic and stored data, and uses fine-grained access control. OpenSearch keeps 90 days of searchable data before older records move to lower-cost storage and the compliance archive in S3.
