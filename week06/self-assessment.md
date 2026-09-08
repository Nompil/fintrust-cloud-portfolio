# Week 6 Self-Assessment

**Date completed:** 14 August 2026
**Learner:** Nompilo Eugenia Mchunu

| Topic | Rating | Current confidence |
| --- | ---: | --- |
| Multi-AZ RDS and read replicas | 4 | I can separate availability from read scaling. |
| Disaster recovery strategies | 4 | I can compare backup and restore, Pilot Light, Warm Standby and active-active designs. |
| CloudWatch Agent | 3 | I know when memory, disk and application metrics need the agent. |
| CloudWatch alarm states | 3 | I understand `OK`, `ALARM` and `INSUFFICIENT_DATA`. |
| EventBridge response | 3 | I can explain how an EC2 state change can invoke Lambda. |
| IAM policy evaluation | 4 | I can trace explicit deny, SCPs, boundaries, identity policies and resource policies. |
| Permission boundaries | 4 | I can calculate the effective permission ceiling for a role. |
| STS credentials | 4 | I know why the access key, secret key and session token are all required. |
| Federation | 4 | I can distinguish workforce federation through IAM Identity Center from customer access through Cognito. |
| SCP scope | 4 | I know that SCPs do not restrict the management account. |
| Config and CloudTrail | 4 | I use Config for resource state and CloudTrail for API activity. |
| Secrets Manager and Parameter Store | 4 | I can choose between automatic rotation and lower-cost parameter storage. |
| ACM Regions | 4 | I know that a CloudFront certificate must be in `us-east-1`. |
| WAF and Shield | 4 | I can match application attacks and network DDoS attacks to the right service. |
| Session Manager | 4 | I can explain how it replaces a bastion host and what an instance needs. |
| GuardDuty response | 4 | I know GuardDuty detects findings while EventBridge and Lambda perform the response. |
| Security service selection | 4 | I can distinguish GuardDuty, Macie, Detective and Inspector. |
| CloudTrail data events | 4 | I know they are optional and add object-level or function-level activity. |
| VPC Flow Logs | 4 | I can read a flow log record and explain a `REJECT` action. |
| Penetration testing | 4 | I know that DDoS simulation must use an AWS-approved provider. |
| SQL analytics | 4 | I completed CTE, ranking, running-total and spending-spike queries. |
| boto3 automation | 3 | I can build paginated audit scripts with exception handling and encrypted S3 report output. |

The area I want to strengthen is testing boto3 automation against several AWS accounts without broadening the execution role. I will focus on least-privilege test roles, repeatable test data, and clear separation between read-only audit permissions and remediation permissions.
