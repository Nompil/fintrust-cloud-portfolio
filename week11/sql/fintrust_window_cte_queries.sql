-- Week 11: window functions and common table expressions
-- PostgreSQL 15 or later
--
-- Expected columns:
--   transactions(transaction_id, account_id, transaction_date, amount)
--   accounts(account_id, customer_id)
--
-- These are read-only analysis queries. Execute them against the supplied
-- analytics database or a compatible FinTrust practice schema.

-- Query 1: top three transactions per account.
-- ROW_NUMBER keeps exactly three rows per account. DENSE_RANK shows where
-- equal amounts share a rank, making the difference between the two visible.
WITH ranked_transactions AS (
    SELECT
        t.account_id,
        t.transaction_id,
        t.transaction_date,
        t.amount,
        ROW_NUMBER() OVER (
            PARTITION BY t.account_id
            ORDER BY t.amount DESC, t.transaction_date DESC, t.transaction_id DESC
        ) AS row_number_rank,
        DENSE_RANK() OVER (
            PARTITION BY t.account_id
            ORDER BY t.amount DESC
        ) AS dense_rank_by_amount
    FROM transactions AS t
)
SELECT
    account_id,
    transaction_id,
    transaction_date,
    amount,
    row_number_rank,
    dense_rank_by_amount
FROM ranked_transactions
WHERE row_number_rank <= 3
ORDER BY account_id, row_number_rank;

-- Query 2: a three-step CTE chain that flags month-over-month growth above 100%.
-- A NULL previous month is not treated as an anomaly because there is no baseline.
WITH monthly_totals AS (
    SELECT
        t.account_id,
        DATE_TRUNC('month', t.transaction_date)::DATE AS month_start,
        SUM(t.amount) AS monthly_amount
    FROM transactions AS t
    GROUP BY t.account_id, DATE_TRUNC('month', t.transaction_date)
),
monthly_history AS (
    SELECT
        account_id,
        month_start,
        monthly_amount,
        LAG(monthly_amount) OVER (
            PARTITION BY account_id
            ORDER BY month_start
        ) AS previous_month_amount
    FROM monthly_totals
),
growth_alerts AS (
    SELECT
        account_id,
        month_start,
        monthly_amount,
        previous_month_amount,
        ROUND(
            100.0 * (monthly_amount - previous_month_amount)
            / NULLIF(previous_month_amount, 0),
            1
        ) AS growth_pct
    FROM monthly_history
    WHERE previous_month_amount IS NOT NULL
      AND previous_month_amount > 0
)
SELECT
    account_id,
    month_start,
    monthly_amount,
    previous_month_amount,
    growth_pct
FROM growth_alerts
WHERE growth_pct > 100
ORDER BY growth_pct DESC, account_id, month_start;

-- Query 3: current-year account quartiles by total transaction volume.
WITH account_volume AS (
    SELECT
        t.account_id,
        SUM(t.amount) AS current_year_amount
    FROM transactions AS t
    WHERE t.transaction_date >= DATE_TRUNC('year', CURRENT_DATE)
      AND t.transaction_date < DATE_TRUNC('year', CURRENT_DATE) + INTERVAL '1 year'
    GROUP BY t.account_id
),
quartiled_accounts AS (
    SELECT
        account_id,
        current_year_amount,
        NTILE(4) OVER (
            ORDER BY current_year_amount DESC, account_id
        ) AS volume_quartile
    FROM account_volume
)
SELECT
    account_id,
    current_year_amount,
    volume_quartile
FROM quartiled_accounts
ORDER BY volume_quartile, current_year_amount DESC, account_id;
