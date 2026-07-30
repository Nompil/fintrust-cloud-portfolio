\# Week 3 Storage Security



\## Overview



FinTrust secures all S3 buckets using IAM roles, bucket policies, encryption, pre-signed URLs, and Block Public Access.



The goal is to protect customer information and meet POPIA compliance requirements.



\---



\## Transaction Bucket Security



Bucket:



fintrust-transactions-af-south-1



\### Bucket Policy



```json

{

&#x20; "Version": "2012-10-17",

&#x20; "Statement": \[

&#x20;   {

&#x20;     "Sid": "DenyInsecureTransport",

&#x20;     "Effect": "Deny",

&#x20;     "Principal": "\*",

&#x20;     "Action": "s3:\*",

&#x20;     "Resource": \[

&#x20;       "arn:aws:s3:::fintrust-transactions-af-south-1",

&#x20;       "arn:aws:s3:::fintrust-transactions-af-south-1/\*"

&#x20;     ],

&#x20;     "Condition": {

&#x20;       "Bool": {

&#x20;         "aws:SecureTransport": "false"

&#x20;       }

&#x20;     }

&#x20;   },

&#x20;   {

&#x20;     "Sid": "AllowAuditRoleReadOnly",

&#x20;     "Effect": "Allow",

&#x20;     "Principal": {

&#x20;       "AWS": "arn:aws:iam::123456789012:role/FinTrust-Audit-Role"

&#x20;     },

&#x20;     "Action": \[

&#x20;       "s3:GetObject",

&#x20;       "s3:ListBucket"

&#x20;     ],

&#x20;     "Resource": \[

&#x20;       "arn:aws:s3:::fintrust-transactions-af-south-1",

&#x20;       "arn:aws:s3:::fintrust-transactions-af-south-1/\*"

&#x20;     ]

&#x20;   }

&#x20; ]

}

