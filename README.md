# FinTrust Cloud Portfolio

**Learner:** Nompilo Eugenia Mchunu

**Programme:** Cloud to Solutions Accelerator (16 weeks)

**Target certification:** AWS Certified Solutions Architect Associate (SAA-C03)

**Cohort start:** 6 July 2026

## About

This repository records my practical work for the FinTrust Bank case study. It brings together AWS architecture decisions, MySQL and PostgreSQL exercises, Python automation, and a small transaction-data pipeline.

The current repository contains completed portfolio work from Weeks 1 to 7.

## Portfolio map

| Week | Focus | Highlights |
| --- | --- | --- |
| [Week 1](week01/) | Cloud and SQL foundations | AWS infrastructure, EC2, resilience, governance, schema design, and filtering |
| [Week 2](week02/) | Compute, storage, SQL joins, Python | Compute decisions, JOIN and aggregate queries, transaction rules |
| [Week 3](week03/) | S3 and Python automation | Storage design, reusable functions, CSV cleaning, JSON reporting, logging |
| [Week 4](week04/) | Databases and data pipelines | Transaction validation, SQLite loading, reporting, pandas analysis |
| [Week 5](week05/) | AWS networking | VPC design, connectivity, Route 53, and CloudFront |
| [Week 6](week06/) | Security, identity, observability, and analytics | Highly available architecture, IAM, threat response, PostgreSQL analytics, and boto3 audits |
| [Week 7](week07/) | Messaging, APIs, Lambda, and infrastructure as code | SQS, SNS, EventBridge, Step Functions, Flask, FastAPI, Lambda, and CloudFormation |

## FinTrust scenario

FinTrust is a South African digital bank serving 2.3 million customers across all nine provinces. Its systems currently run in two on-premises data centres in Johannesburg and Cape Town. The bank needs to address four pressures:

- customer growth towards five million customers by 2027
- POPIA requirements for data residency and access logging
- increasing card fraud requiring real-time transaction monitoring
- transaction latency of three to five seconds during peak periods

The assignment is to design and progressively build a cloud-native transaction intelligence system on AWS. The primary deployment Region is `af-south-1` (Cape Town), with production workloads distributed across multiple Availability Zones.

## Run the code

The Week 1 and Week 2 SQL exercises target MySQL 8. Week 6 uses PostgreSQL for CTE and window-function practice. The course uses a supplied `fintrust` sample database on Week 1 Day 2 and a learner-built `fintrust_db` schema from Day 3 onward. The [Week 1 README](week01/) and [Week 6 README](week06/) give the correct execution order.

The Python examples require Python 3.10 or later:

```powershell
python week02\hello_fintrust.py
python week03\python\test_utils.py
python week03\python\clean_transactions_v2.py
python week04\run_smoke_tests.py
python week06\python\test_week06_audits.py
python -m unittest week07.tests.test_week07 -v
```

Week 4 analysis uses pandas:

```powershell
python -m pip install -r week04\requirements.txt
python week04\analyse.py
```

Generated SQLite databases, logs, virtual environments, and Python cache files are excluded from version control.

## Skills demonstrated

- AWS architecture: Regions, Availability Zones, EC2, Lambda, containers, S3, RDS, VPC, Route 53, CloudFront, IAM, messaging, APIs, and security services
- SQL: schema design, constraints, filtering, joins, aggregation, CTEs, window functions, and reporting
- Python: functions, validation, exceptions, logging, CSV/JSON processing, SQLite, pandas, boto3, Flask, and FastAPI
- Engineering practice: clear project structure, reproducible run instructions, diagrams, and small validation scripts

## Architecture diagram packs

- [Week 1 architecture diagrams PDF](week01/diagrams/week01_architecture_diagrams.pdf)
- [Week 2 architecture diagrams PDF](week02/diagrams/week02_architecture_diagrams.pdf)
- [Week 3 architecture diagrams PDF](week03/diagrams/week03_architecture_diagrams.pdf)
- [Week 4 pipeline architecture PDF](week04/diagrams/week04_pipeline_architecture.pdf)
- [Week 5 VPC architecture PDF](week05/diagrams/week05_vpc_architecture.pdf)
- [Week 6 architecture diagrams PDF](week06/diagrams/week06_architecture_diagrams.pdf)
- [Week 7 architecture diagrams PDF](week07/diagrams/week07_architecture_diagrams.pdf)

## Certification target

AWS Certified Solutions Architect Associate (SAA-C03)
