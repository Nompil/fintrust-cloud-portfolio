# Week 1 — Foundation

This week established the core foundation for the FinTrust portfolio: AWS cloud concepts, relational database design, SQL querying, and professional GitHub documentation.

## What I Learned

- AWS global infrastructure: Regions, Availability Zones, and Edge Locations
- EC2 compute choices: AMIs, instance families, placement groups, and pricing models
- Resilience patterns: Auto Scaling, load balancing, decoupling, and disaster recovery
- Multi-account governance: AWS Organizations, SCPs, and Control Tower
- SQL foundations: CREATE TABLE, INSERT, SELECT, and WHERE filtering

## Portfolio Structure

```text
week01/
├── README.md
├── notes/
│   ├── day1_reflection.md
│   ├── region_decision.md
│   ├── ec2-compute-decisions.md
│   ├── fintrust_data_model.md
│   ├── resilience-and-dr-plan.md
│   └── multi-account-governance.md
└── sql/
    ├── day2_explore.sql
    ├── day2_basic_select.sql
    ├── day3_fintrust_schema.sql
    └── day4_where_queries.sql
```

## Key Deliverables

- [notes/day1_reflection.md](notes/day1_reflection.md): reflection on the Week 1 learning experience
- [notes/region_decision.md](notes/region_decision.md): CPLG-based AWS region decision for FinTrust
- [notes/ec2-compute-decisions.md](notes/ec2-compute-decisions.md): EC2 architecture decisions for the FinTrust workload
- [notes/resilience-and-dr-plan.md](notes/resilience-and-dr-plan.md): resilience and disaster recovery strategy
- [notes/multi-account-governance.md](notes/multi-account-governance.md): AWS Organizations and Control Tower governance model
- [notes/fintrust_data_model.md](notes/fintrust_data_model.md): core FinTrust data entities and relationships
- [sql/day3_fintrust_schema.sql](sql/day3_fintrust_schema.sql): FinTrust database schema with constraints
- [sql/day4_where_queries.sql](sql/day4_where_queries.sql): SQL filtering queries for business analysis

## Reflection

Week 1 gave me a strong base in both architecture thinking and practical SQL. The most important lesson was that good technical work is not only about using the correct service or syntax, but also about explaining why the design decision is appropriate for the business problem.