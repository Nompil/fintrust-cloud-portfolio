# FinTrust Incident Response and Audit Design

**Date:** 13 August 2026
**Author:** Nompilo Eugenia Mchunu

## Automated GuardDuty response

FinTrust enables GuardDuty in every governed account and Region. GuardDuty detects suspicious behaviour but does not block it. A high-severity finding follows this response path:

1. GuardDuty publishes the finding to EventBridge.
2. An EventBridge rule matches GuardDuty findings with severity 7 or higher.
3. A Lambda function reads the affected EC2 instance ID.
4. Lambda replaces the instance Security Groups with the approved isolation Security Group.
5. Lambda creates an EBS snapshot for forensic preservation and publishes a notification to the security SNS topic.
6. The security team investigates the finding in Amazon Detective.

The target is automatic isolation within three minutes. The isolation role allows only the EC2 actions needed for containment, the snapshot action, and publishing to the named SNS topic.

## Simulated GuardDuty finding

This record is a simulation used to verify the response design. It is not presented as evidence from a live AWS account.

| Field | Value |
| --- | --- |
| Finding type | `UnauthorizedAccess:EC2/TorIPCaller` |
| Severity | `8.0 High` |
| Resource | `i-0f17a6c2b4e8d9012` |
| Account | `111122223333` |
| Region | `af-south-1` |
| Expected response | EventBridge invokes the isolation Lambda function |
| Completion target | Instance isolated and security team notified within three minutes |

## VPC Flow Log interpretation

Sample record using AWS documentation address ranges:

```text
2 111122223333 eni-0abc1234 203.0.113.25 10.0.11.15 51522 22 6 1 60 1723540500 1723540560 REJECT OK
```

| Field | Interpretation |
| --- | --- |
| Source | `203.0.113.25` attempted the connection |
| Destination | Private address `10.0.11.15` |
| Destination port | Port 22, SSH |
| Protocol | `6`, TCP |
| Action | `REJECT`, so the Security Group or network ACL blocked the traffic |
| Bytes | 60 bytes of flow metadata were recorded; packet contents are not captured |

The rejection shows the network controls prevented the connection. It does not identify the IAM user or API action. CloudTrail is used for that separate question.

## CloudTrail configuration

FinTrust uses a multi-Region trail that writes to the Log Archive account. Log file validation and S3 Object Lock protect the audit record. Management events are recorded, and S3 data events are enabled for the transaction and customer-document buckets so object-level access can be investigated. CloudTrail events also stream to CloudWatch Logs for root-user and policy-change alerts.

## Threat detection responsibilities

| Service | FinTrust use |
| --- | --- |
| GuardDuty | Detect compromised resources and unusual account activity |
| Macie | Run weekly PII discovery against customer-document S3 buckets |
| Detective | Investigate GuardDuty findings and correlated behaviour |
| Inspector | Scan EC2 packages and ECR images for CVEs |

## Penetration testing rule

FinTrust may test its own permitted AWS resources without requesting approval from AWS. It may not perform DNS zone walking, request flooding, or tests that affect other customers. Any DDoS simulation must use an AWS-approved third-party provider.
