\# FinTrust Multi-Account Governance



\## Overview



FinTrust uses AWS Organizations to separate production workloads, security services, governance controls, and training environments into dedicated accounts.



This approach improves security, compliance, auditing, and operational management.



\---



\# Organizational Units (OUs)



\## Management OU



\### Account



\- Management



\### Purpose



\- Consolidated billing

\- Organization-wide governance

\- Service Control Policy (SCP) management



\### Notes



No workloads run in this account.



\---



\## Security OU



\### Log Archive Account



Purpose:



\- Centralized CloudTrail logs

\- Centralized AWS Config logs

\- Long-term audit retention



\### Audit Account



Purpose:



\- Read-only access for compliance teams

\- Security reviews and investigations



\---



\## Production OU



\### Account



\- banking-prod



\### Purpose



Hosts all FinTrust production workloads.



\### Services



\- Auto Scaling Groups (ASG)

\- Application Load Balancers (ALB)

\- Amazon RDS

\- Amazon SQS

\- Amazon SNS

\- Pilot Light Disaster Recovery



\---



\## Sandbox OU



\### Account



\- sandbox-training



\### Purpose



\- Experimentation

\- Learning

\- Training labs

\- Testing new solutions



\---



\# Service Control Policies (SCPs)



\## Region Restriction SCP



Allowed Regions:



\- af-south-1 (Cape Town)

\- eu-west-1 (Ireland)



\### Purpose



Supports:



\- POPIA data residency requirements

\- Disaster recovery strategy

\- Governance controls



\---



\## CloudTrail Protection SCP



Denied Actions:



\- cloudtrail:StopLogging

\- cloudtrail:DeleteTrail



\### Purpose



Prevents audit logging from being disabled or deleted.



\---



\# FinTrust Benefits



\## Security



Separate accounts reduce risk and limit access.



\## Compliance



Audit and Log Archive accounts support regulatory requirements.



\## Governance



Service Control Policies enforce organization-wide standards.



\## Disaster Recovery



EU-West-1 supports Pilot Light Disaster Recovery.



\## Scalability



Multiple accounts allow FinTrust to grow safely and efficiently.



\---



\# FinTrust Governance Structure



Management Account

│

├── Security OU

│   ├── Log Archive

│   └── Audit

│

├── Production OU

│   └── banking-prod

│

└── Sandbox OU

&#x20;   └── sandbox-training



\---



\# Week 1 Summary



This week introduced the foundational concepts required to build the FinTrust cloud architecture.



Key topics included:



\- AWS Regions and Availability Zones

\- Edge Locations and CloudFront

\- Multi-AZ resilience

\- EC2 compute design

\- Auto Scaling Groups

\- Application Load Balancers

\- SQS and SNS messaging

\- Disaster Recovery strategies

\- AWS Organizations and governance

\- FinTrust data model design



These concepts form the foundation of the final FinTrust cloud-native banking platform.

