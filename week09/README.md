# Week 9: Cost Control and Migration Planning

Week 9 adds financial governance and migration planning to FinTrust. The work connects the compute, container, serverless and analytics services from earlier weeks to a cost model that can be monitored across 14 AWS accounts. It also classifies the legacy estate before choosing database, server and archive migration methods.

## Architecture and decisions

* [FinTrust cost and migration architecture](diagrams/fintrust-cost-and-migration-architecture.pdf)
* [Pricing and business case](notes/pricing-and-business-case.md)
* [FinOps controls](notes/finops-controls.md)
* [Governance and migration planning](notes/governance-and-migration.md)
* [Database migration and recovery](notes/database-migration-and-recovery.md)
* [Python and QuickSight reporting](notes/cost-reporting-tools.md)

## Python work

| File | FinTrust purpose |
| --- | --- |
| [Pricing and TCO](python/pricing_and_tco.py) | Queries an EC2 On Demand price, models Savings Plans utilisation and finds the TCO break even month |
| [Monthly cost report](python/monthly_cost_report.py) | Queries three complete months, ranks services, calculates monthly change and writes the report to S3 |
| [Budget controls](python/budget_controls.py) | Builds percentage threshold notifications and reports current budget use without hardcoding an account ID |
| [Tag governance](python/tag_governance.py) | Audits required tag keys and allowed values, lists Service Catalog portfolios and writes a governance report |
| [DMS monitor](python/dms_monitor.py) | Reads task progress and table statistics, recognises terminal states and produces a scheduler friendly summary |
| [Snow planner](python/snow_transfer_planner.py) | Selects a Snow device, calculates capacity and compares the plan with an internet transfer |
| [FIS review](python/fis_experiments.py) | Summarises recent Fault Injection Service experiments and their stop conditions |
| [Tests](tests/test_week09.py) | Checks calculations and AWS request handling with local client substitutes |

The monthly report is useful to FinTrust because it turns organisation spend into a small scheduled report that can be sent to account owners without requiring dashboard access. In production, EventBridge Scheduler would invoke a Lambda function after the billing month closes. Lambda would query Cost Explorer in `us-east-1` and write the report to the protected `fintrust-cost-reports` bucket. QuickSight remains the better option when the finance team needs interactive filtering and drill down.

## Supporting evidence

* [CUR chargeback query](sql/monthly_chargeback.sql)
* [FinTrust server classification](data/migration-classification.csv)
* [Scenario calculations](evidence/scenario-calculations.md)
* [Portfolio evidence](evidence/portfolio-evidence.md)
* [Local checks](evidence/local-checks.md)
* [Week 9 reflection](reflection.md)
* [Week 9 self assessment](self-assessment.md)
* [Week 10 preparation](notes/week10-preparation.md)

## Local checks

Install the Week 9 dependencies and run the tests from the repository root:

```powershell
python -m pip install -r week09\requirements.txt
python -m unittest week09.tests.test_week09 -v
```

The code uses the normal boto3 credential chain. It does not contain account numbers, credentials, customer records or claims of completed AWS activity.
