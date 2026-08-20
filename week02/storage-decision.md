# FinTrust EBS Storage Decision

## Workload mapping

| Component | Storage type | AWS service | Configuration | Reason |
| --- | --- | --- | --- | --- |
| Transaction API web tier | Block | EBS gp3 | 100 GB, 3,000 IOPS | General-purpose SSD performance at a lower cost than provisioned IOPS storage |
| Transaction database | Block | EBS io2 Block Express | 500 GB, 10,000 provisioned IOPS | Consistent performance and high durability for transaction processing |
| Transaction history older than two years | Object | S3 Glacier Instant Retrieval | Lifecycle transition from S3 | Lower storage cost for data that is read infrequently |
| Fraud model files | File | Amazon EFS | Regional file system with Elastic throughput | Multiple Lambda functions and ECS tasks can mount the same files |
| EBS backups | Snapshot | EBS snapshots managed by DLM | Daily at 03:00, 30-day retention | Incremental point-in-time backups that can restore a volume in another Availability Zone |

## Architecture

The storage layout is shown in the [Week 2 architecture diagrams PDF](diagrams/week02_architecture_diagrams.pdf).

## gp3 and io2 cost decision

gp3 is the normal starting point because storage, IOPS, and throughput can be sized independently. Its included baseline performance is enough for the web tier and many general workloads. io2 costs more because provisioned IOPS are billed separately, but FinTrust accepts that cost for the transaction database where predictable I/O and durability matter more than the lowest monthly price. Exact prices should be checked in the AWS Pricing Calculator for `af-south-1` before deployment.

## Snapshot policy

Data Lifecycle Manager creates a snapshot every day at 03:00 and retains it for 30 days. A quarterly recovery test restores a new volume in a different Availability Zone and verifies the database before the temporary recovery resources are removed.
