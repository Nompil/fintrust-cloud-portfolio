# Week 10: Migration Execution

Week 10 turns the migration plan into reusable code. The `fintrust_migration` package classifies instances, reads Application Migration Service progress, manages DMS tasks, checks CDC lag, starts and monitors DataSync executions, changes transfer throttles and compares transfer costs. The SQL file supplies reporting views for migration progress and audit work.

## Deliverables

* [Migration automation package](fintrust_migration/)
* [All migration SQL views](sql/migration_views.sql)
* [Architecture narrative](architecture-narrative.md)
* [Detailed migration architecture](diagrams/fintrust-migration-execution-architecture.pdf)

## Package map

| Module | Responsibility |
| --- | --- |
| [Session factory](fintrust_migration/utils/sessions.py) | Lazy regional clients, resources and cross account role sessions |
| [Transfer costs](fintrust_migration/utils/transfer_costs.py) | DataSync, Direct Connect, Snowball and hybrid calculation |
| [EC2 classifier](fintrust_migration/ec2/classifier.py) | Six strategy and wave classification from EC2 tags |
| [MGN inventory](fintrust_migration/ec2/mgn_helpers.py) | Replication and lifecycle status for source servers |
| [DMS helpers](fintrust_migration/rds/dms_helpers.py) | Safe task lifecycle, CDC metrics and cutover gate |
| [DataSync helpers](fintrust_migration/s3/sync_helpers.py) | Task execution, progress, timeout handling and scheduled throttling |
| [Orchestrator](fintrust_migration/orchestrator.py) | Short EventBridge driven actions for classification, cutover checks and final sync |

All clients are created only when a function is called. Importing the package does not read credentials or contact AWS. Destructive DMS full restarts require an explicit approval argument.

## SQL work

The single SQL submission contains the five assessed reporting views plus two extension views:

1. `v_wave_progress`
2. `v_customer_accounts`
3. `v_monthly_txn_summary`
4. `v_daily_transfer_volume`
5. `v_volume_migration_progress`
6. `v_transfer_audit`
7. `v_migration_audit`

The percentage calculations use `NULLIF` to prevent division by zero. Dashboard consumers receive stable column names even if the underlying joins later change.

## Local checks

From the repository root:

```powershell
python -m pip install -r week10\requirements.txt
python -c "from week10.fintrust_migration import classify_instances, is_cutover_ready, start_task_execution, set_task_throttle; print('Package import OK')"
python -m unittest week10.tests.test_week10 -v
```

No personal account number, access key, database credential or actual customer record is stored in this folder. Account identifiers used by the tests are fictional test data.

## Review material

* [Six strategy decisions](notes/migration-strategies.md)
* [DMS cutover plan](notes/dms-cutover.md)
* [DataSync transfer plan](notes/datasync-transfer.md)
* [Automation and SQL decisions](notes/automation-and-reporting.md)
* [Week 11 preparation](notes/week11-preparation.md)
* [Self assessment](self-assessment.md)
* [Reflection](reflection.md)
* [Portfolio evidence](evidence/portfolio-evidence.md)
* [Local verification record](evidence/local-checks.md)
