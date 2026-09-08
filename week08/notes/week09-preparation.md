# Week 9 Preparation

Week 9 adds cost management and migration planning to the architecture. The Week 8 design already contains several cost choices that need measuring rather than assuming:

1. Compare the monthly EMR cluster with a permanent Redshift or EMR environment.
2. Track Spot interruption rates for the EMR Task fleet and keep Core nodes on On-Demand capacity.
3. Monitor Athena bytes scanned and enforce the 10 GB workgroup limit.
4. Check whether purchased SPICE capacity matches the four dashboard datasets.
5. Review SageMaker endpoint utilisation before committing to a larger or reserved inference option.
6. Use Cost Explorer for trends, AWS Budgets for thresholds and the Cost and Usage Report for resource-level analysis.

For the migration plan, DMS supports database replication with limited downtime, while Snowball Edge is more appropriate for a large historical archive that cannot cross the available network within the migration window. Each workload still needs its own choice among rehost, replatform, refactor, repurchase, retain, retire and relocate.
