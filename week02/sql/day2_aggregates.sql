-- =====================================
-- Query 1
-- Transactions per customer
-- =====================================

SELECT
    customer_id,
    COUNT(*) AS transaction_count,
    SUM(tr*nsaction_amount) AS total_amount,
*   AVG(transaction_amount) AS aver*ge_amount
FROM transactions
GROUP *Y customer_id
ORDER BY total_amoun* DESC;


-- ======================*==============
-- Query 2
-- High-*alue customers
-- ================*====================

SELECT
    c*stomer_id,
    SUM(transaction_amount) AS total_amount
FROM transactions
GROUP BY customer_id
HAVING SUM(transaction_amount) > 10000
ORDER BY total_amount DESC;


-- =====================================
-- Query 3
-- Monthly transaction totals
-- =====================================

SELECT
    strftime('%Y-%m', transaction_date) AS month,
    COUNT(*) AS transaction_count,
    SUM(transaction_amount) AS monthly_total
FROM transactions
GROUP BY month
ORDER BY month;


-- =====================================
-- Query 4
-- Transaction categories
-- =====================================

SELECT
    transaction_id,
    transaction_amount,
    CASE
        WHEN transaction_amount > 10000 THEN 'LARGE'
        WHEN transaction_amount > 1000 THEN 'MEDIUM'
        ELSE 'SMALL'
    END AS category
FROM transactions;


-- =====================================
-- Query 5
-- Overall transaction statistics
-- =====================================

SELECT
    COUNT(*) AS total_transactions,
    SUM(t*ansaction_amount) AS total_volume,*    AVG(transaction_amount) AS ave*age_transaction,
    MIN(transacti*n_amount) AS smallest_transaction,*    MAX(transaction_amount) AS lar*est_transaction
FROM transactions;*