-- Week 12: transaction reporting view and targeted index definitions
-- PostgreSQL 15 or later. These statements require a compatible FinTrust
-- analytics schema and have not been represented as executed results.
--
-- Expected columns:
-- transactions(transaction_id, customer_id, account_id, transaction_date, amount, status)
-- customers(customer_id, customer_name)
-- accounts(account_id, account_type)

CREATE OR REPLACE VIEW vw_transaction_summary AS
SELECT
    t.transaction_id,
    t.transaction_date,
    t.status,
    t.amount,
    c.customer_name,
    a.account_type
FROM transactions AS t
JOIN customers AS c ON c.customer_id = t.customer_id
JOIN accounts AS a ON a.account_id = t.account_id;

-- Use the partial index only after EXPLAIN ANALYZE shows the pending or processing
-- transaction report is a frequent access pattern on a sufficiently large table.
-- CREATE INDEX CONCURRENTLY cannot run inside a transaction block.
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_transactions_pending_status_date
    ON transactions (status, transaction_date DESC)
    WHERE status IN ('PENDING', 'PROCESSING');

-- Check the plan before and after creating the index in the authorised database.
EXPLAIN (ANALYZE, BUFFERS)
SELECT
    transaction_id,
    transaction_date,
    amount,
    customer_name,
    account_type
FROM vw_transaction_summary
WHERE status = 'PENDING'
  AND transaction_date >= DATE '2024-01-01'
ORDER BY transaction_date DESC
LIMIT 100;
