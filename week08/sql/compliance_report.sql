-- High-value transactions for the selected monthly partition.
-- The year and month filters allow Athena to prune unrelated S3 partitions.
SELECT
    account_id,
    SUM(amount) AS total_amount,
    COUNT(*) AS transaction_count
FROM fintrust_curated.transactions
WHERE year = '2024'
  AND month = '06'
  AND amount > 50000
GROUP BY account_id
ORDER BY total_amount DESC
LIMIT 100;
