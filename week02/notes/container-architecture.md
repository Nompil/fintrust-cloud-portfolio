\# FinTrust Container Architecture



\## Overview



Containers package an application together with its dependencies, runtime, libraries and configuration into a single portable unit.



This solves the classic problem:



> "It works on my machine but not on the server."



Containers ensure applications run consistently across development, testing and production environments.



\---



\# Containers vs EC2 vs Lambda



\## EC2 (Virtual Machines)



Characteristics:



\- Full operating system isolation

\- Requires OS management

\- Requires patching

\- Startup measured in minutes

\- Unlimited runtime



FinTrust Use Case:



\- Traditional transaction processing servers

\- Long-running workloads



\---



\## Containers (ECS)



Characteristics:



\- Package application and dependencies together

\- Fast startup

\- Highly portable

\- Share operating system kernel

\- Unlimited runtime



FinTrust Use Case:



\- API microservices

\- Account service

\- Fraud processing



\---



\## Lambda



Characteristics:



\- Serverless

\- No servers to manage

\- Event driven

\- Pay only while code runs

\- Maximum runtime: 15 minutes



FinTrust Use Case:



\- Monthly compliance reports

\- Event-driven automation

\- Future fraud-scoring functions



\---



\# Docker Fundamentals



\## Docker Image



Definition:



A read-only blueprint containing:



\- Application code

\- Libraries

\- Dependencies

\- Runtime



Example:



```text

fintrust-api:v1.0

```



Characteristics:



\- Immutable

\- Versioned

\- Stored in Amazon ECR



\---



\## Container



Definition:



A running instance of an image.



Characteristics:



\- Isolated runtime environment

\- Running or stopped state

\- Multiple containers can use the same image



\---



\## Registry



Definition:



Storage location for images.



FinTrust uses:



```text

Amazon ECR

```



Benefits:



\- Private

\- Secure

\- AWS integrated

\- POPIA-compliant regional storage



\---



\## Dockerfile



Definition:



Instructions used to build a Docker image.



Example components:



\- Base image

\- Application code

\- Dependencies

\- Startup command



\---



\# ECS vs EKS vs ECS Anywhere



\## Amazon ECS



AWS-native container orchestration service.



Benefits:



\- Simpler than Kubernetes

\- Integrates with:

&#x20; - ALB

&#x20; - IAM

&#x20; - CloudWatch

&#x20; - ECR

\- Recommended FinTrust starting point



FinTrust Decision:



```text

Use ECS

```



\---



\## Amazon EKS



Managed Kubernetes service.



Benefits:



\- Kubernetes standard

\- Multi-cloud portability



Challenges:



\- More operational complexity

\- Requires Kubernetes expertise



FinTrust Decision:



```text

Possible future option

Not required today

```



\---



\## Amazon ECS Anywhere



Extends ECS management to on-premises servers.



Use Cases:



\- Hybrid environments

\- Existing data centre workloads



FinTrust Decision:



```text

Not used currently

All workloads run in AWS

```



\---



\# ECS Launch Types



\## ECS Fargate



Serverless containers.



Advantages:



\- No EC2 management

\- Automatic scaling

\- No capacity planning

\- Per-second billing



FinTrust Recommendation:



```text

Primary deployment model

```



\---



\## ECS on EC2



Containers run on self-managed EC2 instances.



Advantages:



\- Hardware control

\- Custom AMIs

\- GPU support



Disadvantages:



\- EC2 management required

\- More operational effort



FinTrust Recommendation:



```text

Only if special hardware is needed

```



\---



\# FinTrust Container Architecture



\## Transaction API



Platform:



```text

Amazon ECS

```



Launch Type:



```text

Fargate

```



Reason:



\- Stateless

\- Auto-scaling

\- No server administration



\---



\## Account Service



Platform:



```text

Amazon ECS

```



Launch Type:



```text

Fargate

```



Reason:



\- Independent scaling

\- Microservice architecture



\---



\## Fraud Batch Processor



Platform:



```text

Amazon ECS

```



Launch Type:



```text

Fargate

```



Reason:



\- Long-running workload

\- Greater than 15 minutes

\- Lambda unsuitable



\---



\## Monthly Report Generator



Platform:



```text

AWS Lambda

```



Reason:



\- Short execution time

\- Runs infrequently

\- Near-zero idle cost



\---



\# Stateless Container Principle



Containers should not store state locally.



Persistent data belongs in:



\## Amazon RDS



\- Customer data

\- Account data

\- Transaction data



\## Amazon S3



\- Reports

\- Archives

\- Backups



\## ElastiCache



\- Session storage

\- Temporary application state



Benefits:



\- Horizontal scaling

\- Fault tolerance

\- Easier recovery



\---



\# FinTrust Architecture Diagram



Users

↓

Route 53

↓

CloudFront

↓

Application Load Balancer

↓

Amazon ECS

(Fargate)

↓

Transaction API Containers

↓

Amazon RDS PostgreSQL



Supporting Services:



\- Amazon ECR

\- Amazon CloudWatch

\- Amazon S3

\- AWS Lambda



\---



\# Key Exam Decision Rules



Scenario:



New containerized application with no Kubernetes experience.



Answer:



```text

Amazon ECS + Fargate

```



\---



Scenario:



Existing Kubernetes workloads.



Answer:



```text

Amazon EKS

```



\---



Scenario:



Containers on on-premises servers.



Answer:



```text

Amazon ECS Anywhere

```



\---



Scenario:



Short event-driven workload under 15 minutes.



Answer:



```text

AWS Lambda

```



\---



\# FinTrust Business Benefits



This architecture supports:



\- Customer growth

\- High availability

\- Auto-scaling

\- Reduced operational complexity

\- Faster deployments

\- Lower infrastructure management overhead

\- Cost optimization

