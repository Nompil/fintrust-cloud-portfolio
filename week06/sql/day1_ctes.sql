-- Author: Nompilo Eugenia Mchunu
-- Week 6 Day 1: subqueries and common table expressions

-- Query 1: calculate the suspicious transaction ratio for each customer.
WITH customer_activity AS (
    SELECT
        customer_id,
        COUNT(*) AS total_transaction_count,
        COUNT(*) FILTER (WHERE is_suspicious) AS suspicious_transaction_count
    FROM transactions
    GROUP BY customer_id
)
SELECT
    c.customer_id,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    ca.total_transaction_count,
    ca.suspicious_transaction_count,
    ROUND(
        ca.suspicious_transaction_count::NUMERIC
        / NULLIF(ca.total_transaction_count, 0),
        4
    ) AS suspicious_ratio
FROM customer_activity AS ca
INNER JOIN customers AS c
    ON c.customer_id = ca.customer_id
ORDER BY suspicious_ratio DESC, c.customer_id;

-- Query 2: compare each branch total with the previous month using CTEs.
WITH branch_monthly AS (
    SELECT
        branch_code,
        DATE_TRUNC('month', transaction_date)::DATE AS month_start,
        SUM(amount) AS total_amount,
        COUNT(*) AS transaction_count
    FROM transactions
    GROUP BY branch_code, DATE_TRUNC('month', transaction_date)
),
month_comparison AS (
    SELECT
        current_month.branch_code,
        current_month.month_start,
        current_month.total_amount,
        current_month.transaction_count,
        previous_month.total_amount AS previous_month_amount
    FROM branch_monthly AS current_month
    LEFT JOIN branch_monthly AS previous_month
        ON previous_month.branch_code = current_month.branch_code
       AND previous_month.month_start = current_month.month_start - INTERVAL '1 month'
)
SELECT
    branch_code,
    month_start,
    total_amount,
    previous_month_amount,
    ROUND(
        (total_amount - previous_month_amount)
        / NULLIF(previous_month_amount, 0) * 100,
        1
    ) AS percentage_change
FROM month_comparison
ORDER BY branch_code, month_start;
