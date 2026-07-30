\# FinTrust Shared Storage Decision



\## Overview



FinTrust now uses all three AWS storage categories:



\- Block Storage (EBS)

\- Object Storage (S3)

\- File Storage (EFS and FSx)



Each storage type solves a different business problem.



\---



\# Amazon EFS



Amazon EFS is a shared NFS file system for Linux workloads.



Key Features:



\- Multi-AZ access

\- Multiple EC2 instances can mount simultaneously

\- Elastic storage growth

\- No capacity planning

\- Pay only for storage used



FinTrust Use Case:



Fraud detection model files shared between:



\- AWS Lambda

\- ECS Fargate

\- Analytics workloads



Configuration:



\- General Purpose Performance

\- Elastic Throughput

\- EFS Standard



\---



\# EFS Storage Classes



\## EFS Standard



Used for frequently accessed files.



Advantages:



\- Best performance

\- Multi-AZ resilience



\---



\## EFS Standard-IA



Used for infrequently accessed files.



Advantages:



\- Lower cost

\- Lifecycle management support



\---



\# Amazon FSx Family



AWS provides purpose-built managed file systems.



\---



\## FSx for Windows File Server



Protocol:



```text

SMB

```



Features:



\- Active Directory integration

\- Windows permissions

\- Windows-native file sharing



FinTrust Use Case:



Compliance document shares for:



\- Audit Team

\- Risk Team

\- Legal Team



\---



\## FSx for Lustre



Purpose:



High-performance computing and machine learning.



Features:



\- Very high throughput

\- Sub-millisecond latency

\- Native S3 integration



FinTrust Use Case:



Fraud model training data cache.



Configuration:



\- Scratch deployment

\- Linked to S3 transaction archive



\---



\## FSx for NetApp ONTAP



Supports:



\- NFS

\- SMB

\- iSCSI



Use Case:



Enterprise migrations from NetApp storage.



\---



\## FSx for OpenZFS



Supports:



\- Linux

\- Unix

\- NFS



Use Case:



Organizations migrating from ZFS environments.



\---



\# Storage Selection Guide



\## EBS



Choose when:



\- Database storage

\- Single EC2 instance

\- Boot volumes



FinTrust Example:



RDS Transaction Database



\---



\## EFS



Choose when:



\- Multiple Linux servers need shared files

\- Multi-AZ file access required



FinTrust Example:



Fraud ML model files



\---



\## FSx for Windows



Choose when:



\- Windows workloads

\- Active Directory

\- SMB protocol



FinTrust Example:



Compliance document shares



\---



\## FSx for Lustre



Choose when:



\- HPC workloads

\- Machine learning

\- Massive throughput

\- S3 integration required



FinTrust Example:



Fraud model training



\---



\# FinTrust Shared Storage Architecture



\## Fraud Model Files



Storage:



Amazon EFS



Configuration:



\- General Purpose

\- Elastic Throughput



Reason:



Multiple services require simultaneous access.



\---



\## Compliance Documents



Storage:



FSx for Windows File Server



Configuration:



\- SMB

\- Active Directory



Reason:



Windows applications require native Windows file sharing.



\---



\## Fraud Training Data



Storage:



FSx for Lustre



Configuration:



\- Scratch deployment

\- Linked to S3



Reason:



High-speed ML workloads require maximum throughput.



\---



\## Transaction Database



Storage:



EBS io2 Block Express



Reason:



Mission-critical database requiring high IOPS.



\---



\## Transaction Archive



Storage:



S3 Glacier Instant Retrieval



Reason:



Low-cost long-term retention.



\---



\# Three Storage Types Summary



\## Block Storage



Service:



```text

Amazon EBS

```



Example:



Transaction Database



\---



\## Object Storage



Service:



```text

Amazon S3

```



Example:



Transaction Archives



\---



\## File Storage



Services:



```text

Amazon EFS

Amazon FSx

```



Examples:



ML Files

Compliance Documents

Training Data



\---



\# Key Exam Decision Rules



Shared Linux storage across instances:



```text

Amazon EFS

```



Windows + SMB + Active Directory:



```text

FSx for Windows File Server

```



Machine Learning + S3 + Massive Throughput:



```text

FSx for Lustre

```



Database Storage:



```text

EBS io2 Block Express

```



Archive Storage:



```text

S3 Glacier

```



\---



\# FinTrust Summary



FinTrust now uses:



\- EBS for databases

\- S3 for archives

\- EFS for shared Linux file access

\- FSx for Windows compliance shares

\- FSx for Lustre machine-learning workloads



This design balances performance, scalability, durability, and cost optimisation.

