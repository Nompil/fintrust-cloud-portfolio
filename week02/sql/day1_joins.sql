-- =========================================================
-- Week 2 Day 1 - SQL JOIN exercises for FinTrust
-- These queries demonstrate INNER JOIN, LEFT JOIN, and
-- multi-table joins using the FinTrust schema.
-- =========================================================

-- Exercise 1: Show all customers with their account details.
-- INNER JOIN is used because we only want customers who have
-- a matching account row.
SELECT
    c.first_name,
    c.last_name,
    a.account_type,
    a.balance
FROM customers c
INNER JOIN accounts a
    ON c.customer_id = a.customer_id
ORDER BY a.balance DESC;

-- Exercise 2: Find Gauteng customers with balances above 25000.
-- INNER JOIN keeps only customers that have matching accounts.
SELECT
    c.first_name,
    c.last_name,
    c.province,
    a.account_type,
    a.balance
FROM customers c
INNER JOIN accounts a
    ON c.customer_id = a.customer_id
WHERE c.province = 'Gauteng'
  AND a.balance > 25000
ORDER BY a.balance DESC;

-- Exercise 3: Show customer transactions using a 3-table join.
-- INNER JOIN is correct here because we want only records that
-- have a customer, an account, and a transaction.
SELECT
    c.first_name,
    c.last_name,
    a.account_type,
    t.amount,
    t.transaction_date,
    t.transaction_type
FROM customers c
INNER JOIN accounts a
    ON c.customer_id = a.customer_id
INNER JOIN transactions t
    ON a.account_id = t.account_id
WHERE t.transaction_type = 'debit'
ORDER BY t.transaction_date DESC;

-- Exercise 4: Find customers who have no transactions.
-- LEFT JOIN is used so unmatched customers are still returned,
-- and the IS NULL filter isolates the missing relationship.
SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    c.province
FROM customers c
LEFT JOIN accounts a
    ON c.customer_id = a.customer_id
LEFT JOIN transactions t
    ON a.account_id = t.account_id
WHERE t.transaction_id IS NULL;

-- Exercise 5: Show high-value transactions for selected provinces.
-- INNER JOIN is appropriate because we want only rows with all
-- matching relationships in the joined tables.
SELECT
    c.first_name,
    c.last_name,
    c.province,
    t.amount
FROM customers c
INNER JOIN accounts a
    ON c.customer_id = a.customer_id
INNER JOIN transactions t
    ON a.account_id = t.account_id
WHERE t.amount > 10000
  AND c.province IN ('Western Cape', 'KwaZulu-Natal')
ORDER BY t.amount DESC;