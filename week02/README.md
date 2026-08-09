# Week 02 – Compute, Storage, SQL & Python Fundamentals

## What I Built

- SQL JOIN exercises using the FinTrust banking dataset
- Aggregate queries using COUNT, SUM, AVG, GROUP BY and HAVING
- Python conditional logic exercises
- A transaction decision engine for fraud detection
- AWS compute architecture notes
- AWS storage architecture notes
- Lambda, container, and shared-storage documentation

---

## Key Concepts Demonstrated

### SQL

- INNER JOIN
- LEFT JOIN
- GROUP BY
- HAVING
- Aggregate functions

### Python

- Variables and data types
- Decimal for monetary values
- Functions
- Conditional logic
- Boolean operators
- Transaction decision engines

### AWS Compute

- EC2
- ECS Fargate
- Lambda
- Elastic Beanstalk
- AWS Batch

### AWS Storage

- EBS gp3
- EBS io2 Block Express
- Amazon EFS
- Amazon FSx
- Amazon S3 Glacier

---

## How to Run

### SQL

Run the SQL files in SQLite or MySQL.

```sql
.read sql/joins_practice.sql
.read sql/aggregates_report.sql
```

### Python

```powershell
python python\conditionals.py
python python\transaction_flowchart.py
```

---

## FinTrust Context

These exercises form part of the FinTrust Bank cloud architecture project.

The project simulates a South African digital bank operating in:

```text
af-south-1 (Cape Town)
```

and focuses on cloud architecture, security, automation, governance and software development.

---

## Files

### SQL

- sql/joins_practice.sql
- sql/aggregates_report.sql

### Python

- python/conditionals.py
- python/transaction_flowchart.py

### Notes

- architecture/week02_compute_notes.md
- notes/container-architecture.md
- notes/lambda-design.md
- notes/compute-decision-map.md
- notes/storage-decision.md
- notes/shared-storage-decision.md