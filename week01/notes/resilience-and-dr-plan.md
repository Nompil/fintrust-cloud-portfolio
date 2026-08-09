# FinTrust Resilience and Disaster Recovery Plan

FinTrust needs a layered resilience strategy that combines scaling, traffic distribution, message decoupling, and disaster recovery planning.

## Auto Scaling Group

- Minimum capacity: 2
- Desired capacity: 4
- Maximum capacity: 10
- Availability Zones: af-south-1a and af-south-1b

Scaling policy approach:
- Target Tracking at 60% CPU for steady-state behaviour
- Scheduled Scaling before month-end peaks

## Application Load Balancer

The ALB sits in front of the Auto Scaling Group and distributes traffic across healthy targets. It supports path-based routing for the accounts, transactions, and fraud-alerts services.

## SQS Decoupling

The mobile app submits payment events to an SQS queue, and the fraud-scoring service consumes them independently. This prevents a slowdown in fraud processing from blocking customer transactions.

## SNS Fan-Out

A transaction-completed event is published to an SNS topic and fan-out to the notification, audit logging, and analytics consumers.

## Disaster Recovery

FinTrust should use a Pilot Light strategy with encrypted backups and a minimal standby environment in eu-west-1. This supports an RPO of around 15 minutes and an RTO below one hour while avoiding the cost of a fully active secondary environment.



\## Benefits



\- Independent processing

\- Reduced service coupling

\- Easier scaling



\---



\# Disaster Recovery Strategy



\## Primary Region



Africa (Cape Town)



```text

af-south-1

```



\## Disaster Recovery Region



Europe (Ireland)



```text

eu-west-1

```



\## DR Model



Pilot Light Disaster Recovery



\## Components



\- Encrypted nightly database snapshots

\- S3 data replication

\- Minimal standby database

\- Route 53 failover capability



\---



\# Recovery Objectives



\## RPO (Recovery Point Objective)



15 minutes



Maximum acceptable data loss after a disaster.



\## RTO (Recovery Time Objective)



Less than 1 hour



Maximum acceptable service recovery time.



\---



\# Failure Scenarios



\## Scenario 1



\### Failure



EC2 instance crashes



\### Protection



Auto Scaling Group health checks



\### Outcome



Replacement instance launches automatically from the Golden AMI.



\---



\## Scenario 2



\### Failure



Availability Zone outage



\### Protection



Multi-AZ Auto Scaling Group and ALB



\### Outcome



Traffic shifts to healthy resources in another AZ.



\---



\## Scenario 3



\### Failure



Fraud-scoring service overloaded



\### Protection



SQS Queue



\### Outcome



Transactions continue while requests wait safely in the queue.



\---



\## Scenario 4



\### Failure



Month-end transaction volume triples



\### Protection



Scheduled Scaling



\### Outcome



Capacity increases before the traffic spike begins.



\---



\## Scenario 5



\### Failure



Regional outage in af-south-1



\### Protection



Pilot Light DR in eu-west-1



\### Outcome



Standby infrastructure scales up and Route 53 redirects traffic.



Target:



\- RPO: 15 minutes

\- RTO: Less than 1 hour



\---



\# Architecture Summary



Users

→ Route 53

→ CloudFront

→ Application Load Balancer

→ Auto Scaling Group

→ Transaction Services



Additional Services:



\- Amazon SQS

\- Amazon SNS

\- Amazon S3

\- Amazon RDS PostgreSQL

\- Disaster Recovery Region (eu-west-1)



This design supports FinTrust's goals of high availability, compliance, fraud detection, fault tolerance and customer growth.

