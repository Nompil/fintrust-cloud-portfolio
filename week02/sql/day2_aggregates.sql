-- Author: Nompilo Eugenia Mchunu
-- Date: 20 August 2026
-- Week 2 Day 2: MySQL aggregate and reporting exercises

USE fintrust_db;

-- Exercise 1: Customer transaction activity for the reporting dashboard.
-- INNER JOIN includes only customers who have at least one transaction.
SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    c.province,
    COUNT(t.transaction_id) AS total_transactions,
    SUM(t.amount) AS total_transaction_amount
FROM customers AS c
INNER JOIN accounts AS a
    ON c.customer_id = a.customer_id
INNER JOIN transactions AS t
    ON a.account_id = t.account_id
GROUP BY
    c.customer_id,
    c.first_name,
    c.last_name,
    c.province
ORDER BY total_transaction_amount DESC;

-- Exercise 2: Account portfolio size and average balance by product type.
SELECT
    account_type,
    COUNT(*) AS account_count,
    AVG(balance) AS average_balance
FROM accounts
GROUP BY account_type
ORDER BY average_balance DESC;

-- Exercise 3: Provinces whose credit deposits exceed R100,000.
-- WHERE filters transaction rows before grouping; HAVING filters totals.
SELECT
    c.province,
    SUM(t.amount) AS total_deposit_amount,
    COUNT(t.transaction_id) AS credit_transaction_count
FROM customers AS c
INNER JOIN accounts AS a
    ON c.customer_id = a.customer_id
INNER JOIN transactions AS t
    ON a.account_id = t.account_id
WHERE t.transaction_type = 'CREDIT'
GROUP BY c.province
HAVING SUM(t.amount) > 100000
ORDER BY total_deposit_amount DESC;

-- Exercise 4: Monthly transaction volume and count for trend reporting.
SELECT
    YEAR(transaction_date) AS transaction_year,
    MONTH(transaction_date) AS transaction_month,
    SUM(amount) AS total_transaction_amount,
    COUNT(*) AS transaction_count
FROM transactions
GROUP BY
    YEAR(transaction_date),
    MONTH(transaction_date)
ORDER BY
    transaction_year,
    transaction_month;

-- Exercise 5: Daily high-frequency debit activity as a fraud signal.
SELECT
    c.customer_id,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    DATE(t.transaction_date) AS transaction_date,
    COUNT(t.transaction_id) AS debit_count
FROM customers AS c
INNER JOIN accounts AS a
    ON c.customer_id = a.customer_id
INNER JOIN transactions AS t
    ON a.account_id = t.account_id
WHERE t.transaction_type = 'DEBIT'
GROUP BY
    c.customer_id,
    c.first_name,
    c.last_name,
    DATE(t.transaction_date)
HAVING COUNT(t.transaction_id) > 3
ORDER BY
    transaction_date DESC,
    debit_count DESC;
