# Week 2 Day 1 and Day 2 MySQL Verification

The Week 2 Day 1 and Day 2 SQL was executed on 20 August 2026 using MySQL Community Server 8.4.11 in an isolated local Docker container. The Week 1 Day 3 core schema and branches extension were loaded first.

## Day 1 JOINs

Script: `week02/sql/day1_joins.sql`

| Check | Verified result |
| --- | --- |
| Five lab exercises | Executed successfully |
| Three practical-guide challenges | Executed successfully |
| Three-table JOINs | Customer, account, and transaction relationships resolved correctly |
| Unmatched-record queries | LEFT JOIN and `IS NULL` executed successfully |
| SQL errors | None |

## Day 2 aggregates

Script: `week02/sql/day2_aggregates.sql`

| Check | Verified result |
| --- | --- |
| Customer transaction totals | Executed successfully |
| Average balance by account type | Executed successfully |
| Provincial credit threshold using `HAVING` | Executed successfully |
| Monthly transaction summary | Executed successfully |
| Daily debit fraud signal | Executed successfully |
| SQL errors | None |

The validation database contained 5 customers, 5 accounts, 5 transactions, 3 branches, and 3 verified foreign-key constraints. Queries that return no matching rows with the small learning dataset still completed correctly. The temporary validation container was removed after testing.
