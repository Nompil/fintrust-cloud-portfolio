# FinTrust Storage Decision Notes

Storage is one of those topics that becomes much clearer once I connect it to the workload. A banking platform does not need just one kind of storage. It needs the right storage type for the right job.

## The main difference between storage options

I think of it this way:

- EBS is for block storage attached to a single EC2 instance
- S3 is for object storage and long-term archive use
- EFS is for shared file storage that can be mounted by multiple services

That distinction matters because the same data cannot always be placed on the same storage type just because it is technically possible.

## EBS for mission-critical workloads

EBS is the right fit for workloads that need persistent, low-latency storage attached to an instance. For FinTrust, that is useful for application servers and the transactional database layer.

### gp3

This is the default choice for general-purpose storage. It is practical for web-facing application servers and operating system volumes.

### io2 Block Express

This is the premium option. It is used when the workload needs very high IOPS, predictable performance, and the highest durability. That is why it is the better fit for a transaction database.

## S3 for archives and durable object storage

S3 is better for data that needs to be retained safely but does not need to behave like a mounted disk. For FinTrust, it is a strong fit for transaction history archives and long-term retention.

## EFS for shared access

EFS matters when multiple services need to read the same files. That makes it useful for shared model files or other data that needs to be accessed by more than one application component.

## FinTrust storage mapping

- Transaction API web tier: EBS gp3
- RDS transaction database: EBS io2 Block Express
- Old transaction history: S3 Glacier or S3 Standard depending on access frequency
- Shared ML model files: EFS
- Backup and recovery: EBS snapshots managed through lifecycle policies

## My takeaway

The storage decisions for FinTrust are really about matching the data access pattern to the storage model. High-performance transactional data needs EBS. Long-term archives need S3. Shared file access needs EFS.
