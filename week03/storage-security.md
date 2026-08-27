# FinTrust S3 Security

FinTrust keeps the transaction, statement and machine-learning buckets private. Application roles receive only the actions they need, while the bucket policy enforces rules that apply to every principal.

## Security choices

| Control | FinTrust decision | Reason |
| --- | --- | --- |
| Public access | Enable all four Block Public Access settings | Customer and transaction data must not be anonymously accessible |
| Object ownership | Bucket owner enforced | ACLs are disabled and access is controlled with policies |
| Encryption | SSE-KMS with a customer-managed key | Key use is recorded and access can be limited to approved roles |
| Network transport | Deny requests that do not use TLS | Data is protected while travelling to and from S3 |
| Temporary downloads | Short-lived pre-signed URLs | A customer can download one statement without receiving S3 permissions |
| Audit trail | CloudTrail data events for sensitive buckets | Object reads and writes can be investigated |

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
        "arn:aws:s3:::fintrust-transactions-af-south-1",
        "arn:aws:s3:::fintrust-transactions-af-south-1/*"
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

An application role would receive its normal `s3:GetObject` or `s3:PutObject` permissions through an IAM policy. The explicit deny above still overrides an allow when the request does not use HTTPS.

## Pre-signed URL use case

When a customer requests a monthly statement, the portal checks that the statement belongs to that customer. The backend then creates a pre-signed `GetObject` URL with a short expiry. The link uses the permissions of the signing role, so the role is restricted to the statement prefix and the bucket remains private.

These controls support POPIA by limiting access to personal information, encrypting the records, and keeping an audit trail of object and KMS activity.
