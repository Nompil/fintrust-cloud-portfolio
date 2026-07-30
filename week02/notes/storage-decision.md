\# FinTrust Storage Decision Matrix



\## Overview



FinTrust uses multiple AWS storage services because different workloads require different storage characteristics.



Key requirements include:



\- High-performance transaction processing

\- Long-term archive retention

\- Shared machine-learning model storage

\- Backup and disaster recovery



\---



\# Amazon EBS



Amazon Elastic Block Store (EBS) provides persistent block storage for EC2 instances.



Characteristics:



\- Attached to a single EC2 instance

\- Persistent across stop/start

\- Lives within a single Availability Zone

\- Supports snapshots for backups



\---



\# EBS Volume Types



\## gp3



Type:



General Purpose SSD



Maximum Performance:



\- 16,000 IOPS

\- 1,000 MB/s throughput



FinTrust Use:



\- Transaction API web servers

\- Application servers

\- Operating system volumes



Configuration:



\- 100 GB

\- 3,000 IOPS



Reason:



Cost-effective SSD storage for general workloads.



\---



\## io2 Block Express



Type:



Provisioned IOPS SSD



Maximum Performance:



\- 256,000 IOPS

\- 4,000 MB/s throughput



Durability:



\- 99.999%



FinTrust Use:



\- RDS transaction database



Configuration:



\- 500 GB

\- 10,000 IOPS



Reason:



Mission-critical financial transactions require consistent IOPS and maximum durability.



\---



\## st1



Type:



Throughput Optimized HDD



Maximum Performance:



\- 500 IOPS

\- 500 MB/s



FinTrust Use:



\- Audit logs

\- Analytics processing



Reason:



Optimized for sequential access workloads.



\---



\## sc1



Type:



Cold HDD



Maximum Performance:



\- 250 IOPS

\- 250 MB/s



FinTrust Use:



\- Infrequently accessed records



Reason:



Lowest storage cost.



\---



\# EBS vs S3 vs EFS



\## Amazon EBS



Storage Type:



Block Storage



Best For:



\- Databases

\- Operating systems

\- Transaction processing



FinTrust Example:



```text

RDS Transaction Database

```



\---



\## Amazon S3



Storage Type:



Object Storage



Best For:



\- Backups

\- Archives

\- Static files



FinTrust Example:



```text

Transaction archives

```



\---



\## Amazon EFS



Storage Type:



Shared File Storage



Best For:



\- Multiple application servers

\- Shared files

\- Machine learning models



FinTrust Example:



```text

Fraud detection model files

```



\---



\# Snapshot Strategy



\## Purpose



EBS snapshots provide point-in-time backups.



Snapshots are stored in:



```text

AWS-managed S3

```



\---



\## Benefits



\- Incremental backups

\- Cross-AZ recovery

\- Cross-region copy

\- Disaster recovery support



\---



\## FinTrust Snapshot Policy



Schedule:



```text

03:00 every day

```



Retention:



```text

30 days

```



Automation:



```text

Amazon Data Lifecycle Manager (DLM)

```



Testing:



```text

Quarterly restore tests

```



\---



\# FinTrust Storage Architecture



\## Transaction Processing EC2



Storage:



```text

EBS gp3

```



Configuration:



\- 100 GB

\- 3,000 IOPS



Reason:



Balanced performance and cost.



\---



\## RDS Transaction Database



Storage:



```text

EBS io2 Block Express

```



Configuration:



\- 500 GB

\- 10,000 IOPS



Reason:



Mission-critical workload requiring very high durability.



\---



\## Transaction History Archive



Storage:



```text

S3 Glacier Instant Retrieval

```



Reason:



Data older than 2 years is rarely accessed.



Cost is significantly lower than EBS.



\---



\## Fraud Detection ML Models



Storage:



```text

Amazon EFS

```



Reason:



Must be shared across multiple services.



Supports Lambda and ECS access.



\---



\## Backups



Storage:



```text

AWS-managed S3 via EBS Snapshots

```



Configuration:



\- Daily snapshots

\- 30-day retention



\---



\# Cost Comparison



\## gp3



Advantages:



\- Lower cost

\- Suitable for most workloads



Disadvantages:



\- Lower durability than io2



\---



\## io2 Block Express



Advantages:



\- Consistent provisioned IOPS

\- 99.999% durability

\- Predictable performance



Disadvantages:



\- Higher cost



\---



\## FinTrust Decision



For databases:



```text

io2 Block Express

```



Reason:



The transaction database is mission-critical and requires maximum durability.



For web servers:



```text

gp3

```



Reason:



Cost-effective with sufficient performance.



\---



\# Key Decision Rules



Choose:



```text

gp3

```



When:



\- General-purpose workloads

\- Application servers

\- OS volumes



\---



Choose:



```text

io2 Block Express

```



When:



\- Mission-critical databases

\- High IOPS requirements

\- Maximum durability required



\---



Choose:



```text

S3 Glacier

```



When:



\- Archive data

\- Long-term retention



\---



Choose:



```text

EFS

```



When:



\- Multiple services need shared file access



\---



\# FinTrust Architecture Summary



Transaction API

&#x20;       ↓

EBS gp3



RDS Database

&#x20;       ↓

EBS io2 Block Express



Transaction Archives

&#x20;       ↓

S3 Glacier



Fraud ML Models

&#x20;       ↓

EFS



Backups

&#x20;       ↓

EBS Snapshots

&#x20;       ↓

AWS-managed S3



This storage design balances performance, durability, scalability and cost optimization for FinTrust's cloud-native banking platform.

