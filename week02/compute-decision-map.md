# FinTrust Compute Decision Map

| FinTrust service | Compute choice | Why it fits | What would fail with the wrong choice? |
| --- | --- | --- | --- |
| Transaction API | ECS on Fargate | Stateless, auto-scaling service deployed across two Availability Zones behind an ALB | A single unmanaged server would create a scaling bottleneck and a single point of failure |
| Account Service | ECS on Fargate | Independent microservice that can scale separately from the Transaction API | Coupling it to the Transaction API would prevent independent deployment and scaling |
| Fraud Batch Processor | ECS on Fargate | Runs longer than 15 minutes, starts from EventBridge, and can scale to zero between jobs | Lambda would stop the job when it reached the maximum function duration |
| Compliance Report Generator | AWS Lambda | Monthly trigger, completes in minutes, and has no idle compute cost | EC2 would remain mostly idle while still requiring patching and payment |
| Internal Admin Portal | AWS Elastic Beanstalk | Managed application platform that retains occasional SSH access | Fargate would not provide the required direct host access for debugging |
| Nightly Account Reconciliation | AWS Batch with Spot capacity | Runs about 80,000 short CPU-intensive jobs and can use lower-cost spare capacity | A custom EC2 scheduler would add orchestration work and On-Demand cost |
| Customer Mobile App Backend | API Gateway, Lambda, and DynamoDB | Canonical serverless API pattern for a lightweight event-driven backend | An always-on server fleet would add capacity management and idle cost |

The choice follows the workload rather than a preferred service. Fargate suits long-running containerised services, Lambda suits short event-driven functions, Batch suits large parallel job queues, and Elastic Beanstalk retains server access while managing common deployment tasks.

## Workload decision path

The workload decision path is shown in the [Week 2 architecture diagrams PDF](diagrams/week02_architecture_diagrams.pdf).
