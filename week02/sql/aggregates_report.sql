-- Customer transaction summary

SELECT
    customer_id,
    COUNT(*) AS transaction_count,
    SUM(transaction_amount) AS total_amount,
    AVG(transaction_amount) AS average_amount
FROM transactions
GROUP BY customer_id
HAVING SUM(transaction_amount) > 10000
ORDER BY total_amount DESC;

-- Monthly transaction summary

SELECT
    strftime('%Y-%m', transaction_date) AS month,
    SUM(transaction_amount) AS monthly_total
FROM transactions
GROUP BY month;

-- Transaction categorisation

SELECT
    transaction_id,
    transaction_amount,
    CASE
        WHEN transaction_amount > 10000 THEN 'LARGE'
        WHEN transaction_amount > 1000 THEN 'MEDIUM'
        ELSE 'SMALL'
    END AS category
FROM transactions;