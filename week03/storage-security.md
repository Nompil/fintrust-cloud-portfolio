# FinTrust S3 Security

FinTrust keeps all S3 buckets private. Access is granted to workload roles, not individual IAM users, and every request is encrypted in transit.

## Baseline controls

- Enable all four S3 Block Public Access settings at both account and bucket level.
- Use bucket-owner-enforced object ownership to disable ACLs.
- Encrypt sensitive objects with a customer-managed KMS key and restrict the key policy to approved roles.
- Require TLS through a bucket-policy deny statement.
- Record data events for sensitive buckets in AWS CloudTrail and centralise logs in the security account.
- Use short-lived pre-signed URLs only when a customer must download a statement directly.
- Enable AWS Config rules and Security Hub findings for continuous control checks.

## TLS-only transport policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyInsecureTransport",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::fintrust-transactions-af-south-1-*",
        "arn:aws:s3:::fintrust-transactions-af-south-1-*/*"
      ],
      "Condition": {
        "Bool": {
          "aws:SecureTransport": "false"
        }
      }
    }
  ]
}
```

Application and audit permissions belong in identity policies attached to their respective roles. This keeps the bucket policy focused on guardrails that apply to every principal.
