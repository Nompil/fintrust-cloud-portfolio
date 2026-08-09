# FinTrust Region Decision — CPLG Framework Analysis

## Scenario
FinTrust Bank serves 2.3 million South African customers. It processes card transactions, mobile payments, and account queries. POPIA (Protection of Personal Information Act) requires that personal financial data of South African citizens must be processed and stored within South Africa.

## CPLG Analysis

### Compliance (C) — Highest Priority
POPIA mandates South African data residency. This is non-negotiable. Only **af-south-1 (Cape Town)** qualifies as an AWS Region within South Africa.

### Proximity (P)
All 2.3 million FinTrust customers are in South Africa (across all nine provinces). Deploying in `af-south-1` places the infrastructure geographically closest to users, minimising latency for transaction processing.

### Latency (L)
`af-south-1` has all required AWS services for FinTrust: EC2 (compute), RDS (databases), Lambda (serverless), S3 (storage), DynamoDB (NoSQL). No service gaps exist.

### Go-live Cost (G)
`af-south-1` is approximately 20–30% more expensive than `us-east-1` (US East), but this is a tie-breaker only. Compliance and proximity override cost.

## Decision
**Primary Region: af-south-1 (Cape Town)**

**Justification:** Compliance first (POPIA), supported by proximity to all nine provinces and acceptable latency. Cost is not a factor here — legal compliance is non-negotiable.

## Multi-AZ Strategy
`af-south-1` has 3 availability zones: `af-south-1a`, `af-south-1b`, `af-south-1c`. FinTrust's production systems will be deployed across at least 2 AZs for high availability and automatic failover. This protects against single data centre failures.
