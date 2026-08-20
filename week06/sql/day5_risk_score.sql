-- Author: Nompilo Eugenia Mchunu
-- Week 6 Day 5: combined fraud-risk score for the integration challenge

WITH suspicious_ratios AS (
    SELECT
        customer_id,
        COUNT(*) FILTER (WHERE is_suspicious)::NUMERIC
            / NULLIF(COUNT(*), 0) AS suspicious_ratio
    FROM transactions
    GROUP BY customer_id
),
monthly_spend AS (
    SELECT
        customer_id,
        DATE_TRUNC('month', transaction_date)::DATE AS month_start,
        SUM(amount) AS monthly_amount
    FROM transactions
    WHERE transaction_date >= DATE '2024-01-01'
      AND transaction_date < DATE '2025-01-01'
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
),
spending_spikes AS (
    SELECT DISTINCT customer_id
    FROM spend_history
    WHERE monthly_amount > previous_month_amount * 3
),
combined AS (
    SELECT
        c.customer_id,
        CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
        sr.suspicious_ratio,
        CASE WHEN ss.customer_id IS NOT NULL THEN 1 ELSE 0 END AS spike_flag,
        (sr.suspicious_ratio * 0.6)
            + (CASE WHEN ss.customer_id IS NOT NULL THEN 0.4 ELSE 0 END) AS risk_score
    FROM customers AS c
    INNER JOIN suspicious_ratios AS sr
        ON sr.customer_id = c.customer_id
    LEFT JOIN spending_spikes AS ss
        ON ss.customer_id = c.customer_id
)
SELECT
    customer_id,
    customer_name,
    ROUND(suspicious_ratio, 4) AS suspicious_ratio,
    spike_flag,
    ROUND(risk_score, 4) AS risk_score
FROM combined
ORDER BY risk_score DESC, customer_id
LIMIT 20;
