\# FinTrust Resilience and Disaster Recovery Plan



\## Overview



This document describes the resilience, scalability, decoupling and disaster recovery strategy for the FinTrust cloud-native banking platform.



The design supports high availability, fault tolerance, customer growth, and regulatory compliance.



\---



\# Auto Scaling Group (ASG)



\## Configuration



\- Minimum Capacity: 2

\- Desired Capacity: 4

\- Maximum Capacity: 10



\## Availability Zones



\- af-south-1a

\- af-south-1b



\## Scaling Policies



\### Target Tracking



\- CPU Utilization Target: 60%



\### Scheduled Scaling



Month-end salary processing creates predictable traffic spikes.



Capacity increases from:



\- Desired: 4

\- Increased Capacity: 8



before the surge begins.



\## Benefits



\- Elastic scaling

\- High availability

\- Automatic recovery from instance failure



\---



\# Application Load Balancer (ALB)



\## Purpose



The ALB sits in front of the Auto Scaling Group and distributes traffic across healthy instances.



\## Path-Based Routing



Routes requests to:



\- /api/accounts/\*

\- /api/transactions/\*

\- /api/fraud-alerts/\*



\## Benefits



\- Single DNS endpoint

\- Single TLS certificate

\- HTTP/HTTPS awareness

\- Path-based routing

\- Integration with Lambda targets



\---



\# SQS Decoupling Pattern



\## Architecture



Mobile App

→ SQS Queue

→ Fraud Scoring Service



\## Purpose



Transaction processing is separated from fraud analysis.



If fraud processing slows down:



\- Transactions continue being accepted

\- Messages accumulate safely in the queue



\## Benefits



\- Failure isolation

\- Improved scalability

\- Better customer experience



\---



\# SNS Fan-Out Pattern



\## Architecture



Transaction Completed Event

→ SNS Topic



Consumers:



\- Customer Notification Service

\- Audit Logging Service

\- Analytics Service



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

