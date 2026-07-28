\# FinTrust Data Model



\## Overview



The FinTrust transaction intelligence system is built around three core entities:



1\. Customers

2\. Accounts

3\. Transactions



These entities form the foundation of the banking platform and support customer management, account management, transaction processing, reporting and fraud detection.



\---



\# Entity Relationship Diagram



CUSTOMERS (1) ------< ACCOUNTS (1) ------< TRANSACTIONS (Many)



A customer can own multiple accounts.



An account can have multiple transactions.



\---



\# CUSTOMERS



Stores customer information.



\## Attributes



\- customer\_id (Primary Key)

\- first\_name

\- last\_name

\- id\_number

\- email

\- phone

\- province

\- created\_at



\## Business Purpose



The Customers table stores personal and contact information for FinTrust customers.



\---



\# ACCOUNTS



Stores banking account information.



\## Attributes



\- account\_id (Primary Key)

\- customer\_id (Foreign Key)

\- account\_type

\- account\_number

\- balance

\- status



\## Account Types



\- CHEQUE

\- SAVINGS

\- CREDIT



\## Status Values



\- ACTIVE

\- SUSPENDED



\## Business Purpose



The Accounts table stores account details and links each account to a customer.



\---



\# TRANSACTIONS



Stores financial transaction information.



\## Attributes



\- transaction\_id (Primary Key)

\- account\_id (Foreign Key)

\- type

\- amount

\- description

\- merchant\_category

\- transaction\_date

\- reference\_no



\## Transaction Types



\- DEBIT

\- CREDIT

\- PAYMENT



\## Business Purpose



The Transactions table records all financial activity for customer accounts and provides data for reporting, auditing and fraud detection.



\---



\# Relationships



\## Customer → Accounts



One customer can own multiple accounts.



Example:



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

