# FinTrust Data Model

The FinTrust data model is built around three core entities: customers, accounts, and transactions. Together they support banking operations, reporting, and analytics.

## Entity Relationship Summary

Customers -> Accounts -> Transactions

- One customer can have many accounts
- One account can have many transactions

## Customers

Purpose: store customer identity and contact information.

Key fields:
- customer_id
- first_name
- last_name
- email
- province
- created_at

## Accounts

Purpose: store account details for each customer.

Key fields:
- account_id
- customer_id
- account_type
- account_number
- balance
- status

## Transactions

Purpose: store financial activity for each account.

Key fields:
- transaction_id
- account_id
- transaction_type
- amount
- merchant_category
- transaction_date

## Why This Model Matters

This structure reflects a realistic banking relationship model. It supports referential integrity, clear reporting logic, and scalable analytics for fraud detection and customer insights.



Customer:

\- John Smith



Accounts:

\- Savings Account

\- Cheque Account



\---



\## Account → Transactions



One account can contain multiple transactions.



Example:



Account:

\- Cheque Account



Transactions:

\- Debit Card Purchase

\- ATM Withdrawal

\- Salary Deposit



\---



\# Final Architecture Relevance



These three entities form the core data model of the FinTrust cloud-native transaction intelligence system.



Future AWS services that will use this data include:



\- Amazon RDS PostgreSQL

\- AWS Lambda

\- Amazon S3

\- Amazon Athena

\- Amazon QuickSight

\- Amazon CloudWatch



The data stored in these entities will support:



\- Transaction processing

\- Fraud detection

\- Customer reporting

\- Business analytics

\- Regulatory compliance

