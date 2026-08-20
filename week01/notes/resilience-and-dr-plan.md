# FinTrust Resilience and Disaster Recovery Plan

FinTrust combines Multi-AZ compute, load balancing, asynchronous messaging, and a Pilot Light recovery environment. Each layer addresses a different failure mode.

## Compute and traffic

- Auto Scaling Group: minimum 2, desired 4, maximum 10 instances.
- Availability Zones: `af-south-1a` and `af-south-1b`.
- Target tracking: maintain approximately 60% average CPU utilisation.
- Scheduled scaling: raise capacity before predictable month-end salary-processing peaks.
- Golden AMI: launch replacement instances with the approved patched configuration.
- Application Load Balancer: terminate TLS, check target health, and route `/api/accounts/*`, `/api/transactions/*`, and `/api/fraud-alerts/*` to separate target groups.

## Resilience architecture

The complete resilience flow is shown in the [Week 1 architecture diagrams PDF](../diagrams/week01_architecture_diagrams.pdf).

The Application Load Balancer sends traffic only to healthy instances in the Auto Scaling group. RDS maintains a standby database in another Availability Zone. SQS prevents a slow fraud-scoring consumer from blocking transaction submission. SNS publishes each completed event to independent queues so notification, audit, and analytics consumers can retry and scale separately. The Pilot Light environment is activated only when a regional recovery is approved.

## Disaster recovery

| Item | Decision |
| --- | --- |
| Primary Region | `af-south-1` (Cape Town) |
| Recovery Region | `eu-west-1` (Ireland), subject to approved cross-border safeguards |
| Strategy | Pilot Light |
| Recovery point objective | 15 minutes |
| Recovery time objective | Less than 1 hour |
| Recovery data | Encrypted database backups and approved S3 replicas |
| Failover | Scale recovery compute, restore or promote data services, validate controls, then update Route 53 |

The programme scenario permits encrypted disaster-recovery copies in Ireland under suitable safeguards. A real implementation requires formal legal, security, and data-governance approval before any cross-border replication.

## Failure mapping

| Failure | Defence | Expected result |
| --- | --- | --- |
| EC2 instance fails | ASG health checks and golden AMI | A replacement instance launches automatically |
| One Availability Zone fails | Multi-AZ ASG and ALB | Traffic goes only to healthy targets while capacity rebalances |
| Fraud scoring slows down | SQS | Requests wait durably without tightly coupling the services |
| Month-end traffic triples | Scheduled scaling plus target tracking | Capacity is available before and during the predictable peak |
| Primary Region is unavailable | Pilot Light recovery runbook | Restore service within the approved RTO and RPO targets |

RTO and RPO are objectives, not guarantees. Recovery exercises must measure whether the design actually meets them.
