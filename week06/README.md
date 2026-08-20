# Week 6: Security, Identity, Observability, and Analytics

Week 6 combines highly available architecture, advanced IAM, preventive and detective security controls, threat response, PostgreSQL analytics, and boto3 automation for the FinTrust case study.

## Architecture and security decisions

- [Week 6 architecture diagram pack](diagrams/week06_architecture_diagrams.pdf)
- [IAM design decision](notes/iam-design.md)
- [Security services configuration](notes/security-services.md)
- [Incident response and audit design](notes/incident-response.md)
- [CISO-level security architecture summary](notes/security-architecture-summary.md)

## SQL deliverables

- [Practice schema and data](sql/setup_week06_analytics.sql)
- [Day 1 CTE queries](sql/day1_ctes.sql)
- [Day 2 window-function challenges](sql/day2_window_functions.sql)
- [Day 5 combined risk score](sql/day5_risk_score.sql)

The SQL files target PostgreSQL 15 or later because the Week 6 material uses `DATE_TRUNC`, `FILTER`, and PostgreSQL window-function syntax. Run the setup file first, followed by the three exercise files.

## Python deliverables

- [Day 3 S3 audit](python/s3_audit.py)
- [Day 4 IAM and Security Group audit](python/security_audit.py)
- [Day 5 risk and S3 activity report](python/risk_activity_report.py)
- [Local audit tests](python/test_week06_audits.py)
- [Python dependencies](requirements.txt)

The scripts use the normal boto3 credential chain. They do not contain access keys. Install boto3 with:

```powershell
python -m pip install -r week06\requirements.txt
```

The security audit reads the report bucket from `FINTRUST_AUDIT_BUCKET`. An optional customer-managed KMS key can be supplied through `FINTRUST_AUDIT_KMS_KEY_ID`.

## Reflection and review

- [Week 6 reflection](reflection.md)
- [Week 6 self-assessment](self-assessment.md)
- [Validation record](evidence/validation.md)
