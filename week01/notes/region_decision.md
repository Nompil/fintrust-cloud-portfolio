# FinTrust Region Decision — CPLG Framework

FinTrust operates in South Africa and must meet POPIA data residency requirements. For that reason, the primary AWS Region should be af-south-1, the Cape Town Region.

## CPLG Analysis

### Compliance
POPIA requires that personal financial data of South African citizens be processed and stored within South Africa. This makes af-south-1 the only suitable primary Region for live banking workloads.

### Proximity
FinTrust serves customers across South Africa, so deploying in the local Region reduces latency and aligns the architecture with the business footprint.

### Latency
The Cape Town Region provides the required AWS services for FinTrust's initial architecture, including EC2, RDS, Lambda, S3, and DynamoDB.

### Cost
Cost is relevant, but it is a secondary factor here. Compliance and proximity are more important than a lower-cost Region outside South Africa.

## Decision
The recommended primary Region is af-south-1 (Cape Town). It is the best fit for compliance, user proximity, and operational suitability.

## Multi-AZ Direction
FinTrust should run production workloads across at least two Availability Zones in af-south-1 to improve resilience and protect against single-AZ failures.
