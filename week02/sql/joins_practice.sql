-- Author: Nompilo Eugenia Mchunu
-- Date: 20 August 2026
-- Week 2 portfolio check-in: INNER JOIN and LEFT JOIN practice

USE fintrust_db;

-- Match each customer to their accounts.
SELECT
    c.customer_id,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    a.account_id,
    a.account_type,
    a.balance
FROM customers AS c
INNER JOIN accounts AS a
    ON c.customer_id = a.customer_id
ORDER BY customer_name, a.account_id;

-- Keep all customers and identify those who have no account.
SELECT
    c.customer_id,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    a.account_id,
    a.account_type
FROM customers AS c
LEFT JOIN accounts AS a
    ON c.customer_id = a.customer_id
WHERE a.account_id IS NULL
ORDER BY customer_name;

-- Join customers, accounts, and transactions for a complete activity report.
SELECT
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    a.account_number,
    a.account_type,
    t.transaction_id,
    t.transaction_type,
    t.amount,
    t.transaction_date
FROM customers AS c
INNER JOIN accounts AS a
    ON c.customer_id = a.customer_id
INNER JOIN transactions AS t
    ON a.account_id = t.account_id
ORDER BY t.transaction_date DESC;

-- Find customers whose accounts do not yet have a transaction.
SELECT DISTINCT
    c.customer_id,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name
FROM customers AS c
INNER JOIN accounts AS a
    ON c.customer_id = a.customer_id
LEFT JOIN transactions AS t
    ON a.account_id = t.account_id
WHERE t.transaction_id IS NULL
ORDER BY customer_name;
