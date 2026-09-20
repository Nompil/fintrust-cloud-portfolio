# Week 11 Well-Architected and FinOps Notes

## Pillar distinctions

Operational Excellence covers repeatable operations, small reversible changes and learning from failures. Security covers identity, encryption, traceability and defence in depth. Reliability is about recovery, redundancy and recovery objectives. Performance Efficiency is about latency, scale and choosing technology that fits the workload. Cost Optimisation avoids waste while meeting the requirement. Sustainability focuses on utilisation and environmental impact.

The most useful exam habit is to name the desired outcome before considering services. An ALB and Auto Scaling Group across Availability Zones answer a reliability problem. CloudFront or ElastiCache answer a latency problem. The same services can appear in a wider design, but the scenario wording determines the main pillar.

## FinTrust findings from the supplied scenarios

The Week 11 material describes three manual RDS configurations, two Single-AZ legacy MySQL instances, 62 percent of EC2 spend on On-Demand capacity, seven-year archives in S3 Standard and only 34 percent CostCentre and Environment tag coverage. These are course scenarios, not measurements collected from an account in this repository.

The proposed order is to close the reliability and security risks first, then make cost changes that do not weaken the required availability. The restartable batch workload is a reasonable candidate for Spot. Seven-year regulatory archives can use S3 Glacier Deep Archive only when the stated twelve to forty-eight hour retrieval window is acceptable. Tagging needs to improve before chargeback figures can be trusted.

## Cost and governance tool selection

| Need | Appropriate service | Reason |
| --- | --- | --- |
| Visual spend trends and forecasts | Cost Explorer | Interactive analysis by service, Region, account, tag and purchase type |
| Hourly line-item chargeback data | Cost and Usage Report with Athena | Detailed billing data delivered to S3 |
| A budget alert or a spend control action | AWS Budgets | Alerts and Budget Actions support thresholds and enforcement |
| EC2 right-sizing with Basic support | Compute Optimizer | It is free and uses CloudWatch metrics for recommendations |
| Broad cost, performance or fault-tolerance checks | Trusted Advisor with Business or Enterprise support | Those check categories are not available under Basic support |
| Prevent disabling CloudTrail across accounts | AWS Organizations SCP | An SCP sets an organisation-level permission ceiling |
| New governed accounts with a landing zone | AWS Control Tower | Account Factory and guardrails provide the starting controls |

An SCP never grants a permission. It only narrows the permissions that IAM policies could otherwise grant.
