# FinTrust S3 Storage Design

## Bucket strategy

| Data | Bucket naming base | Controls | Lifecycle |
| --- | --- | --- | --- |
| Transaction records | `fintrust-transactions-af-south-1` | Versioning, SSE-KMS, Object Lock compliance mode | Standard, then Standard-IA after 30 days, Glacier Instant Retrieval after 90 days, and Deep Archive after 365 days |
| Customer statements | `fintrust-statements-af-south-1` | Versioning, SSE-KMS, Block Public Access | Standard, then Standard-IA after 30 days and Glacier Flexible Retrieval after 365 days |
| Fraud-model data | `fintrust-ml-data-af-south-1` | Versioning, SSE-KMS, bucket-owner-enforced object ownership | Intelligent-Tiering for data with uncertain access patterns |
| Audit logs | `fintrust-audit-logs-af-south-1` | Dedicated log account, SSE-KMS, Object Lock | Retention follows the approved compliance schedule |

The deployment process appends the AWS account ID to each naming base so that the final bucket name is globally unique. Retention periods and deletion rules require approval from FinTrust's legal and records-management teams.

## Design decisions

- Keep customer and transaction data in `af-south-1` unless a documented legal decision permits cross-Region replication.
- Enable versioning before configuring Object Lock. Object Lock can only be used on versioned buckets.
- Use compliance mode only for records with an approved immutable retention requirement; governance mode permits authorised users to bypass retention.
- Apply lifecycle rules to current and noncurrent object versions so old versions do not create uncontrolled storage cost.
- Use S3 Inventory and Storage Lens to confirm that encryption, lifecycle, and retention controls remain effective.

## Cost approach

The storage-class choice depends on object size, retrieval frequency, minimum storage duration, and retrieval charges. A cost estimate should use measured data volumes and access patterns.
