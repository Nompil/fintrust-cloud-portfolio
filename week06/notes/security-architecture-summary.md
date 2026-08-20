# Week 6 FinTrust Security Architecture Summary

**Date:** 14 August 2026
**Author:** Nompilo Eugenia Mchunu

## Availability and recovery

The production entry point is an Application Load Balancer spanning public subnets in `af-south-1a` and `af-south-1b`. An Auto Scaling Group maintains application instances in private subnets in both Availability Zones. Each Availability Zone has its own NAT Gateway so one NAT failure does not remove outbound access from both application subnets. The database uses RDS Multi-AZ for automatic failover. The recovery strategy is Pilot Light in `eu-west-1`, with an RPO of 15 minutes and an RTO below one hour. CloudWatch alarms cover ALB errors, EC2 utilisation, and RDS connections, while the CloudWatch Agent supplies memory and disk metrics that EC2 does not publish by default.

## Identity and access

Employees use IAM Identity Center with Active Directory instead of separate IAM users in every account. Customers authenticate through Cognito and receive short-lived STS credentials limited to their own S3 prefix. AWS workloads use service roles rather than access keys. Service Control Policies prevent unapproved Region use in member accounts, while permission boundaries keep DevOps-created roles within the security team's approved ceiling. Explicit denies remain final at every layer.

## Preventive and detective controls

Control Tower manages the landing zone and applies preventive SCP controls and detective Config controls. AWS Config evaluates twelve controls covering encryption, public access, logging, Multi-AZ, and MFA. Secrets Manager rotates database and payment credentials, ACM supplies managed certificates in the correct Regions, and WAF protects CloudFront and the ALB from SQL injection, XSS, and abusive request rates. SSM Session Manager replaces bastion hosts and records administrator sessions without opening inbound SSH.

## Detection and response

CloudTrail provides the API audit record and explicitly records S3 data events for protected buckets. VPC Flow Logs provide network metadata for connection investigations. GuardDuty findings with severity 7 or higher trigger EventBridge and Lambda to isolate the affected instance and notify the security team. Macie discovers PII in S3, Inspector reports software vulnerabilities, and Detective supports root-cause investigation. These services cover different questions, so none is treated as a replacement for another.

## Overall position

The design combines resilience, access control, compliance evidence, and automated response. It keeps live banking workloads in South Africa, reduces standing credentials and open management ports, and gives the security team evidence about configuration state, API actions, network traffic, sensitive data, and software vulnerabilities. The remaining operational requirement is regular recovery and incident-response testing so the stated RPO, RTO, and isolation targets are measured rather than assumed.
