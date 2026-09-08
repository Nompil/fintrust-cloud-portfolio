# Pandas and Athena

Pandas is useful when a FinTrust analyst is developing a transformation against a small extract or testing fraud features on a laptop. It gives direct control over data types, filters and grouped calculations, and the result can be inspected at each step. Memory is the practical limit, so it is not the right place to scan several years of the bank's transaction history.

Athena is the better fit for an investigator or compliance analyst running ad hoc SQL across partitioned data in S3. It does not require a local download or a long-running cluster, and several people can query the same Glue table definition. Its cost depends on bytes scanned, which is why the FinTrust tables use Parquet and date partitions. Regular executive dashboards use SPICE instead of repeating the same Athena scans for every viewer.
