# FinTrust Multi-Account Governance

FinTrust uses AWS Organizations to separate production workloads, security, governance, and training environments into dedicated accounts. This approach improves security, compliance, auditing, and operational management.

## Organizational Units

### Management OU
- Account: Management
- Purpose: consolidated billing and organization-wide governance
- Note: no workloads run in this account

### Security OU
- Log Archive Account: centralised CloudTrail and AWS Config logs
- Audit Account: read-only access for compliance and security review

### Production OU
- Account: banking-prod
- Purpose: host all production workloads
- Services: Auto Scaling Groups, Application Load Balancers, Amazon RDS, Amazon SQS, Amazon SNS, and Pilot Light DR

### Sandbox OU
- Account: sandbox-training
- Purpose: experimentation, learning, and test environments

## Service Control Policies

### Region Restriction SCP
Allowed Regions:
- af-south-1 (Cape Town)
- eu-west-1 (Ireland)

Purpose:
- support POPIA data residency requirements
- support disaster recovery strategy
- enforce governance boundaries

### CloudTrail Protection SCP
Denied actions:
- cloudtrail:StopLogging
- cloudtrail:DeleteTrail

This protects the audit trail and ensures compliance controls remain active across the organization.



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

