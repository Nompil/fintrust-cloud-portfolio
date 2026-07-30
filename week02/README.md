# Week 02 – Compute, Storage, SQL & Python Fundamentals

## What I Built

- SQL JOIN exercises using the FinTrust banking dataset
- Aggregate queries using COUNT, SUM, AVG, GROUP BY and HAVING
- Python conditional logic exercises
- A transaction decision engine for fraud detection
- AWS compute architecture notes
- AWS storage architecture notes
- Lambda and container architecture documentation

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

Open the SQL files in SQLite or MySQL.

```sql
.read day1_joins.sql
.read day2_aggregates.sql
```

### Python

```powershell
python python\conditionals.py

python python\day3_exercises.py

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

- day1_joins.sql
- day2_aggregates.sql

### Python

- conditionals.py
- day3_exercises.py
- transaction_flowchart.py

### Notes

- container-architecture.md
- lambda-design.md
- compute-decision-map.md
- storage-decision.md
- shared-storage-decision.md
- python-environment.md
- conditionals-reference.md