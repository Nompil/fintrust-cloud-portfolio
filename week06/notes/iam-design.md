# FinTrust IAM Design Decision

**Date:** 11 August 2026
**Author:** Nompilo Eugenia Mchunu

## Employee console access

FinTrust uses IAM Identity Center connected to the corporate Active Directory for 300 employees. Staff sign in with their existing company credentials and receive permission sets according to their role. Developers receive access to the development account, analysts receive read-only access to the data account, and administrators remain within the limits imposed by the organisation controls. FinTrust does not create an IAM user in every account for each employee.

This design gives the bank one place to add, remove, and review workforce access. When someone changes teams or leaves the company, the Active Directory group change is reflected across the assigned AWS accounts.

## Customer access to S3

The mobile banking application uses a Cognito User Pool to authenticate 100,000 customers. The User Pool supports sign-in, MFA, and token issuance. A Cognito Identity Pool exchanges the authenticated customer token for temporary STS credentials associated with a restricted IAM role.

The customer role permits S3 access only to the prefix belonging to that customer. The application therefore avoids long-lived access keys and does not create IAM users for retail customers. The temporary credentials contain an access key ID, a secret access key, and a session token. All three values are required.

## DevOps permission boundary

The DevOps team can create roles for Lambda functions and ECS tasks, but every role it creates must use the approved permission boundary. The boundary prevents the team from creating a role with more authority than the security team has allowed. An identity policy may request broad permissions, but the effective permissions remain inside the intersection of the identity policy and the boundary.

This control is aimed at privilege escalation. It is not a replacement for an identity policy and does not grant any permission by itself.

## Policy evaluation chain

The detailed evaluation diagram is in the Week 6 architecture PDF. The review order used for the FinTrust design is:

1. Check every applicable policy for an explicit deny. A deny is final.
2. Check the Service Control Policy for the member account. The SCP establishes the organisation-level ceiling.
3. Check any permission boundary attached to the principal. The boundary creates a second ceiling.
4. Evaluate the identity, session, and resource policies that apply to the request.
5. Allow the request only when an applicable policy allows it and none of the ceilings or explicit denies remove it.

SCPs apply to member accounts, not the AWS Organizations management account. FinTrust keeps production workloads out of the management account for this reason.

## Decision summary

| User group | Identity service | Credential type | Access scope |
| --- | --- | --- | --- |
| Employees | IAM Identity Center and Active Directory | Temporary role credentials | Permission set for assigned accounts |
| Retail customers | Cognito User Pool and Identity Pool | Temporary STS credentials | Customer-specific S3 prefix |
| DevOps team | IAM Identity Center role with permission boundary | Temporary role credentials | Development actions within the approved boundary |
| AWS workloads | EC2 instance roles, ECS task roles, and Lambda execution roles | Temporary role credentials | Least-privilege service access |
