# FinTrust Multi-Account Governance

FinTrust uses AWS Organizations and AWS Control Tower to separate production, security, and training workloads into different accounts. An AWS account is a security and billing boundary, while Organizational Units group accounts that need common governance.

## Account structure

The account hierarchy is shown in the [Week 1 architecture diagrams PDF](../diagrams/week01_architecture_diagrams.pdf).

| OU/account | Purpose | Main control |
| --- | --- | --- |
| Management account | Consolidated billing and organisation policy; no workloads | SCPs do not apply to the management account |
| Security / Log Archive | Central CloudTrail and AWS Config logs | Prevent modification or deletion of audit records |
| Security / Audit | Read-only security and compliance visibility | Detective controls report configuration drift |
| Production / `banking-prod` | ALB, Auto Scaling, messaging, data, and recovery workloads | Restrict deployments to approved Regions |
| Sandbox / `sandbox-training` | Experiments and training labs | Limit costly services and isolate the production blast radius |

Control Tower supplies the landing zone, Log Archive and Audit accounts, preventive and detective controls, and Account Factory for repeatable account provisioning. Organizations remains the underlying service for OUs, accounts, consolidated billing, and SCPs.

## SCP behaviour

An SCP sets the maximum permissions available in a member account. It does not grant access: an IAM identity still needs an allow policy. An explicit SCP deny cannot be overridden by an account administrator's IAM policy, and SCPs do not restrict the organisation's management account.

### Protect CloudTrail

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ProtectCloudTrail",
      "Effect": "Deny",
      "Action": [
        "cloudtrail:StopLogging",
        "cloudtrail:DeleteTrail"
      ],
      "Resource": "*"
    }
  ]
}
```

### Restrict requested Regions

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyUnapprovedRegions",
      "Effect": "Deny",
      "NotAction": [
        "cloudfront:*",
        "iam:*",
        "organizations:*",
        "route53:*",
        "support:*"
      ],
      "Resource": "*",
      "Condition": {
        "StringNotEquals": {
          "aws:RequestedRegion": [
            "af-south-1",
            "eu-west-1"
          ]
        }
      }
    }
  ]
}
```

The Region policy is an illustrative starting point. Global-service exemptions and Control Tower compatibility must be validated against the current AWS documentation before deployment.

## Four-step SAA question method

1. Identify the primary requirement, such as cost, availability, performance, or operational simplicity.
2. Identify constraints that eliminate whole solution categories.
3. Remove answers that violate a requirement or constraint.
4. Compare the remaining answers and choose the least complex option that fully satisfies the scenario.

Common traps include choosing the wrong architectural layer, over-engineering beyond the stated recovery objective, ignoring data-transfer cost, or keeping session state on instances that must scale horizontally.

## Week 1 architecture summary

FinTrust's Week 1 design uses `af-south-1` as the primary Region, Multi-AZ EC2 Auto Scaling behind an Application Load Balancer, SQS and SNS to decouple transaction processing, and a Pilot Light recovery plan with an RPO of 15 minutes and RTO below one hour. AWS Organizations and Control Tower place those workloads into governed production, security, and sandbox accounts with central logging and preventive controls.
