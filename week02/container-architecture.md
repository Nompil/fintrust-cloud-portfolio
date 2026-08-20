# FinTrust Container Architecture

## Service decisions

| FinTrust service | Container platform | Launch type | Scaling policy | Reason |
| --- | --- | --- | --- | --- |
| Transaction API | Amazon ECS | AWS Fargate | ECS Service Auto Scaling across two Availability Zones | Stateless API that must scale without managing EC2 hosts |
| Account Service | Amazon ECS | AWS Fargate | Scale independently from the Transaction API | Independent microservice with different demand patterns |
| Fraud Batch Processor | Amazon ECS | AWS Fargate | EventBridge starts tasks when required; no tasks run between jobs | Processing can exceed Lambda's 15-minute limit |
| Compliance Report Generator | AWS Lambda | Not applicable | One invocation from a monthly EventBridge schedule | Short, infrequent task with no reason to pay for idle compute |

The Transaction API should keep at least two healthy tasks distributed across two Availability Zones. A target-tracking policy can add or remove tasks using measured CPU utilisation or Application Load Balancer request count. The final threshold and maximum task count must be based on load-test results.

## Architecture

The container design is shown in the [Week 2 architecture diagrams PDF](diagrams/week02_architecture_diagrams.pdf).

Container images are stored in Amazon ECR in `af-south-1`. ECS deploys those images as stateless Fargate tasks. Application state is kept outside the containers so either task can serve any request and failed tasks can be replaced safely.

## Why ECS on Fargate

ECS fits an AWS-first team that does not need Kubernetes. Fargate removes host provisioning and patching while retaining container packaging and service-level scaling. EKS would add unnecessary Kubernetes operational complexity, while ECS on EC2 would require the team to manage cluster instances.
