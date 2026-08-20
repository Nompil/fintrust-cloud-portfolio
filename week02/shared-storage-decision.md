# FinTrust Shared Storage Decision

## Overview

FinTrust now uses all three primary AWS storage categories:

- Block storage for single-instance workloads using EBS
- Object storage for durable archives using S3
- File storage for shared access using EFS and FSx

That combination matches the different workloads in the bank's platform.

## Storage choices for FinTrust

| Component | Storage service | Configuration | Why it fits |
|---|---|---|---|
| Transaction database | EBS io2 Block Express | High-performance block storage | Best fit for a relational database that needs low-latency, durable storage attached to one instance |
| Transaction statement archive | S3 Glacier Instant Retrieval | Object storage | Ideal for long-term retention and cost-efficient archive storage |
| Fraud model files | Amazon EFS | General Purpose performance, Elastic throughput | Multiple Lambda functions and ECS tasks need to read the same shared files |
| Compliance document shares | FSx for Windows File Server | SMB and Active Directory integration | Windows-based teams need shared folders with permissions and domain-based access |
| Fraud model training cache | FSx for Lustre | Scratch deployment linked to S3 | High-throughput, low-latency storage for ML training workloads |

## Three storage types in one architecture

- Block storage: EBS for databases and boot volumes
- Object storage: S3 for archives and long-term retention
- File storage: EFS and FSx for shared access across services and teams

This is the clearest way to think about the design: each storage type solves a different access pattern.

## Shared storage architecture

The shared storage layout is shown in the [Week 2 architecture diagrams PDF](diagrams/week02_architecture_diagrams.pdf).

EFS serves the Linux-based Lambda and ECS workloads through NFS. FSx for Windows supplies SMB shares and Active Directory permissions. FSx for Lustre supplies the parallel throughput needed for model training and can exchange data with S3.
