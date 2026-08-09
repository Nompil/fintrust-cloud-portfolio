WEEK 4  ·  DAY 1  ·  REFERENCE GUIDE

# RDS *Quick Reference*
Engine comparison, Multi-AZ vs Read Replica decision table, backup cheatsheet, and the most common SAA-C03 RDS exam traps — one page to print and keep.

Guide
W4 D1

G01RDS Engine Comparison
Six Engines — Which to Choose

EngineBest ForKey AdvantageSAA Trigger KeywordsPostgreSQLComplex queries, JSON, GIS data, financial systemsBest standards compliance; supports advanced SQL (CTEs, window functions, JSONB)"complex transactions", "JSONB", "PostGIS", "open source"MySQLWeb apps, WordPress, general-purpose OLTPMost widely deployed; large community; high compatibility"MySQL", "LAMP stack", "web application"MariaDBMySQL-compatible workloads needing community forkDrop-in MySQL replacement with some extra features"MariaDB", "MySQL fork"OracleEnterprise apps with Oracle licensing dependenciesOnly option if app requires Oracle-specific PL/SQL packages"Oracle", "PL/SQL", "enterprise Oracle workload"SQL Server.NET apps, Microsoft stack, Windows authNative Windows authentication; SSRS/SSIS integration"SQL Server", ".NET", "Windows integrated auth"Aurora MySQL / PostgreSQLHigh-scale OLTP needing better performance and HA5x MySQL throughput, 3x PostgreSQL; 6-copy storage across 3 AZs"15 read replicas", "Global Database", "Aurora Serverless"

🔑**Default answer for SAA:** When the question says "relational database" and doesn't specify an engine, PostgreSQL or MySQL on RDS (or Aurora) is almost always the right direction. Oracle and SQL Server only win when the question explicitly mentions those platforms.

G02Multi-AZ vs Read Replica
Availability vs Performance — Never Confuse These

PropertyMulti-AZRead ReplicaPrimary purpose**High availability / DR****Read scaling / reporting offload**ReplicationSynchronous — standby is always in syncAsynchronous — slight replica lag possibleStandby readable?NO — standby is passive, not accessible for queriesYES — each replica is an independent readable endpointFailoverAutomatic — DNS flips in 60–120 seconds on primary failureManual promotion required — not automatic failoverConnection string change?NO — same endpoint before and after failoverYES — replica has its own endpoint URLMax replicas1 standby (Multi-AZ); up to 3 with Multi-AZ DB Cluster (Aurora-like)Up to 5 for MySQL/PostgreSQL; up to 15 for AuroraCross-region?NO — standby is in a different AZ, same RegionYES — cross-region Read Replicas supportedTypical use caseProduction database that must survive an AZ failureAnalytics, reporting, reducing load on primary

⚠️**Classic exam trap:** "The standby in Multi-AZ can be used for read traffic to improve performance." — FALSE. The standby is passive and not accessible. For read scaling, you need Read Replicas in addition to Multi-AZ.

G03RDS Backup Cheatsheet
Automated Backups · Snapshots · PITR

FeatureAutomated BackupsManual SnapshotsTriggered byRDS automatically — daily during the backup windowYou (or automation) — on demandRetention1–35 days (set at creation; default 7 days)Indefinite — until you delete themPoint-in-time restore (PITR)YES — restore to any second within the retention windowNO — only to the exact moment of the snapshotTransaction logsYES — stored to S3 continuously; enables PITRNO — snapshots are at a moment in time onlySurvive DB deletion?NO — deleted with the DB unless you take a final snapshotYES — persist after you delete themCross-region copy?Supports automated backup replication to another RegionYES — can copy snapshot to another Region

🔑**SAA exam points:** (1) Maximum automated backup retention is **35 days** — not 90, not unlimited. If the scenario requires more, use AWS Backup with a lifecycle policy. (2) PITR is only possible with automated backups, not manual snapshots. (3) Setting retention to 0 disables automated backups entirely.

G04Top 5 RDS Exam Traps
SAA-C03 Most Common Mistakes

- **"Multi-AZ improves read performance"** — FALSE. Multi-AZ is for availability only. The standby is not readable. Use Read Replicas for read scaling.
- **"Multi-AZ failover requires a connection string change"** — FALSE. The RDS endpoint (DNS) automatically points to the new primary after failover. Your app reconnects to the same endpoint.
- **"Read Replicas provide automatic failover"** — FALSE. Read Replicas must be manually promoted. Only Multi-AZ provides automatic failover.
- **"You can restore a backup to an existing instance"** — FALSE. Point-in-time restore and snapshot restore always create a NEW RDS instance. You then update your application's connection string.
- **"RDS automated backups are kept indefinitely"** — FALSE. They are deleted when you delete the DB (unless you take a final snapshot) and have a maximum retention of 35 days.

FINTRUSTCheckpoint — FinTrust RDS Choices
Engine Choice**PostgreSQL** on RDS Multi-AZ. Chosen for ACID compliance, complex transaction queries, and JSONB support for trade documents. Not Oracle (no licensing requirement), not MySQL (PostgreSQL's SQL standards compliance is better for financial data).

Multi-AZ ConfigPrimary in **af-south-1a**, standby in **af-south-1b**. Synchronous replication. Automatic failover in 60–120 seconds. Same connection string before and after failover. Standby is NOT readable.

Backup PolicyAutomated backups: **15-day retention** (regulatory requirement). Daily backup window: 02:00–03:00 SAST. PITR enabled within retention window. Weekly manual snapshots retained indefinitely for audit.

---

(Full Week 4 content captured — Day 2, Day 3, Day 4, Day 5 and labs are included in the original user content. If you want day-specific files, request splitting.)
