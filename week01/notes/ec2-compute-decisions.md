\# FinTrust EC2 Compute Decisions



\## Overview



FinTrust serves 2.3 million customers and expects to grow to 5 million customers by 2027.



Multiple AWS compute services are required because different workloads have different performance, availability and cost requirements.



\---



\## Transaction Processing API



\### Requirement



\- Always running

\- Handles customer transactions

\- Supports burst traffic



\### AWS Design



\- EC2

\- Auto Scaling Group

\- Application Load Balancer (ALB)



\### Instance Type



c6i.xlarge



\### Pricing Model



3-Year Reserved Instances



\### Reason



Predictable workload with high utilisation.



\---



\## Fraud Detection Batch



\### Requirement



\- Overnight processing

\- Fault tolerant

\- Long-running workload



\### AWS Design



c6i.4xlarge



\### Pricing Model



Spot Instances



\### Additional Design



\- Checkpoint progress every 10 minutes

\- Store checkpoints in Amazon S3



\### Reason



Can tolerate interruptions and achieves significant cost savings.



\---



\## Fraud Detection ML Training Cluster



\### Requirement



\- GPU-intensive machine learning

\- Maximum throughput



\### AWS Design



p4d.24xlarge



\### Placement Strategy



Cluster Placement Group



\### Pricing Model



Spot Instances



\### Reason



Maximises GPU-to-GPU communication performance.



\---



\## Transaction Database Pair



\### Requirement



\- High availability

\- Fault tolerance



\### Design



Primary and Standby Database



\### Placement Strategy



Spread Placement Group



\### Pricing Model



Reserved Instances



\### Reason



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







