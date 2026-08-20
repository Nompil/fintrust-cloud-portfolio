-- Author: Nompilo Eugenia Mchunu
-- Date: 20 August 2026
-- Week 2 Day 1: MySQL JOIN exercises for the FinTrust database

USE fintrust_db;

-- Exercise 1: Customers with their account details.
SELECT
    c.first_name,
    c.last_name,
    a.account_type,
    a.balance
FROM customers AS c
INNER JOIN accounts AS a
    ON c.customer_id = a.customer_id
ORDER BY a.balance DESC;

-- Exercise 2: Gauteng customers with balances above R25,000.
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

-- Exercise 3: Debit transactions with their customer and account.
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
WHERE t.transaction_type = 'DEBIT'
ORDER BY t.transaction_date DESC;

-- Exercise 4: Customers with no transactions on any account.
SELECT DISTINCT
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

-- Exercise 5: High-value transactions in selected provinces.
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

-- Challenge 1: INNER JOIN is required because only customers with a
-- matching cheque account below R1,000 belong in this report.
SELECT
    c.first_name,
    c.last_name,
    c.province,
    a.balance
FROM customers AS c
INNER JOIN accounts AS a
    ON c.customer_id = a.customer_id
WHERE a.account_type = 'CHEQUE'
  AND a.balance < 1000
ORDER BY a.balance ASC;

-- Challenge 2: INNER JOINs connect Western Cape customers to their
-- accounts and transactions; unmatched records are not relevant here.
SELECT
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    t.amount,
    t.transaction_type,
    t.transaction_date
FROM customers AS c
INNER JOIN accounts AS a
    ON c.customer_id = a.customer_id
INNER JOIN transactions AS t
    ON a.account_id = t.account_id
WHERE c.province = 'Western Cape'
ORDER BY t.transaction_date DESC;

-- Challenge 3: LEFT JOIN keeps every account so IS NULL can identify
-- accounts for which no matching transaction exists.
SELECT
    a.account_id,
    a.account_type,
    a.balance,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name
FROM accounts AS a
INNER JOIN customers AS c
    ON a.customer_id = c.customer_id
LEFT JOIN transactions AS t
    ON a.account_id = t.account_id
WHERE t.transaction_id IS NULL
ORDER BY a.account_id;
