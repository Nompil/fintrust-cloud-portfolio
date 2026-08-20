# FinTrust Region Decision: CPLG Framework

The programme scenario requires FinTrust's personal financial data to remain in South Africa. On that basis, the primary AWS Region should be `af-south-1` (Cape Town).

## CPLG Analysis

### Compliance
The stated data-residency requirement makes `af-south-1` the only suitable primary Region for live banking workloads in this case study. A real implementation would require FinTrust's legal and compliance teams to confirm the exact POPIA and cross-border processing obligations.

### Proximity
FinTrust serves customers across South Africa, so deploying in the local Region reduces latency and aligns the architecture with the business footprint.

### Latency
The Cape Town Region provides the required AWS services for FinTrust's initial architecture, including EC2, RDS, Lambda, S3, and DynamoDB.

### Cost
Cost is relevant, but it is a secondary factor here. Compliance and proximity are more important than a lower-cost Region outside South Africa.

## Decision
The recommended primary Region is `af-south-1` (Cape Town). It is the best fit for the scenario's compliance requirement, user proximity, and operational needs.

## Multi-AZ Direction
FinTrust should run production workloads across at least two Availability Zones in af-south-1 to improve resilience and protect against single-AZ failures.
