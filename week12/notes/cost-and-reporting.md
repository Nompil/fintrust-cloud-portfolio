# Week 12 Cost and Reporting Decisions

## Cost Explorer report design

Cost Explorer is a billing endpoint, so the client is created in `us-east-1` even though FinTrust workloads use other Regions. The report starts on a calendar-month boundary, groups unblended cost by service, and can also group by linked account and service. The account names come from Organizations because Cost Explorer returns account IDs rather than friendly names.

The report writers create CSV and HTML locally first. Upload is optional and requires a bucket name at runtime. This avoids a hidden upload or a hardcoded bucket. The scheduled Lambda handler only runs when `FINTRUST_COST_REPORT_BUCKET` is configured.

## Cost decisions from the course scenario

The supplied Week 12 scenario uses four levers: right-size consistently low-utilisation capacity, match capacity to demand with elasticity, remove resources that no longer serve a workload, and make lower-cost architectural choices early. A restartable batch workload is a Spot candidate. A stable EC2 family and Region may suit an EC2 Instance Savings Plan. A workload shared across EC2, Lambda and Fargate needs the flexibility of a Compute Savings Plan.

The figures in the Week 12 lessons, including the 91 percent Savings Plan coverage and the proposed right-sizing savings, are teaching scenarios. They are not reported as results from this portfolio.

## Reporting controls

Cost allocation tags need activation in the Billing console before they appear in Cost Explorer. Tags are more reliable when they are enforced at provisioning time. Config can identify resources missing required tags, while Service Catalog can apply tags through approved products. An SCP can place an organisation-level limit around resource creation, but it does not grant permission or replace IAM.
