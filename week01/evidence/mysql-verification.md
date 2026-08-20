# Week 1 MySQL Verification

The Week 1 SQL was executed on 20 August 2026 using MySQL Community Server 8.4.11 in an isolated local Docker container. Every listed script completed without an SQL error.

## Day 2 supplied sample database

Scripts executed:

1. `week01/sql/day2_fintrust_sample_data.sql`
2. `week01/sql/day2_explore.sql`
3. `week01/sql/day2_basic_select.sql`

| Table | Verified row count |
| --- | ---: |
| `customers` | 10 |
| `accounts` | 10 |
| `transactions` | 10 |

## Day 3 and Day 4 learner database

Scripts executed:

1. `week01/sql/day3_fintrust_schema.sql`
2. `week01/sql/day3_challenge_branches.sql`
3. `week01/sql/day4_where_queries.sql`
4. `week01/sql/day4_where_challenges.sql`

| Check | Verified result |
| --- | --- |
| Core tables | `customers`, `accounts`, and `transactions` created successfully |
| Core row counts | 5 customers, 5 accounts, and 5 transactions |
| Branches challenge | 3 branches created; nullable `accounts.branch_id` added |
| Foreign keys | 3 constraints verified in `information_schema.REFERENTIAL_CONSTRAINTS` |
| WHERE exercises | All required and stretch queries executed successfully |

The temporary validation container was removed after testing.
