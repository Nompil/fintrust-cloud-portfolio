# Week 2: Compute, Storage, SQL, and Python

Week 2 applies workload characteristics to AWS compute and storage choices while extending the FinTrust SQL and Python exercises.

## Deliverables

### AWS architecture

- [Week 2 architecture diagrams PDF](diagrams/week02_architecture_diagrams.pdf)
- [Day 1 container architecture](container-architecture.md)
- [Day 2 Lambda design](lambda-design.md)
- [Day 2 compute decision map](compute-decision-map.md)
- Compute architecture in the [Week 2 architecture diagrams PDF](diagrams/week02_architecture_diagrams.pdf)
- [EBS storage decision](storage-decision.md)
- [Shared-storage decision](shared-storage-decision.md)
- [Week 2 compute notes and transaction flow diagram](architecture/week02_compute_notes.md)

### SQL

- [JOIN exercises](sql/day1_joins.sql)
- [Aggregate reporting](sql/day2_aggregates.sql)
- [Portfolio check-in JOIN file](sql/joins_practice.sql)
- [Portfolio check-in aggregate file](sql/aggregates_report.sql)
- [JOIN reference](notes/sql_join_reference.md)
- [Aggregate reference](notes/sql_aggregate_reference.md)

These queries target the `fintrust_db` MySQL schema created on Week 1 Day 3. Run `week01/sql/day3_fintrust_schema.sql` before the Week 2 SQL files.

### Verification

- [Day 1 and Day 2 MySQL verification](evidence/mysql-day1-day2-verification.md)

### Python

- [First Python script](hello_fintrust.py)
- [Functions and calculations](python/day3_exercises.py)
- [Conditional logic](python/conditionals.py)
- [Transaction assessment](python/transaction_flowchart.py)

Run the examples from the repository root:

```powershell
python week02\hello_fintrust.py
python week02\python\day3_exercises.py
python week02\python\conditionals.py
python week02\python\transaction_flowchart.py
```

## Week 2 check-in

The final check-in names are `sql/joins_practice.sql`, `sql/aggregates_report.sql`, `python/conditionals.py`, `python/transaction_flowchart.py`, and `architecture/week02_compute_notes.md`. The original day-based SQL files remain in the same folder because those are the filenames specified in the daily lab instructions.
