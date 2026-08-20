-- Author: Nompilo Eugenia Mchunu
-- Date: 20 August 2026
-- Week 2 portfolio check-in: aggregate reports for FinTrust

USE fintrust_db;

-- Count transactions and calculate total and average value per customer.
SELECT
    c.customer_id,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    COUNT(t.transaction_id) AS transaction_count,
    SUM(t.amount) AS total_amount,
    AVG(t.amount) AS average_amount
FROM customers AS c
INNER JOIN accounts AS a
    ON c.customer_id = a.customer_id
INNER JOIN transactions AS t
    ON a.account_id = t.account_id
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY total_amount DESC;

-- Show customers whose combined transaction value is above R10,000.
SELECT
    c.customer_id,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    SUM(t.amount) AS total_amount
FROM customers AS c
INNER JOIN accounts AS a
    ON c.customer_id = a.customer_id
INNER JOIN transactions AS t
    ON a.account_id = t.account_id
GROUP BY c.customer_id, c.first_name, c.last_name
HAVING SUM(t.amount) > 10000
ORDER BY total_amount DESC;

-- Summarise transaction count and value by month using MySQL date functions.
SELECT
    YEAR(transaction_date) AS transaction_year,
    MONTH(transaction_date) AS transaction_month,
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_amount,
    AVG(amount) AS average_amount
FROM transactions
GROUP BY YEAR(transaction_date), MONTH(transaction_date)
ORDER BY transaction_year, transaction_month;

-- Categorise transactions and aggregate the result for reporting.
SELECT
    CASE
        WHEN amount > 50000 THEN 'VERY_HIGH'
        WHEN amount > 10000 THEN 'HIGH'
        WHEN amount > 1000 THEN 'MEDIUM'
        ELSE 'LOW'
    END AS value_category,
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_amount,
    AVG(amount) AS average_amount
FROM transactions
GROUP BY value_category
ORDER BY total_amount DESC;
