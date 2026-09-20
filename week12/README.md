# Week 12: Cost Governance and Performance Tuning

Week 12 builds cost reporting and multi-account governance around the FinTrust migration work. It extends the existing `week10/fintrust_migration` package instead of creating a second package with the same name.

## Deliverables

| Course requirement | Portfolio evidence |
| --- | --- |
| Cost Explorer report module | [Cost reporting module](../week10/fintrust_migration/cost_reporting.py) |
| Service and account reporting | `get_monthly_spend_by_service` and `get_per_account_spend` |
| CSV and HTML output | `write_csv_report` and `write_html_report` |
| Report runner | [Generate report script](generate_report.py) |
| Scheduled report handler | [Lambda handler](scheduled_cost_report.py) and [EventBridge schedule](infrastructure/cost-report-schedule.yaml) |
| IAM and SCP troubleshooting | [Access-denied analysis](lab-notes/access-denied-scenarios.md) and SCP examples |
| SQL tuning work | [View and targeted index](sql/fintrust_views.sql) and [tuning plan](lab-notes/sql-tuning-plan.md) |
| Cost and governance diagram | [Three-page PDF](diagrams/fintrust-cost-governance-architecture.pdf) |
| Portfolio audit | [Week 12 audit](evidence/portfolio-audit.md) |

## Run locally

```powershell
python -m pip install -r week12\requirements.txt
python -m unittest week12.tests.test_week12 -v
```

`generate_report.py` uses the normal boto3 credential chain and only works with an authorised AWS billing or delegated billing account. Cost Explorer calls are made in `us-east-1`, as required by the course material. The scheduled handler requires `FINTRUST_COST_REPORT_BUCKET` before it will upload files.

The SQL and CloudFormation files are implementation material, not execution evidence. Actual `EXPLAIN ANALYZE`, Cost Explorer, Config, CloudTrail, mock-exam and LMS results are intentionally not claimed here.

## Review material

* [Cost and reporting decisions](notes/cost-and-reporting.md)
* [Multi-account governance](notes/multi-account-governance.md)
* [Monitoring and infrastructure as code](notes/monitoring-and-infrastructure.md)
* [SAA Domains 1 and 2 review](notes/saa-domains-one-two.md)
* [Week 12 reflection](reflection.md)
* [Self assessment](self-assessment.md)
* [Portfolio audit](evidence/portfolio-audit.md)
* [Local verification record](evidence/local-checks.md)
