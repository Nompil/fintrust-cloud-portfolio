# Week 11: Well-Architected Review and Data Skills

Week 11 connects the Well-Architected Framework with practical data engineering work. The folder contains a six-pillar mapping for FinTrust, PostgreSQL window and CTE queries, and Python helpers for retrying a boto3-compatible call and collecting S3 metadata concurrently.

## Week 11 deliverables

| Course requirement | Portfolio evidence |
| --- | --- |
| WAF pillar mapping | [FinTrust pillar mapping](notes/waf-pillar-mapping.md) and [PDF overview](diagrams/fintrust-waf-pillar-mapping.pdf) |
| Top three transactions per account | [PostgreSQL query file](sql/fintrust_window_cte_queries.sql) using `ROW_NUMBER` and `DENSE_RANK` |
| Multi-step anomaly detection | The same SQL file, with `monthly_totals`, `monthly_history` and `growth_alerts` CTEs |
| Retry decorator around a boto3 call | [Pipeline resilience helpers](python/pipeline_resilience.py) |
| Parallel S3 metadata collection | [ThreadPoolExecutor helper](python/pipeline_resilience.py) and benchmark function |
| Portfolio review and reflection | [Checklist review](evidence/portfolio-check.md), [reflection](reflection.md) and [self assessment](self-assessment.md) |

## Run locally

The Python exercises need no AWS account for their tests because the client is supplied by the caller and the tests use a small in-memory stand-in.

```powershell
python -m pip install -r week11\requirements.txt
python -m unittest week11.tests.test_week11 -v
```

The SQL queries target PostgreSQL 15 or later. They use `DATE_TRUNC`, `LAG`, `ROW_NUMBER`, `DENSE_RANK` and `NTILE`. They have not been represented as executed results because no Week 11 database output was supplied.

## Notes

* [WAF pillar mapping](notes/waf-pillar-mapping.md)
* [Well-Architected and FinOps notes](notes/waf-and-finops-notes.md)
* [Data engineering implementation notes](notes/data-engineering-notes.md)
* [Portfolio review through Week 11](evidence/portfolio-check.md)
* [Local verification record](evidence/local-checks.md)

The remaining practical evidence is listed in [portfolio evidence](evidence/portfolio-evidence.md). It should be added only after the relevant AWS, SQL, LMS or peer-review activity has happened.
