\# FinTrust Compute Decision Map



\## Overview



FinTrust uses multiple AWS compute services because different workloads have different requirements.



There is no single "best" compute service.



The correct service depends on:



\- Runtime length

\- Scalability requirements

\- Operational overhead

\- Cost requirements

\- Infrastructure access needs



\---



\# FinTrust Compute Portfolio



\## Transaction API



\### Compute Choice



Amazon ECS on Fargate



\### Reason



\- Stateless microservice

\- Auto-scaling

\- Multi-AZ deployment

\- No infrastructure management



\### What Would Break If We Chose The Wrong Service?



Using Lambda could introduce cold-start delays and API limitations for long-running requests.



\---



\## Account Service



\### Compute Choice



Amazon ECS on Fargate



\### Reason



\- Independent scaling

\- Simple API workloads

\- No EC2 management



\### What Would Break If We Chose The Wrong Service?



Running continuously on EC2 would increase operational overhead and maintenance effort.



\---



\## Fraud Batch Processor



\### Compute Choice



Amazon ECS on Fargate



\### Reason



\- Runtime exceeds 15 minutes

\- EventBridge-triggered

\- Containerized workload



\### What Would Break If We Chose The Wrong Service?



Lambda cannot run longer than 15 minutes.



\---



\## Compliance Report Generator



\### Compute Choice



AWS Lambda



\### Reason



\- Runs once per month

\- Short execution time

\- Near-zero idle cost



\### What Would Break If We Chose The Wrong Service?



Using EC2 would require paying for infrastructure that sits idle most of the month.



\---



\## Internal Admin Portal



\### Compute Choice



AWS Elastic Beanstalk



\### Reason



\- Managed deployment platform

\- Auto Scaling

\- Load Balancer included

\- SSH access available when needed



\### What Would Break If We Chose The Wrong Service?



Fargate does not provide direct server access for troubleshooting and debugging.



\---



\## Nightly Account Reconciliation



\### Compute Choice



AWS Batch with Spot Capacity



\### Reason



\- Approximately 80,000 jobs nightly

\- CPU-intensive processing

\- Dynamic scaling

\- Cost optimization using Spot Instances



\### What Would Break If We Chose The Wrong Service?



Managing thousands of Lambda invocations would increase complexity and make orchestration difficult.



\---



\## Customer Mobile App Backend



\### Compute Choice



API Gateway + Lambda + DynamoDB



\### Reason



\- Serverless architecture

\- Auto-scaling

\- Event-driven

\- Low operational overhead



\### What Would Break If We Chose The Wrong Service?



Always-on EC2 infrastructure would increase cost and reduce elasticity.



\---



\# Fargate Decision Guide



Use ECS Fargate when:



\- Applications are containerized

\- Workloads are stateless

\- No server management is desired

\- Automatic scaling is needed



Examples:



\- Transaction API

\- Account Service

\- Fraud Processing



\---



\# Elastic Beanstalk Decision Guide



Use Elastic Beanstalk when:



\- Developers want rapid deployment

\- Infrastructure should be managed

\- Server access is still required



Examples:



\- Internal admin applications

\- Legacy web applications



\---



\# AWS Batch Decision Guide



Use AWS Batch when:



\- Thousands of jobs must run

\- Processing is CPU-intensive

\- Long-running workloads exist

\- Spot Instances can reduce costs



Examples:



\- Reconciliation processing

\- Financial calculations

\- Large analytics workloads



\---



\# Serverless API Components



\## API Gateway



Provides:



\- REST APIs

\- HTTP APIs

\- WebSocket APIs



Acts as the entry point for client requests.



\---



\## Step Functions



Provides:



\- Workflow orchestration

\- Retry handling

\- Error handling

\- Multi-step business processes



\---



\## AppSync



Provides:



\- Managed GraphQL APIs

\- Real-time subscriptions

\- Flexible client queries



\---



\# FinTrust Architecture Summary



Customer Request

&#x20;       ↓

Route 53

&#x20;       ↓

CloudFront

&#x20;       ↓

Application Load Balancer

&#x20;       ↓

ECS Fargate Services



Additional Compute Services



\- Lambda

\- Elastic Beanstalk

\- AWS Batch



Future Serverless Layer



\- API Gateway

\- Step Functions

\- AppSync



This compute portfolio allows FinTrust to use the most appropriate AWS service for each workload while optimizing cost, scalability and operational efficiency.

