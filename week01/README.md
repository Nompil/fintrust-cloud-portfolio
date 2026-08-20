# Week 1: Cloud and SQL Foundations

Week 1 introduced the FinTrust case study, AWS global infrastructure, EC2 workload decisions, resilient architecture, multi-account governance, relational data modelling, and foundational MySQL queries.

## What I learned

### AWS and architecture

- Day 1: programme structure, FinTrust requirements, AWS Skills Builder, and the portfolio workflow
- Day 2: Regions, Availability Zones, Edge Locations, and the `af-south-1` decision
- Day 3: AMIs, EC2 instance families, Placement Groups, pricing models, Lambda, and ECS
- Day 4: Auto Scaling, load balancing, SQS/SNS decoupling, and RTO/RPO-based disaster recovery
- Day 5: AWS Organizations, SCPs, Control Tower, and the four-step SAA question method

### SQL

- Relational tables, keys, constraints, and appropriate data types
- `CREATE TABLE`, `INSERT`, `SELECT`, aliases, calculations, ordering, and limits
- Filtering with comparison operators, `LIKE`, `IN`, `BETWEEN`, `IS NULL`, `AND`, `OR`, and `NOT`

## Deliverables

- [Week 1 architecture diagrams PDF](diagrams/week01_architecture_diagrams.pdf)
- [Day 1 reflection](notes/day1_reflection.md)
- [AWS Region decision](notes/region_decision.md)
- [EC2 compute decisions](notes/ec2-compute-decisions.md)
- [Resilience and disaster recovery](notes/resilience-and-dr-plan.md)
- [Multi-account governance](notes/multi-account-governance.md)
- [FinTrust data model](notes/fintrust_data_model.md)
- Entity-relationship diagram in the [Week 1 architecture diagrams PDF](diagrams/week01_architecture_diagrams.pdf)
- [Day 2 sample database](sql/day2_fintrust_sample_data.sql)
- [Database schema and sample data](sql/day3_fintrust_schema.sql)
- [Branches stretch challenge](sql/day3_challenge_branches.sql)
- [Basic SELECT exercises](sql/day2_basic_select.sql)
- [Data exploration queries](sql/day2_explore.sql)
- [WHERE exercises](sql/day4_where_queries.sql)
- [WHERE challenges](sql/day4_where_challenges.sql)

## Learner evidence

- [Week 1 self-assessment](self-assessment-week01-NompiloEugeniaMchunu.pdf)
- [Self-assessment source](self-assessment-week01-NompiloEugeniaMchunu.md)
- [Cloud Quest reflection](notes/cloud_quest_reflection.md)
- [MySQL verification record](evidence/mysql-verification.md)

## Architecture decision

FinTrust uses `af-south-1` as its primary AWS Region. The decision is driven first by South African data-residency requirements and then by proximity to the bank's customers. Production services should use at least two Availability Zones to avoid a single-AZ failure.

## Run the SQL

The scripts target MySQL 8. The LMS uses two databases during the week: the supplied Day 2 sample uses `fintrust`, while the Day 3 learner-built schema and later exercises use `fintrust_db`.

Day 2:

1. `sql/day2_fintrust_sample_data.sql`
2. `sql/day2_explore.sql`
3. `sql/day2_basic_select.sql`

Day 3 onward:

1. `sql/day3_fintrust_schema.sql`
2. `sql/day3_challenge_branches.sql` (optional stretch)
3. `sql/day4_where_queries.sql`
4. `sql/day4_where_challenges.sql`

Both setup scripts rebuild only their named lab tables so the exercises are reproducible.
