# Week 2 Day 1: SQL JOINs Reference

## The JOIN mental model
A JOIN combines rows from two tables using a shared key. In FinTrust, the main relationship is:

- customers.customer_id -> accounts.customer_id
- accounts.account_id -> transactions.account_id

Think of two spreadsheets laid side by side. INNER JOIN keeps only rows with a match in both. LEFT JOIN keeps all rows from the left table and fills the right side with NULL where no match exists.

## INNER JOIN syntax
```sql
SELECT
    c.first_name,
    c.last_name,
    a.account_type,
    a.balance
FROM customers c
INNER JOIN accounts a
    ON c.customer_id = a.customer_id
WHERE a.balance > 10000
ORDER BY a.balance DESC;
```

Use aliases to avoid ambiguity. The alias is assigned in the FROM and JOIN clauses and then used throughout the query.

## LEFT JOIN vs INNER JOIN

### INNER JOIN
Returns only customers with matching accounts.

```sql
SELECT c.first_name, c.last_name, a.account_type
FROM customers c
INNER JOIN accounts a
    ON c.customer_id = a.customer_id;
```

### LEFT JOIN
Returns all customers, including those with no account.

```sql
SELECT c.first_name, c.last_name, a.account_type
FROM customers c
LEFT JOIN accounts a
    ON c.customer_id = a.customer_id;
```

### Anti-join pattern
Use LEFT JOIN and IS NULL to find rows that have no match.

```sql
SELECT c.first_name, c.last_name
FROM customers c
LEFT JOIN accounts a
    ON c.customer_id = a.customer_id
WHERE a.account_id IS NULL;
```

## Full 3-table JOIN example
```sql
SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    a.account_type,
    a.balance AS current_balance,
    t.transaction_id,
    t.amount,
    t.transaction_type,
    t.transaction_date
FROM customers c
INNER JOIN accounts a
    ON c.customer_id = a.customer_id
INNER JOIN transactions t
    ON a.account_id = t.account_id
ORDER BY
    c.last_name,
    t.transaction_date DESC;
```

## Common JOIN errors

### Ambiguous column names
Problem: SELECT customer_id without a table prefix.

Fix: Use the alias, for example c.customer_id or a.customer_id.

### Missing ON clause
Problem: A JOIN without ON produces a Cartesian product.

Fix: Always include ON with the relationship key.

### Joining the wrong columns
Problem: joining customer_id to account_id.

Fix: join primary keys to foreign keys in the correct direction.

### LEFT JOIN behaving like INNER JOIN
Problem: filtering the right table in WHERE removes unmatched rows.

Fix: put the right-table filter in the ON clause when you want to keep the LEFT JOIN behaviour.

## Challenge queries
1. Find customers with a cheque account balance below R 1000.
2. List all transactions made by Western Cape customers in a 3-table join.
3. Find accounts with no transactions using a LEFT JOIN.

## Portfolio note
Save the working queries in week02/sql/day1_joins.sql with comments above each query explaining the intent and why the join type was chosen.
