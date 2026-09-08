# DMS Cutover Plan

Oracle to Aurora PostgreSQL requires SCT because the database engines differ. The conversion report separates automatic objects from the PL/SQL procedures and triggers requiring manual work. DMS starts only after the target schema and network routes have been checked.

The task uses Full Load plus CDC, Full LOB mode for compliance documents and validation. Oracle supplemental logging and adequate redo retention are prerequisites. CloudWatch supplies `CDCLatencySource` and `CDCLatencyTarget`; table statistics supply load and validation errors.

Cutover requires all of the following:

1. DMS task status is `running`.
2. Source and target latency are no more than 30 seconds.
3. No DMS tables are in an error state.
4. Validation reports zero failed records.
5. The application smoke test and rollback owner are ready.
6. The approved maintenance window has started.

If lag rises above 120 seconds, the cutover pauses. The team checks source transaction rate, target write capacity, replication instance memory, network throughput and LOB handling. It does not restart the full load. A stopped CDC task resumes with `resume-processing`; `start-replication` is reserved for an approved rebuild because it can reload target data.
