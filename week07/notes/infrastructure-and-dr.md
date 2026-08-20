# Infrastructure, Microservices, and Recovery

## CloudFormation

`Resources` is the only mandatory CloudFormation template section. Parameters make templates reusable, Conditions control optional resources, and Outputs expose values needed by other stacks. A Change Set previews a proposed update, while drift detection finds live resources that no longer match the deployed template.

Nested stacks reuse modules such as VPC and IAM templates within an account. Stack Sets deploy a common baseline across accounts and Regions. FinTrust can use Stack Sets for CloudTrail, Config, and GuardDuty across its organisation, while production application stacks reuse nested network and monitoring modules.

The Aurora example uses both `DeletionPolicy: Snapshot` and `UpdateReplacePolicy: Snapshot`. A production Change Set must still be reviewed before execution because property changes can replace resources. The event pipeline template grants the fraud scorer only the SQS and SNS actions it requires.

## Microservice migration

The Strangler Fig pattern allows FinTrust to extract one bounded capability at a time. API Gateway routes fraud and payment paths to new services while all other routes continue to use the monolith. Each extracted service owns its data and deployment lifecycle. Once production monitoring confirms stable behaviour, the duplicate capability can be removed from the monolith.

SQS isolates a producer from one task-processing service. SNS creates one-to-many fan-out. EventBridge adds content-based routing without requiring the producer to know its consumers. API Gateway provides a stable synchronous contract where the caller needs an immediate response.

## Recovery choices

| Workload | Strategy | Reason |
| --- | --- | --- |
| Retail payments | Multi-Site Active-Active | Near-zero RPO and an RTO below 60 seconds justify full capacity in both Regions |
| Regulatory reporting | Warm Standby | Reduced compute already runs in the recovery Region for an RTO of about five minutes |
| Internal HR and finance tools | Backup and Restore | A four-hour RTO allows the lowest-cost option |

Pilot Light keeps the data tier replicated but starts compute only during recovery. Warm Standby already runs compute at reduced capacity. This compute distinction is the clearest way to separate the two strategies.
