# FinTrust EC2 Compute Decisions

FinTrust needs different compute patterns for different workloads. The architecture should match each workload to the most appropriate EC2 family, placement strategy, and pricing model.

## Transaction Processing API

- Service: EC2 instances behind an Application Load Balancer
- Instance type: c6i.xlarge
- Pricing model: 3-year Reserved Instances
- Reason: the workload is predictable and continuously active, so a committed purchase model is cost-effective

## Fraud Detection Batch

- Service: EC2 batch compute
- Instance type: c6i.4xlarge
- Pricing model: Spot Instances
- Design detail: checkpoint progress every 10 minutes and store checkpoints in Amazon S3
- Reason: the workload is fault-tolerant and benefits from lower-cost interruptible capacity

## Fraud Detection ML Training Cluster

- Service: GPU-based training cluster
- Instance type: p4d.24xlarge
- Placement strategy: Cluster Placement Group
- Pricing model: Spot Instances
- Reason: the workload requires very high GPU-to-GPU throughput and can tolerate interruption when cost savings are prioritised

## Transaction Database Pair

- Service: primary and standby database instances
- Placement strategy: Spread Placement Group
- Pricing model: Reserved Instances
- Reason: the database tier needs high availability and hardware isolation without sacrificing cost efficiency

## Summary

The overall design balances performance, resilience, and cost by matching each workload to the right compute pattern rather than using one-size-fits-all infrastructure.



Ensures hardware isolation and resilience.



\---



\## Compliance Reports



\### Requirement



\- Monthly execution

\- Under 5 minutes



\### AWS Design



\- EventBridge

\- AWS Lambda



\### Pricing Model



Pay-per-use



\### Reason



Zero idle cost and highly cost effective.



\---



\## Customer Analytics Dashboard



\### Requirement



\- Business-hours workload

\- Reporting and analytics



\### Instance Type



r6i.2xlarge



\### Pricing Model



Savings Plan



\### Reason



Optimises costs for predictable usage patterns.



\---



\## Cost Optimisation Summary



| Workload | Optimisation Strategy |

|-----------|----------------------|

| Transaction Processing | Reserved Instances |

| Fraud Batch | Spot Instances |

| Compliance Reports | Lambda |

| Analytics Dashboard | Savings Plan |



\---



\## Relationship to FinTrust Architecture



These compute decisions support:



\- Customer growth

\- Transaction processing

\- Fraud detection

\- Compliance reporting

\- Business analytics

\- Cost optimisation



The overall architecture combines:



\- EC2

\- Auto Scaling Groups

\- Application Load Balancers

\- Lambda

\- ECS Fargate

\- Amazon S3

\- Amazon RDS PostgreSQL 







