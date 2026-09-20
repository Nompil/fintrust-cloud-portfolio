# FinTrust Well-Architected Pillar Mapping

This mapping uses the FinTrust situations supplied in the Week 11 lessons. The primary pillar is the main problem being addressed. Some choices help more than one pillar, but the stated business need decides the primary answer.

| FinTrust situation | Primary pillar | Why it belongs there | Practical direction |
| --- | --- | --- | --- |
| Three legacy RDS instances are configured manually, which creates drift risk. | Operational Excellence | The problem is how infrastructure changes are run and controlled. | Move the instances into reviewed CloudFormation and use change sets and drift detection. |
| Administrators need audited access without opening SSH, while database passwords need rotation. | Security | The aim is to reduce unauthorised access and limit direct handling of sensitive data. | Use Session Manager, Secrets Manager, IAM roles and CloudTrail. |
| Two legacy MySQL RDS instances are Single-AZ while the banking service has a 45 minute recovery target. | Reliability | The concern is surviving an Availability Zone or database failure and meeting the recovery target. | Remediate the Single-AZ instances and maintain the pilot-light recovery design. |
| Product catalogue reads take 80 milliseconds and the same records are read thousands of times each second. | Performance Efficiency | The stated measure is read latency under heavy repeated demand. | Put ElastiCache for Redis in front of the database reads. |
| A restartable overnight batch job is still using On-Demand EC2 and is estimated to overspend by R480,000 each year. | Cost Optimisation | Interruptions are acceptable, so the requirement is to remove unnecessary spend. | Use Spot capacity with checkpointing and a restart plan. |
| Compute needs to reduce both energy use and cost without changing application code. | Sustainability, with Cost Optimisation | The environmental requirement makes Sustainability primary. Graviton supports both outcomes. | Test a compatible Graviton instance family using production-like metrics before migration. |

## Rules I used

1. Identify the outcome before selecting a service. A deployment pipeline is Operational Excellence, while automatic replacement of an unhealthy instance is Reliability.
2. Read the constraint closely. A batch task that tolerates interruption can use Spot; a payment workflow with a strict availability target cannot make that trade.
3. Keep the service and the pillar separate. Auto Scaling can improve Reliability when replacing failed instances or Performance Efficiency when absorbing a traffic spike.

This is a written mapping of the course scenarios. It is not an exported Well-Architected Tool review or a claim that the FinTrust workload was assessed in AWS.
