# FinTrust Security Services Configuration

**Date:** 12 August 2026
**Author:** Nompilo Eugenia Mchunu

## Configuration summary

| Service | FinTrust configuration | Reason and trade-off |
| --- | --- | --- |
| AWS Config | Twelve managed rules record compliance state and send non-compliant findings for remediation | Config answers whether a resource is compliant now. Recording and rule evaluations add cost, but they provide evidence for continuous POPIA control monitoring. |
| Trusted Advisor | Business support plan with the full security, cost, performance, fault-tolerance, and service-limit checks | Trusted Advisor recommends improvements but does not enforce them. Config remains the compliance control. |
| Control Tower | Four-account landing zone with Management, Log Archive, Audit, and Production accounts | Control Tower standardises account creation and deploys preventive SCP controls and detective Config controls. |
| Secrets Manager | RDS credentials rotate every 30 days. Payment API credentials rotate every 90 days. | It costs more than Parameter Store, but built-in rotation is required for these credentials. |
| Parameter Store | Non-secret feature flags, log levels, and application settings | The standard tier is suitable for configuration that does not need automatic secret rotation. |
| ACM | CloudFront certificate in `us-east-1`. ALB certificate in `af-south-1`. Automatic renewal enabled. | CloudFront has a fixed certificate Region requirement. The ALB certificate stays in the ALB Region. |
| AWS WAF | Web ACL on CloudFront and the ALB. AWS managed SQL injection and XSS rules. Rate rule blocks more than 1,000 requests in five minutes from one IP. | WAF inspects Layer 7 requests. It does not replace Shield protection against network and transport DDoS attacks. |
| Shield Advanced | EC2, ALB, CloudFront, and Route 53 resources enrolled | FinTrust accepts the additional cost for DDoS Response Team access and financial protection during an attack. |
| Firewall Manager | Central policy for WAF and Shield across the organisation | Security controls stay consistent when new accounts are created. |
| SSM Session Manager | All EC2 administration uses Session Manager. Port 22 is closed. Sessions are logged to CloudWatch Logs and S3. | This removes bastion hosts and SSH keys while providing an audit record. Instances need the SSM Agent, an instance role, and outbound access to SSM endpoints. |

## AWS Config managed rules

| Rule | Control checked |
| --- | --- |
| `s3-bucket-server-side-encryption-enabled` | S3 default encryption is enabled |
| `s3-bucket-public-read-prohibited` | S3 public reads are blocked |
| `s3-bucket-public-write-prohibited` | S3 public writes are blocked |
| `s3-bucket-logging-enabled` | S3 access logging is enabled where required |
| `s3-bucket-versioning-enabled` | Protected buckets use versioning |
| `encrypted-volumes` | Attached EBS volumes are encrypted |
| `rds-storage-encrypted` | RDS storage is encrypted |
| `rds-multi-az-support` | Production RDS is configured for Multi-AZ |
| `root-account-mfa-enabled` | Root account MFA is enabled |
| `iam-user-mfa-enabled` | IAM console users have MFA |
| `cloudtrail-enabled` | A CloudTrail trail is operating |
| `vpc-flow-logs-enabled` | VPC Flow Logs are enabled |

## Session Manager connection requirements

The EC2 instance must run the SSM Agent and use an instance role containing `AmazonSSMManagedInstanceCore`. Private subnets reach Systems Manager through NAT or VPC interface endpoints for SSM, SSM Messages, and EC2 Messages. No inbound SSH or RDP rule is required.
