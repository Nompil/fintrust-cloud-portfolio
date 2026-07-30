\# Week 3 Storage Design



\## FinTrust S3 Buckets



\### 1. Transaction Archive Bucket



Bucket Name:



fintrust-transactions-af-south-1



Purpose:



Store transaction JSON records.



Storage Strategy:



\- S3 Standard (0-30 days)

\- S3 Standard-IA (31-90 days)

\- S3 Glacier Instant Retrieval (91-365 days)

\- S3 Glacier Deep Archive (366-1825 days)



Versioning:



Enabled



Object Lock:



Compliance Mode



Retention:



5 Years



\---



\### 2. Customer Statements Bucket



Bucket Name:



fintrust-statements-af-south-1



Purpose:



Store monthly PDF statements.



Storage Strategy:



\- S3 Standard



Versioning:



Enabled



Object Lock:



Not Required



\---



\### 3. ML Training Data Bucket



Bucket Name:



fintrust-ml-data-af-south-1



Purpose:



Store fraud detection training datasets.



Storage Strategy:



\- S3 Standard

\- Glacier Flexible Retrieval after 90 days



Versioning:



Enabled



Object Lock:



Governance Mode



\---



\## Lifecycle Rules



\### Transaction Records



\- Day 30 → Standard-IA

\- Day 90 → Glacier Instant Retrieval

\- Day 365 → Glacier Deep Archive

\- Day 1825 → Delete



\### ML Training Data



\- Day 90 → Glacier Flexible Retrieval



\---



\## Object Lock Decisions



\### Compliance Mode



Used for:



fintrust-transactions-af-south-1



Reason:



Financial transaction records must not be modified or deleted during the retention period.



\### Governance Mode



Used for:



fintrust-ml-data-af-south-1



Reason:



Allows controlled administrative overrides when necessary.



\---



\## Cost Comparison



All Data Stored in S3 Standard:



R24,000/month



Lifecycle-Based Tiering:



R4,200/month



Estimated Saving:



R19,800/month



\---



\## Summary



FinTrust uses three S3 buckets:



\- Transaction Records

\- Customer Statements

\- ML Training Data



Versioning is enabled on all buckets.



Object Lock Compliance Mode protects transaction records for five years.



Lifecycle policies automatically move data into cheaper storage classes to reduce costs while maintaining compliance requirements.

