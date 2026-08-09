-- =========================================================
-- Week 2 Day 2 - Aggregate reporting for FinTrust Bank
-- Author: FinTrust learner
-- Date: 2026-08-09
-- Purpose: Demonstrate COUNT, SUM, AVG, GROUP BY, HAVING, and CASE
-- =========================================================

-- Query 1: Count and sum transactions per customer.
SELECT
    customer_id,
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_amount,
    AVG(amount) AS average_amount
FROM transactions
GROUP BY customer_id
ORDER BY total_amount DESC;

-- Query 2: Find customers whose total transaction volume is high.
SELECT
    customer_id,
    SUM(amount) AS total_amount
FROM transactions
GROUP BY customer_id
HAVING SUM(amount) > 10000
ORDER BY total_amount DESC;

-- Query 3: Show monthly transaction totals.
SELECT
    strftime('%Y-%m', transaction_date) AS month,
    COUNT(*) AS transaction_count,
    SUM(amount) AS monthly_total
FROM transactions
GROUP BY month
ORDER BY month;

-- Query 4: Categorise transactions by size.
SELECT
    transaction_id,
    amount,
    CASE
        WHEN amount > 10000 THEN 'LARGE'
        WHEN amount > 1000 THEN 'MEDIUM'
        ELSE 'SMALL'
    END AS category
FROM transactions;

-- Query 5: Return overall transaction statistics.
SELECT
    COUNT(*) AS total_transactions,
    SUM(amount) AS total_volume,
    AVG(amount) AS average_transaction,
    MIN(amount) AS smallest_transaction,
    MAX(amount) AS largest_transaction
FROM transactions;
