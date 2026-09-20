# SQL Tuning Plan

The Week 12 lesson asks for before and after `EXPLAIN ANALYZE` output from an authorised PostgreSQL database. No output was supplied, so this record contains the test plan rather than invented measurements.

1. Run the `EXPLAIN (ANALYZE, BUFFERS)` query in [fintrust_views.sql](../sql/fintrust_views.sql) before creating the index.
2. Check for a sequential scan only after confirming the table has a meaningful row count. A sequential scan is often reasonable for a small table.
3. Create `idx_transactions_pending_status_date` outside a transaction because it uses `CONCURRENTLY`.
4. Run the identical query again and compare the access path, actual rows, planning time, execution time and shared buffers.
5. Keep the index only if it improves the frequent pending or processing report without adding an unacceptable write cost.

The index is partial because the report filters on `PENDING` and `PROCESSING`. It should not be copied automatically to a table with a different status distribution or access pattern.
