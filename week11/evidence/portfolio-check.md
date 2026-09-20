# Portfolio Check Through Week 11

The Week 11 checklist asks for each deliverable to be committed and accessible. This review records repository evidence that already exists and separates it from account-level proof that cannot be inferred from a document.

| Checklist item | Repository evidence | Status |
| --- | --- | --- |
| IAM least-privilege review | [Week 6 IAM design](../../week06/notes/iam-design.md) | Design evidence present |
| EC2 launch and user data | [Week 1 EC2 decisions](../../week01/notes/ec2-compute-decisions.md) | Design evidence present; no launch output recorded |
| S3 lifecycle, versioning and bucket policy | [Week 3 storage design](../../week03/storage-design.md) and [storage security](../../week03/storage-security.md) | Design evidence present |
| VPC public and private subnet design | [Week 5 network PDF](../../week05/diagrams/fintrust-network-architecture.pdf) | Present |
| RDS Multi-AZ and backups | [Week 4 database design](../../week04/db-architecture-diagram.md) | Design evidence present; no account configuration export recorded |
| DynamoDB key design and access patterns | [Week 8 analytics README](../../week08/README.md) | Partial; partition-key use is documented, but a dedicated table design is not yet separate |
| S3 data lake with Glue and Athena | [Week 8 data lake note](../../week08/notes/data-lake-and-athena.md) | Present |
| FinTrust recovery strategy | [Week 1 resilience plan](../../week01/notes/resilience-and-dr-plan.md) | Present |
| CloudWatch dashboard and composite alarm | [Week 6 security architecture](../../week06/notes/security-architecture-summary.md) | Monitoring design is present; dashboard evidence is not recorded |
| CloudTrail and Athena detection query | [Week 6 incident response note](../../week06/notes/incident-response.md) | CloudTrail design is present; Athena query evidence is not recorded |
| Three-tier application architecture | [Week 6 security architecture](../../week06/notes/security-architecture-summary.md) | Present |
| GuardDuty finding analysis | [Week 6 incident response note](../../week06/notes/incident-response.md) | Simulated analysis is present |
| Week 11 WAF mapping | [WAF mapping](../notes/waf-pillar-mapping.md) | Present |
| Top-three transaction query | [Week 11 SQL](../sql/fintrust_window_cte_queries.sql) | Present, awaiting database output |
| Three-stage anomaly CTE | [Week 11 SQL](../sql/fintrust_window_cte_queries.sql) | Present, awaiting database output |
| Retry decorator around a boto3-compatible call | [Week 11 Python](../python/pipeline_resilience.py) | Present and locally tested |

The items marked as missing practical evidence should be completed with real screenshots, exports or query output. They should not be replaced with made-up results.
