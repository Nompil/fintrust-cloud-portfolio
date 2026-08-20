# Week 2 Compute Notes

## EC2

EC2 is the right choice when FinTrust needs a traditional server with full operating system control. It is useful for legacy systems, custom workloads, and long-running applications that cannot be easily moved to a serverless pattern.

## Lambda

Lambda is best for short, event-driven logic such as transaction validation or fraud scoring. It removes the need to manage servers and is cost-efficient when the workload only runs occasionally.

## ECS

ECS is the better fit for container-based services that need to run continuously, such as APIs and microservices. It keeps the deployment model portable while still allowing the application to scale in a managed way.

## Comparison

| Service | Best use case | Why it fits |
|---|---|---|
| EC2 | Long-running or custom applications | Gives full infrastructure control |
| Lambda | Event-driven processing | Scales automatically and avoids idle cost |
| ECS | Containerised services | Supports reliable, scalable application deployment |

## FinTrust example

FinTrust can use EC2 for legacy workloads, Lambda for real-time fraud checks, and ECS for its core API services. The architecture becomes clearer when each service is matched to a workload rather than forcing one model onto everything. The transaction flow is shown in the [Week 2 architecture diagrams PDF](../diagrams/week02_architecture_diagrams.pdf).
