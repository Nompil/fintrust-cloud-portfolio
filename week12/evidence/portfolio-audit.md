# Week 12 Portfolio Audit

The Week 12 audit expects one `fintrust_migration` package. This portfolio keeps it in [Week 10](../../week10/fintrust_migration/) because that is where the migration package was built. Week 12 extends that package rather than creating a duplicate at the repository root.

| Course audit item | Repository location | Status |
| --- | --- | --- |
| Importable migration package | [Week 10 package](../../week10/fintrust_migration/__init__.py) | Present |
| Migration classifier | [EC2 classifier](../../week10/fintrust_migration/ec2/classifier.py) | Present |
| DMS lifecycle module | [DMS helpers](../../week10/fintrust_migration/rds/dms_helpers.py) | Equivalent structure present |
| DataSync module | [DataSync helpers](../../week10/fintrust_migration/s3/sync_helpers.py) | Equivalent structure present |
| Cost reporting module | [Cost reporting](../../week10/fintrust_migration/cost_reporting.py) | Added in Week 12 |
| Migration SQL views | [Week 10 migration views](../../week10/sql/migration_views.sql) | Present |
| Tuning view and index | [Week 12 SQL](../sql/fintrust_views.sql) | Present, awaiting database output |
| Root dependency list | [Root requirements](../../requirements.txt) | Includes Week 12 requirements |
| Lab notes | [Week 12 lab notes](../lab-notes/) | Present |
| Secrets review | Local scan recorded after final checks | Pending final Week 12 audit |

The course's audit references a `lab_notes/w11d2...` filename during Week 12 Day 2. This portfolio uses descriptive Week 12 filenames so the repository remains understandable after the programme.
