CREATE OR REPLACE VIEW v_wave_progress AS
SELECT
    migration_wave,
    COUNT(*) AS total_assets,
    SUM(CASE WHEN status = 'P' THEN 1 ELSE 0 END) AS planned,
    SUM(CASE WHEN status = 'I' THEN 1 ELSE 0 END) AS in_progress,
    SUM(CASE WHEN status = 'C' THEN 1 ELSE 0 END) AS complete,
    SUM(CASE WHEN status = 'F' THEN 1 ELSE 0 END) AS failed,
    ROUND(
        100.0 * SUM(CASE WHEN status = 'C' THEN 1 ELSE 0 END)
        / NULLIF(COUNT(*), 0),
        1
    ) AS completion_pct
FROM migration_plan
GROUP BY migration_wave;

CREATE OR REPLACE VIEW v_customer_accounts AS
SELECT
    c.customer_id,
    c.first_name || ' ' || c.last_name AS full_name,
    c.segment,
    c.region,
    COUNT(a.account_id) AS account_count,
    COALESCE(SUM(a.balance), 0) AS total_balance,
    COALESCE(SUM(CASE WHEN a.currency = 'ZAR' THEN a.balance ELSE 0 END), 0) AS zar_balance,
    c.onboarded_date
FROM customers c
LEFT JOIN accounts a
    ON c.customer_id = a.customer_id
   AND a.status = 'active'
GROUP BY
    c.customer_id,
    c.first_name,
    c.last_name,
    c.segment,
    c.region,
    c.onboarded_date;

CREATE OR REPLACE VIEW v_monthly_txn_summary AS
SELECT
    DATE_TRUNC('month', t.txn_date) AS txn_month,
    c.segment,
    t.channel,
    t.txn_type,
    COUNT(*) AS txn_count,
    SUM(t.amount) AS total_amount,
    AVG(t.amount) AS avg_amount,
    MAX(t.amount) AS max_amount
FROM transactions t
JOIN accounts a ON t.account_id = a.account_id
JOIN customers c ON a.customer_id = c.customer_id
GROUP BY
    DATE_TRUNC('month', t.txn_date),
    c.segment,
    t.channel,
    t.txn_type;

CREATE OR REPLACE VIEW v_daily_transfer_volume AS
SELECT
    DATE(started_at) AS transfer_date,
    source_volume,
    COUNT(*) AS execution_count,
    SUM(files_transferred) AS total_files,
    ROUND(SUM(bytes_transferred) / 1073741824.0, 2) AS total_gb,
    SUM(CASE WHEN status = 'SUCCESS' THEN 1 ELSE 0 END) AS successful_runs,
    SUM(CASE WHEN status = 'ERROR' THEN 1 ELSE 0 END) AS failed_runs
FROM datasync_executions
GROUP BY DATE(started_at), source_volume;

CREATE OR REPLACE VIEW v_volume_migration_progress AS
WITH latest_success AS (
    SELECT
        task_id,
        SUM(bytes_transferred) AS bytes_transferred,
        MAX(completed_at) AS last_transfer
    FROM datasync_executions
    WHERE status = 'SUCCESS'
    GROUP BY task_id
)
SELECT
    v.volume_id,
    v.volume_name,
    v.source_system,
    v.total_size_gb,
    COALESCE(s.bytes_transferred / 1073741824.0, 0) AS transferred_gb,
    LEAST(
        ROUND(
            100.0 * COALESCE(s.bytes_transferred / 1073741824.0, 0)
            / NULLIF(v.total_size_gb, 0),
            1
        ),
        100.0
    ) AS pct_complete,
    s.last_transfer
FROM transfer_volumes v
LEFT JOIN latest_success s ON v.volume_id = s.task_id;

CREATE OR REPLACE VIEW v_transfer_audit AS
SELECT
    e.exec_id,
    v.volume_name,
    v.source_system,
    c.regulation,
    c.encryption_required,
    c.retention_years,
    e.status AS execution_status,
    e.bytes_transferred,
    e.files_transferred,
    e.started_at,
    e.completed_at
FROM datasync_executions e
JOIN transfer_volumes v ON e.task_id = v.volume_id
LEFT JOIN compliance_requirements c ON v.volume_id = c.volume_id;

CREATE OR REPLACE VIEW v_migration_audit AS
SELECT
    c.customer_id,
    c.first_name || ' ' || c.last_name AS full_name,
    a.account_id,
    m.source_system,
    m.validation_state,
    m.migrated_at
FROM customers c
JOIN accounts a ON c.customer_id = a.customer_id
LEFT JOIN migration_status m ON a.account_id = m.asset_id;
