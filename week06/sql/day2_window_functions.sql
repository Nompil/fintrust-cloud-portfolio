-- Author: Nompilo Eugenia Mchunu
-- Week 6 Day 2: PostgreSQL window function challenges

-- Challenge 1: rank June customers within their spending tier.
WITH june_spend AS (
    SELECT
        c.customer_id,
        CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
        SUM(t.amount) AS total_spend
    FROM customers AS c
    INNER JOIN transactions AS t
        ON t.customer_id = c.customer_id
    WHERE t.transaction_date >= DATE '2024-06-01'
      AND t.transaction_date < DATE '2024-07-01'
    GROUP BY c.customer_id, c.first_name, c.last_name
),
tiered_customers AS (
    SELECT
        customer_id,
        customer_name,
        total_spend,
        CASE
            WHEN total_spend >= 50000 THEN 'Premium'
            WHEN total_spend >= 10000 THEN 'Standard'
            ELSE 'Basic'
        END AS spend_tier
    FROM june_spend
)
SELECT
    customer_id,
    customer_name,
    spend_tier,
    total_spend,
    DENSE_RANK() OVER (
        PARTITION BY spend_tier
        ORDER BY total_spend DESC
    ) AS tier_rank
FROM tiered_customers
ORDER BY spend_tier, tier_rank, customer_id;

-- Challenge 2: retain each suspicious transaction and add branch exposure.
SELECT
    branch_code,
    transaction_id,
    customer_id,
    transaction_date,
    amount,
    SUM(amount) OVER (
        PARTITION BY branch_code
        ORDER BY transaction_date, transaction_id
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_fraud_exposure
FROM transactions
WHERE is_suspicious = TRUE
ORDER BY branch_code, transaction_date, transaction_id;

-- Challenge 3: detect monthly spend that is more than three times the prior month.
WITH monthly_spend AS (
    SELECT
        customer_id,
        DATE_TRUNC('month', transaction_date)::DATE AS month_start,
        SUM(amount) AS monthly_amount
    FROM transactions
    WHERE transaction_date >= DATE '2024-01-01'
      AND transaction_date < DATE '2024-07-01'
    GROUP BY customer_id, DATE_TRUNC('month', transaction_date)
),
spend_history AS (
    SELECT
        customer_id,
        month_start,
        monthly_amount,
        LAG(monthly_amount) OVER (
            PARTITION BY customer_id
            ORDER BY month_start
        ) AS previous_month_amount
    FROM monthly_spend
)
SELECT
    customer_id,
    month_start AS spike_month,
    monthly_amount AS current_month_amount,
    previous_month_amount
FROM spend_history
WHERE monthly_amount > previous_month_amount * 3
ORDER BY customer_id, spike_month;
