# Week 12 Multi-Account Governance

## FinTrust organisation structure

The course scenario places shared networking, security and log archive accounts in an Infrastructure OU. Workload accounts sit in separate Production and Non-Production OUs. Sandbox accounts have tighter cost controls because they are intended for temporary development work. AWS accounts are the isolation boundary; an OU is the place where shared policy is attached.

The management account owns billing and cannot be constrained by an SCP. It should not host application workloads. Member-account access is limited by the intersection of the identity policy, relevant resource policy, permission boundary and SCP. Any explicit deny wins.

## Included guardrails

The approved-region policy denies requests outside `af-south-1` and `eu-west-1`. The audit-control policy prevents deletion of CloudTrail and GuardDuty controls. These are sample guardrails based on the course scenario. They are not attached to an AWS Organisation from this repository.

## Access-denied method

When an access request fails, start with the error wording. An explicit deny points to an SCP or resource-policy deny. Then check the effective SCP, permission boundary, identity policy and any resource policy. For cross-account S3 access, the caller's identity policy and the target bucket policy must both allow the request. The IAM Policy Simulator does not show SCP evaluation, so the effective policy must be checked in Organizations.
