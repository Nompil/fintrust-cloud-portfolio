# Access-Denied Scenario Analysis

The Week 12 Day 2 course material supplies these three troubleshooting situations. This note records the policy reasoning. It does not claim that the IAM Policy Simulator, CloudTrail or an AWS sandbox was used.

## SCP-001: GuardDuty detector cannot be disabled

The account administrator receives AccessDenied when trying to disable a GuardDuty detector. The likely cause is an SCP attached above the member account that explicitly denies `guardduty:DeleteDetector`. The responsible layer is the organisation-level SCP, which limits permissions even for an administrator role. The right response is to confirm that the security guardrail is intentional and use the approved break-glass or security process if an exception is genuinely required. Removing the IAM administrator policy would not resolve an SCP deny.

## IAM-002: S3 objects can be read but not deleted

The role has `s3:DeleteObject` in its identity policy but still cannot delete objects. The supplied scenario points to an S3 bucket policy with an explicit deny for deletes outside approved non-production conditions. The responsible layer is the resource policy, and its explicit deny overrides the identity allow. The fix is not to add a broader IAM policy. The bucket-policy condition and environment classification must be reviewed, then changed only if deletion is allowed by the data-retention and change-control rules.

## PB-003: Administrator role cannot create IAM roles

The role has AdministratorAccess but cannot call `iam:CreateRole`. The likely cause is an attached permission boundary that does not allow the action. The boundary is the responsible layer because it limits the maximum permission available to the role. The appropriate fix is to have the identity or security team update the approved boundary if role creation is required, while keeping the boundary's privilege-escalation protections. Adding another identity policy would not extend permission beyond the boundary.
