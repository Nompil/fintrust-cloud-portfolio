# FinTrust Compute Decision Map

By this point, FinTrust already feels less like a training exercise and more like a real platform design. The clearest lesson is that there is no single compute service that is best in every case. Each workload needs a different fit.

## Why the choices differ

The right service depends on whether the workload is:

- always on or only triggered occasionally
- short-lived or long-running
- event-driven or scheduled
- simple or highly CPU-intensive
- something that needs direct server access or something that should stay fully managed

## FinTrust compute portfolio

| Service | Compute choice | Why it fits | What would break if the wrong choice was made? |
|---|---|---|---|
| Transaction API | ECS on Fargate | It is a stateless service that needs to scale cleanly and stay available without the overhead of managing EC2 hosts | A Lambda-based design would be too restrictive for a persistent API experience |
| Account Service | ECS on Fargate | It can scale independently and stay simple to deploy as a container-based service | Running it on EC2 would add unnecessary operational work |
| Fraud Batch Processor | ECS on Fargate | It is long-running and container-based, so it is better suited to Fargate than Lambda | Lambda would fail once the runtime exceeded its 15-minute limit |
| Compliance Report Generator | AWS Lambda | It runs on a schedule and completes quickly, so it is low-cost and efficient | Using EC2 here would leave infrastructure idle most of the month |
| Internal Admin Portal | AWS Elastic Beanstalk | It gives the team a managed deployment model while still allowing direct server access for debugging | Fargate would make troubleshooting much less practical |
| Nightly Account Reconciliation | AWS Batch with Spot | It handles a large number of CPU-intensive jobs efficiently and keeps cost down | A Lambda-only approach would be messy and expensive for this volume of work |
| Customer-facing mobile app backend | API Gateway + Lambda + DynamoDB | This is the canonical serverless pattern for lightweight, event-based APIs | A traditional server model would be heavier than necessary for this workload |

## My takeaway

The biggest lesson is that the best architecture is usually the one that matches the workload. FinTrust does not need one compute service for everything. It needs the right service for the right job.
