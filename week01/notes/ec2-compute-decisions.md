# FinTrust EC2 Compute Decisions

FinTrust uses a weekly rebuilt golden AMI for EC2 Auto Scaling Groups. The image includes current operating-system patches, the CloudWatch agent, and the approved security configuration so replacement instances launch consistently and require less startup configuration.

## Workload mapping

| Workload | Compute and instance choice | Placement | Purchase model | Reason |
| --- | --- | --- | --- | --- |
| Transaction processing API | `c6i.xlarge` EC2 Auto Scaling Group behind an ALB | Multi-AZ ASG | Three-year Reserved Instances for baseline; On-Demand for bursts | Continuous, predictable, compute-heavy processing with variable peaks |
| Fraud detection batch | `c6i.4xlarge` EC2 workers | No special placement requirement | Spot Instances | Four-hour job tolerates interruption and checkpoints to S3 every 10 minutes |
| Fraud-model training | Eight `p4d.24xlarge` GPU instances | Cluster Placement Group | Spot Instances | Requires the lowest inter-instance latency and highest throughput; training can restart from checkpoints |
| Transaction database pair | Primary and standby database instances | Spread Placement Group | Reserved Instances | Separates the two critical instances across hardware while covering steady usage |
| Compliance report | Lambda triggered by an EventBridge schedule | Managed by AWS | Pay per invocation | Runs monthly for less than five minutes, so idle EC2 capacity is unnecessary |
| Customer analytics dashboard | `r6i.2xlarge` | Standard placement | Compute Savings Plan | Memory-focused workload used mainly during business hours |

## Service boundary

- Use EC2 when operating-system control, long runtimes, or custom networking are required.
- Use Lambda for short event-driven work with no idle capacity.
- Use ECS on Fargate for containerised services that need a consistent runtime without managing EC2 hosts.

The exact instance sizes and commitment terms require measurement and pricing analysis before production deployment; the table records the programme scenario's starting decisions.
