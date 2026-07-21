\# Week 1 - SQL Foundations



\## Objective



The objective of Week 1 was to build a foundation in relational databases and SQL using the FinTrust banking dataset.



Throughout the week, I learned how data is structured, stored and queried within a relational database. I also learned how to create database tables, establish relationships between them, insert data, and retrieve information using SQL.



The concepts covered this week provide the foundation for all future database work within the FinTrust project.



\---



\## Relational Databases



A relational database stores information in tables made up of rows and columns.



Each table represents a specific business entity.



Examples:



\- Customers

\- Accounts

\- Transactions



The relationships between these entities are what make the database relational.



Example:



```text

Customers → Accounts → Transactions

```



This means:



\- One customer can have multiple accounts.

\- One account can have multiple transactions.

\- Every transaction belongs to an account.

\- Every account belongs to a customer.



\### Why This Matters



Relational databases prevent unnecessary duplication of information and help ensure data remains accurate and consistent.



In a banking environment, these relationships are critical because customer, account and transaction information must always remain reliable.



\---



\## SQL Fundamentals



SQL stands for Structured Query Language.



SQL is used to interact with relational databases.



The main SQL operations are:



\### SELECT



Retrieves data from a database.



Example:



```sql

SELECT first\_name, last\_name

FROM customers;

```



\### INSERT



Adds new records.



Example:



```sql

INSERT INTO customers

(first\_name, last\_name)

VALUES

('Thabo', 'Nkosi');

```



\### UPDATE



Modifies existing records.



Example:



```sql

UPDATE customers

SET province = 'Gauteng'

WHERE customer\_id = 1;

```



\### DELETE



Removes records.



Example:



```sql

DELETE FROM customers

WHERE customer\_id = 1;

```



\---



\## Data Types



I learned that every column must have a data type.



Common data types used during the week:



\### VARCHAR



Stores text.



Examples:



\- First names

\- Last names

\- Emails



\### INT



Stores whole numbers.



Examples:



\- Customer IDs

\- Account IDs



\### DECIMAL



Stores exact financial values.



Example:



```sql

DECIMAL(15,2)

```



Used for:



\- Account balances

\- Transaction amounts



Important lesson:



Financial values should be stored using DECIMAL rather than FLOAT because DECIMAL maintains accuracy.



\### DATETIME



Stores dates and times.



Examples:



\- Transaction dates

\- Record creation dates



\### ENUM



Restricts values to predefined options.



Example:



```sql

ENUM('CHEQUE','SAVINGS','CREDIT','BUSINESS')

```



This helps maintain data quality.



\---



\## Database Constraints



Constraints help protect data integrity.



\### PRIMARY KEY



Uniquely identifies every record.



Example:



```text

customer\_id

```



\### FOREIGN KEY



Creates relationships between tables.



Example:



```text

accounts.customer\_id

→ customers.customer\_id

```



\### NOT NULL



Prevents missing values.



\### UNIQUE



Prevents duplicate entries.



Example:



```text

email address

```



\### AUTO\_INCREMENT



Automatically generates sequential IDs.



\---



\# Portfolio Deliverables



\## day2\_explore.sql



\### Objective



Learn how to retrieve and explore data from the FinTrust database using basic SQL queries.



\### Tasks Completed



1\. Displayed all customer records using SELECT \*

2\. Retrieved specific columns from the customers table

3\. Used column aliases to improve readability

4\. Retrieved unique provinces using DISTINCT

5\. Limited query results using LIMIT

6\. Counted records using COUNT(\*)

7\. Created calculated columns for projected account balances



\### Key Skills Practised



\- SELECT

\- DISTINCT

\- LIMIT

\- COUNT

\- Column aliases

\- Calculated columns



\### Important Examples



Select specific columns:



```sql

SELECT first\_name, last\_name, province

FROM customers;

```



Retrieve unique provinces:



```sql

SELECT DISTINCT province

FROM customers;

```



Count customer records:



```sql

SELECT COUNT(\*) AS customer\_count

FROM customers\*

```



Calculate projected balances\*



```sql

SELECT

&#x20;   account\_number\*

&#x20;   balance,

&#x20;   balance \* 1.10 A\* projected\_balance

FROM accounts;

\*``



\### Business Value



These quer\*es form the foundation of customer\*reporting, dashboard creation and \*usiness intelligence analysis.



\--\*



\## day3\_fintrust\_schema.sql



\###\*Objective



Design and build the Fi\*Trust database schema from scratch\*



\### Tasks Completed



1\. Created \*he fintrust\_db database

2\. Created\*the customers table

3\. Created the\*accounts table

4\. Created the tran\*actions table

5\. Added primary key\*

6\. Added foreign keys

7\. Inserted\*customer records

8\. Inserted accou\*t records

9\. Inserted transaction \*ecords

10\. Verified inserted data

\*1. Validated record counts



\### Ke\* Skills Practised



\- CREATE DATABA\*E

\- CREATE TABLE

\- INSERT INTO

\- P\*IMARY KEY

\- FOREIGN KEY

\- Data typ\*s

\- Constraints



\### Tables Create\*



\#### customers



Stores customer \*nformation.



Key fields:



\- custom\*r\_id

\- first\_name

\- last\_name

\- em\*il

\- province



\#### accounts



Stor\*s banking account information.



Ke\* fields:



\- account\_id

\- customer\_\*d

\- account\_type

\- account\_number

\* balance



\#### transactions



Store\* transaction records.



Key fields:\*

\- transaction\_id

\- account\_id

\- t\*ansaction\_type

\- amount

\- merchant\*category



\### Database Relationshi\*s



```text

customers

&#x20;   │

&#x20;   └──\*customer\_id

&#x20;          │

&#x20;        \* ▼

accounts

&#x20;   │

&#x20;   └── account\_\*d

&#x20;          │

&#x20;          ▼

transa\*tions

```



\### Business Value



Thi\* schema represents a simplified ve\*sion of a banking system where cus\*omers own accounts and accounts co\*tain transactions.



\---



\## day4\_w\*ere\_challenges.sql



\### Objective

\*Use filtering techniques to answer\*business questions using SQL.



\###\*Tasks Completed



1\. Queried custom\*rs from specific provinces

2\. Filt\*red accounts by balance thresholds\*3. Found records using LIKE

4\. Use\* IN to match multiple values

5\. Us\*d BETWEEN for ranges

6\. Used IS NU\*L and IS NOT NULL

7\. Combined cond\*tions using AND

8\. Combined condit\*ons using OR

9\. Used NOT to exclud\* records

10\. Sorted results using \*RDER BY

11\. Built business-focused\*reporting queries



\### Key Skills \*ractised



\- WHERE

\- LIKE

\- IN

\- BE\*WEEN

\- IS NULL

\- IS NOT NULL

\- AND\*- OR

\- NOT

\- ORDER BY



\### Importa\*t Examples



Find customers from Ga\*teng:



```sql

SELECT \*

FROM custom\*rs

WHERE province = 'Gauteng';

```\*

Find Gmail customers:



```sql

SEL\*CT \*

FROM customers

WHERE email LI\*E '%gmail%';

```



Find balances wi\*hin a range:



```sql

SELECT \*

FROM\*accounts

WHERE balance BETWEEN 100\* AND 50000;

```



Find records with\*missing values:



```sql

SELECT \*

F\*OM transactions

WHERE merchant\_cat\*gory IS NULL;

```



Combine multipl\* conditions:



```sql

SELECT \*

FROM\*accounts

WHERE account\_type = 'SAV\*NGS'

AND balance > 5000;

```



\### \*usiness Value



Filtering data is o\*e of the most common activities in\*reporting and analytics.



These qu\*ries form the foundation of:



\- Cu\*tomer segmentation

\- Fraud detecti\*n

\- Financial reporting

\- Business\*intelligence dashboards



\---



\## A\*S Connection



The concepts covered\*this week connect directly to Amaz\*n RDS.



Amazon RDS is AWS's manage\* relational database service.



The\*FinTrust database created during t\*is week could be hosted using:



\- \*mazon RDS MySQL

\- Amazon RDS Postg\*eSQL

\- Amazon Aurora



Understandin\* database design and SQL querying \*ill be important when working with\*cloud-hosted databases later in th\* programme.



\---



\## Key Learning \*utcomes



By the end of Week 1 I wa\* able to:



\- Understand relational\*database concepts

\- Create databases and tables

\- Define primary and foreign keys

\- Insert records into tables

\- Query data using SELECT statements

\- Filter data using WHERE clauses

\- Build relationships between tables

\- Understand how structured data supports banking systems



\---



\## Reflection



This week taught me that databases are much more than collections of tables.



A well-designed database creates meaningful relationships between business entities and ensures data remains accurate, consistent and useful.



The most valuable lesson for me was understanding how customers, accounts and transactions connect together to form a complete banking system.



The SQL skills developed this week provide the foundation for future FinTrust reporting, analytics and cloud database solutions.

