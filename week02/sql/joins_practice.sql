-- =========================================================
-- Week 2 Day 1 - JOIN practice for FinTrust Bank
-- Author: FinTrust learner
-- Date: 2026-08-09
-- Purpose: Demonstrate INNER JOIN, LEFT JOIN, and multi-table joins
-- =========================================================

-- Query 1: Show customers with their account details.
SELECT
    c.first_name,
    c.last_name,
    a.account_type,
    a.balance
FROM customers AS c
INNER JOIN accounts AS a
    ON c.customer_id = a.customer_id
ORDER BY a.balance DESC;

-- Query 2: Find Gauteng customers with balances above 25000.
SELECT
    c.first_name,
    c.last_name,
    c.province,
    a.account_type,
    a.balance
FROM customers AS c
INNER JOIN accounts AS a
    ON c.customer_id = a.customer_id
WHERE c.province = 'Gauteng'
  AND a.balance > 25000
ORDER BY a.balance DESC;

-- Query 3: Show transactions for customers using a 3-table join.
SELECT
    c.first_name,
    c.last_name,
    a.account_type,
    t.amount,
    t.transaction_date,
    t.transaction_type
FROM customers AS c
INNER JOIN accounts AS a
    ON c.customer_id = a.customer_id
INNER JOIN transactions AS t
    ON a.account_id = t.account_id
WHERE t.transaction_type = 'debit'
ORDER BY t.transaction_date DESC;

-- Query 4: Find customers who have no transactions.
SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    c.province
FROM customers AS c
LEFT JOIN accounts AS a
    ON c.customer_id = a.customer_id
LEFT JOIN transactions AS t
    ON a.account_id = t.account_id
WHERE t.transaction_id IS NULL;

-- Query 5: Show high-value transactions for selected provinces.
SELECT
    c.first_name,
    c.last_name,
    c.province,
    t.amount
FROM customers AS c
INNER JOIN accounts AS a
    ON c.customer_id = a.customer_id
INNER JOIN transactions AS t
    ON a.account_id = t.account_id
WHERE t.amount > 10000
  AND c.province IN ('Western Cape', 'KwaZulu-Natal')
ORDER BY t.amount DESC;
