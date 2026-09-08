# Database Migration and Recovery

## Oracle to Aurora PostgreSQL

This is a heterogeneous migration. Schema Conversion Tool assesses and converts tables, indexes and compatible code first. The database team reviews procedures and triggers that require manual work. Database Migration Service then runs Full Load plus Change Data Capture so Oracle can remain available while Aurora is validated. At cutover, writes stop briefly, replication lag must reach zero, application connections move to Aurora, and reconciliation checks run before Oracle is retired.

For regular monitoring, EventBridge Scheduler invokes a Lambda function every five minutes. The function reads DMS task statistics and per table validation counts, stores a summary and alerts through SNS when error counts rise. A `running` task is normal during CDC, so the monitor does not treat it as completion.

## Archive transfer

The 3,000 TB archive requires 38 Snowball Edge Storage Optimised devices at 80 TB usable capacity each. That provides 3,040 TB and leaves 40 TB spare. At an ideal sustained 1 Gbps, transferring 3 PB takes about 278 days before protocol overhead. Shipping parallel devices is therefore the practical choice. The destination uses an S3 archive tier with the required retention controls.

## Recovery choices

Retail payments use a multi region active design because RTO and RPO are measured in seconds. Regulatory reporting uses warm standby because the full stack must already exist but can run at reduced capacity. Internal tools use backup and restore because a four hour RTO and daily recovery point are acceptable. Resilience Hub assesses these targets, while controlled Fault Injection Service experiments test whether recovery actually works.

The payment experiment stops when the `HealthyHostCount` alarm remains below the required minimum or the payment error rate exceeds the approved threshold. Stop conditions protect customers; they are not proof that the experiment succeeded.
