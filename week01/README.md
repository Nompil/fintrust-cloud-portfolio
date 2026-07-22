# Week 1 - SQL Foundations and Programme Foundation

## Objective

The objective of Week 1 was to understand the structure of the Cloud to Solutions Accelerator programme, set up my professional GitHub portfolio, and build a strong foundation in relational databases and SQL using the FinTrust banking dataset.

This week introduced the technologies, concepts and business scenario that will be used throughout the programme while also developing my first SQL skills.

## Programme Foundation

Week 1 began with an overview of the 16-week Cloud to Solutions Accelerator programme and the journey toward AWS Certified Solutions Architect Associate (SAA-C03).

The programme is built around four learning streams:

- Cloud and AWS
- SQL and Data Engineering
- Python Programming
- Solutions Architecture

Rather than treating these as separate subjects, the programme combines them to build practical cloud-native solutions.

### My Learning Goal

Through this programme I aim to:

- Build cloud engineering skills
- Develop practical AWS knowledge
- Improve SQL and Python skills
- Design and build the FinTrust solution
- Prepare for the AWS SAA-C03 certification

## The Four Learning Streams

### Cloud and AWS

This stream focuses on AWS services relevant to the Solutions Architect Associate certification.

Topics include:

- Compute
- Storage
- Databases
- Networking
- Security
- High Availability
- Serverless Architecture

### SQL and Data Engineering

This stream focuses on working with structured data using relational databases and SQL.

Topics include:

- Database design
- Queries
- Reporting
- Aggregations
- Data analysis

### Python Programming

This stream develops programming skills used in automation, cloud computing and data processing.

Topics include:

- Variables
- Functions
- Modules
- File handling
- Data pipelines
- AWS Lambda development

### Solutions Architecture

This stream focuses on designing systems rather than only using services.

Topics include:

- Architectural decision making
- Security
- Scalability
- Reliability
- Performance optimisation
- Cost optimisation

## AWS SAA-C03 Certification Target

The AWS Certified Solutions Architect Associate certification is the primary certification target of this programme.

The exam focuses on four domains:

### Design Resilient Architectures

Weighting: 30%

Focus areas:

- High Availability
- Fault Tolerance
- Disaster Recovery
- Business Continuity

### Design High-Performing Architectures

Weighting: 28%

Focus areas:

- Databases
- Storage
- Compute performance
- Networking

### Design Secure Architectures

Weighting: 24%

Focus areas:

- IAM
- Encryption
- Access Management
- Security Controls

### Design Cost-Optimised Architectures

Weighting: 18%

Focus areas:

- Resource optimisation
- Pricing models
- Rightsizing
- Cost management

Understanding these domains helped me understand how each topic contributes toward certification readiness.

## The FinTrust Bank Scenario

All practical work throughout the programme is based on the FinTrust Bank case study.

FinTrust is a South African digital bank serving approximately 2.3 million customers and expanding rapidly.

The bank faces several challenges:

- Rapid customer growth
- POPIA compliance requirements
- Fraud detection requirements
- High transaction latency
- Capacity limitations in its on-premises environment

The objective of the programme is to design and progressively build a cloud-native transaction intelligence platform on AWS.

Each week contributes another component of the final solution.

## Core FinTrust Data Entities

### Customers

Key fields:

- customer_id
- first_name
- last_name
- id_number
- email
- phone
- province
- created_at

### Accounts

Key fields:

- account_id
- customer_id
- account_type
- account_number
- balance
- status

### Transactions

Key fields:

- transaction_id
- account_id
- transaction_type
- amount
- description
- merchant_category
- transaction_date
- reference_number

These entities form the foundation of the database work completed during Week 1.

## GitHub Portfolio

One of the most important lessons from Day 1 was understanding that GitHub is not simply a place to store files.

The portfolio repository acts as:

- A learning journal
- A professional portfolio
- Evidence of technical skills
- A study resource
- A record of growth throughout the programme

Repository structure:

```text
fintrust-cloud-portfolio
│
├── README.md
├── week01
├── week02
├── week03
└── future weeks
```

The repository will continue to grow throughout the programme and eventually contain the FinTrust capstone solution.

## Relational Databases

A relational database stores information in rows and columns organised into tables.

Each table represents a business entity.

Examples:

- Customers
- Accounts
- Transactions

The relationships between these entities are what make the database relational.

Example:

```text
Customers
    ↓
Accounts
    ↓
Transactions
```

This means:

- One customer can own multiple accounts.
- One account can contain multiple transactions.
- Every transaction belongs to an account.
- Every account belongs to a customer.

### Why This Matters

Relational databases reduce duplication, improve consistency and support accurate reporting.

These relationships are critical within banking environments where data integrity is essential.

## SQL Fundamentals

SQL stands for Structured Query Language.

SQL is used to:

- Retrieve data
- Insert data
- Update data
- Delete data
- Create databases
- Create tables
- Generate reports

### SELECT

Used to retrieve information.

Example:

```sql
SELECT first_name, last_name
FROM customers;
```

### INSERT

Used to add records.

Example:

```sql
INSERT INTO customers
(first_name, last_name)
VALUES
('Nompilo', 'Mchunu');
```

### UPDATE

Used to modify existing records.

Example:

```sql
UPDATE customers
SET province = 'KwaZulu-Natal'
WHERE customer_id = 1;
```

### DELETE

Used to remove records.

Example:

```sql
DELETE FROM customers
WHERE customer_id = 1;
```

## Database Design Concepts

### Primary Key

A unique identifier for each record.

Example:

```text
customer_id
```

### Foreign Key

Creates relationships between tables.

Example:

```text
accounts.customer_id
→ customers.customer_id
```

### NOT NULL

Prevents missing values.

### UNIQUE

Prevents duplicate values.

### AUTO_INCREMENT

Automatically generates unique identifiers.

## Data Types Learned

### VARCHAR

Stores text.

Examples:

- Names
- Email addresses
- Provinces

### INT

Stores whole numbers.

Examples:

- Customer IDs
- Account IDs

### DECIMAL

Stores precise financial values.

Examples:

- Account balances
- Transaction amounts

Important lesson:

Financial values should always use DECIMAL instead of FLOAT because DECIMAL provides accurate precision.

### DATETIME

Stores dates and timestamps.

### ENUM

Restricts a field to predefined values.

Example:

```sql
ENUM('CHEQUE','SAVINGS','CREDIT')
```

## Portfolio Deliverables

### day2_explore.sql

Objective:

Learn how to retrieve and explore data using SQL queries.

Tasks Completed:

- Displayed customer records using SELECT
- Retrieved specific columns
- Used column aliases
- Retrieved unique values using DISTINCT
- Limited query results using LIMIT
- Counted records using COUNT(*)
- Created calculated columns

Skills Practised:

- SELECT
- DISTINCT
- LIMIT
- COUNT
- Column aliases
- Calculated fields

Business Values

These queries form the foundation of reporting and analytics used throughout FinTrust.

### day3_fintrust_schema.sql

Objective:

Design and create the FinTrust database schema.

Tasks Completed:

- Created the database
- Created customers table
- Created accounts table
- Created transactions table
- Defined primary keys
- Defined foreign keys
-*Inserted sample records
- Verified table contents
- Verified record counts

Skills Practised:

- CREATE TATABASE
- CREATE TABLE
- INSERT INTO
- PRIMARY KEY
- FOREIGN KEY
- Data types
- Constraints

Business Value:

This schema models a simplified banking environment where customers own accounts and accounts contain transactions.

### day4_where_challenges.sql

Objective:

Answer business questions using SQL filtering techniques.

Tasks Completed:

- Queried customers from specific provinces
- Filtered accounts by balance thresholds
- Used LIKE for pattern matching
- Used IN to filter multiple values
- Used BETWEEN for ranges
- Used IS NULL and IS NOT NULL
- Combined conditions using AND and OR
- Excluded data using NOT
- Sorted results using ORDER BY

Skills Practised:

- WHERE
- LIKE
- IN
- BETWEEN
- IS NULL
- IS NOT NULL
- AND
- OR
- NOT
- ORDER BY

Business Value:

Filtering data is the foundation of business reporting, customer segmentation, fraud detection and analytics.

## AWS Connection

The concepts covered during Week 1 connect directly to Amazon RDS and Amazon Aurora.

The FinTrust schema created this week represents the type of relational database that could eventually be deployed on AWS.

Understanding relational database design is important because many cloud applications rely on structured and well-designed databases.

## Key Learning Outcomes

By the end of Week 1 I was able to:

- Understand the structure of the programme
- Explain the FinTrust case study
- Understand the AWS SAA-C03 certification target
- Create and manage a GitHub portfolio
- Understand relational database concepts
- Create databases and tables
- Define primary and foreign keys
- Insert records
- Query information using SQL
- Filter information using WHERE clauses
- Understand how structured data supports banking systems

## Week 1 Reflection

Week 1 provided a clear understanding of where the programme is heading and how SQL, Python, AWS and Solutions Architecture connect together.

The most valuable lesson was understanding that the technical skills I am learning are not isolated topics. They are all part of building the FinTrust cloud solution while preparing for the AWS Solutions Architect Associate certification.

I also learned that a GitHub repository is more than a place to store files. It serves as a professional portfolio, a study guide and a record of my learning journey throughout the programme.