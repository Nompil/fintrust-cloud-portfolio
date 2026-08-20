# Week 2 Day 2: SQL Aggregate Reference

## Core functions

| Function | Purpose | NULL behaviour |
| --- | --- | --- |
| `COUNT(*)` | Counts rows | Includes rows containing NULL values |
| `COUNT(column)` | Counts non-NULL values | Ignores NULL in that column |
| `SUM(column)` | Adds numeric values | Ignores NULL |
| `AVG(column)` | Calculates the arithmetic mean | Ignores NULL |
| `MIN(column)` | Returns the smallest value | Ignores NULL |
| `MAX(column)` | Returns the largest value | Ignores NULL |

## Query order

The logical pattern is `FROM` and `JOIN`, then `WHERE`, `GROUP BY`, `HAVING`, `SELECT`, and `ORDER BY`.

- Use `WHERE` to filter individual rows before aggregation.
- Use `GROUP BY` for every selected field that is not aggregated.
- Use `HAVING` to filter grouped results using `COUNT`, `SUM`, `AVG`, `MIN`, or `MAX`.

```sql
SELECT
    c.province,
    COUNT(t.transaction_id) AS credit_count,
    SUM(t.amount) AS total_credits
FROM customers AS c
INNER JOIN accounts AS a
    ON c.customer_id = a.customer_id
INNER JOIN transactions AS t
    ON a.account_id = t.account_id
WHERE t.transaction_type = 'CREDIT'
GROUP BY c.province
HAVING SUM(t.amount) > 100000
ORDER BY total_credits DESC;
```

With MySQL's `ONLY_FULL_GROUP_BY` mode, selecting a non-aggregated field that is absent from `GROUP BY` produces an error. All Week 2 aggregate queries therefore list their grouping fields explicitly.
