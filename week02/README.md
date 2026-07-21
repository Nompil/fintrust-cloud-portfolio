\# Week 2 - Python Fundamentals and SQL Reporting



\## Objective



The objective of Week 2 was to develop foundational Python programming skills while continuing to strengthen SQL reporting knowledge.



This week focused on understanding how applications make decisions, how data can be analysed using SQL, and how AWS compute services support business applications.



The concepts learned during this week form the basis of transaction processing, reporting and automation within the FinTrust environment.



\---



\## Python Fundamentals



Python is a high-level programming language commonly used for automation, cloud computing, data analysis and application development.



Throughout this week I learned how Python can be used to solve business problems by translating business rules into code.



\---



\## Variables and Data Types



Variables are used to store information that can be referenced throughout a program.



Examples:



```python

customer\_name = "Thabo"

balance = 15000.50

is\_active = True

```



Common data types:



\### String



Stores text.



Example:



```python

first\_name = "Nompilo"

```



\### Integer



Stores whole numbers.



Example:



```python

customer\_id = 101

```



\### Float



Stores decimal values.



Example:



```python

balance = 2500.75

```



\### Boolean



Stores either:



```python

True

False

```



Example:



```python

account\_active = True

```



\---



\## Conditional Statements



Conditional statements allow a program to make decisions.



\### if



Executes a block of code when a condition is true.



Example:



```python

if balance > 10000:

&#x20;   print("Premium Account")

```



\### elif



Checks additional conditions.



Example:



```python

elif balance > 5000:

&#x20;   print("Standard Account")

```



\### else



Runs when no previous conditions are true.



Example:



```python

else:

&#x20;   print("Basic Account")

```



\### Business Value



Conditional statements are used to automate business decisions such as:



\- Transaction approval

\- Account classification

\- Risk assessment

\- Customer segmentation



\---



\## Comparison Operators



Used to compare values.



| Operator | Meaning |

|-----------|-----------|

| == | Equal to |

| != | Not equal to |

| > | Greater than |

| < | Less than |

| >= | Greater than or equal |

| <= | Less than or equal |



Example:



```python

if balance >= 10000:

&#x20;   print("Eligible")

```



\---



\## Boolean Logic



Boolean logic allows multiple conditions to be evaluated.



\### AND



Both conditions must be true.



```python

if balance > 5000 and account\_type == "SAVINGS":

```



\### OR



Only one condition must be true.



```python

if province == "Gauteng" or province == "Western Cape":

```



\### NOT



Reverses a condition.



```python

if not account\_active:

```



\### Business Value



Boolean logic makes it possible to build realistic business rules.



\---



\## Membership Testing



Membership testing checks whether a value exists within a collection.



Example:



```python

if province in provinces\_list:

```



Use cases:



\- Validation

\- Access control

\- Product selection

\- Region-based processing



\---



\# SQL Reporting



Week 2 continued building SQL knowledge through reporting and aggregation.



\---



\## SQL JOINS



JOINs are used to combine information from multiple tables.



\### INNER JOIN



Returns records when matching values exist in both tables.



Example:



```sql

SELECT \*

FROM customers

INNER JOIN accounts

ON customers.customer\_id = accounts.customer\_id;

```



Business Value:



Links customers to their accounts.



\---



\### LEFT JOIN



Returns all records from the left table even if matching records do not exist in the right table.



Example:



```sql

SELECT \*

FROM customers

LEFT JOIN accounts

ON customers.customer\_id = accounts.customer\_id;

```



Business Value:



Shows all customers including those without accounts.



\---



\### Multi-Table Joins



Combine information from multiple related tables.



Example:



```text

Customers

&#x20;   ↓

Accounts

&#x20;   ↓

Transactions

```



Business Value:



Provides complete business reports.



\---



\## Aggregate Functions



Aggregate functions summarise large amounts of data.



\### COUNT()



Counts rows.



```sql

SELECT COUNT(\*)

FROM accounts;

```



\### SUM()



Calculates totals.



```sql

SELECT SUM(balance)

FROM accounts;

```



\### AVG()



Calculates averages.



```sql

SELECT AVG(balance)

FROM accounts;

```



\### MIN()



Returns the lowest value.



```sql

SELECT MIN(balance)

FROM accounts;

```



\### MAX()



Returns the highest value.



```sql

SELECT MAX(balance)

FROM accounts;

```



\### Business Value



Aggregate functions power dashboards, reports and management insights.



\---



\## GROUP BY



Groups data into categories.



Example:



```sql

SELECT account\_type, COUNT(\*)

FROM accounts

GROUP BY account\_type;

```



Business Value:



Creates summary reports by category.



\---



\## HAVING



Filters grouped data after aggregation.



Example:



```sql

SELECT province, COUNT(\*)

FROM customers

GROUP BY province

HAVING COUNT(\*) > 10;

```



Business Value:



Identifies significant groupings and trends.



\---



\## CASE Statements



Allows conditional logic inside SQL queries.



Example:



```sql

CASE

&#x20;   WHEN balance > 10000 THEN 'High Balance'

&#x20;   ELSE 'Standard'

END

```



Business Value:



Generates business classifications directly within reports.



\---



\# Portfolio Deliverables



\## hello\_fintrust.py



\### Objective



Create a basic Python program and become familiar with running Python scripts.



\### Skills Practised



\- Python syntax

\- Variables

\- Printing output



\---



\## day3\_exercises.py



\### Objective



Practise Python fundamentals.



\### Skills Practised



\- Variables

\- Data types

\- Expressions

\- Operators



\---



\## conditionals.py



\### Objective



Create business rules using conditional statements.



\### Skills Practised



\- if

\- elif

\- else

\- Boolean logic



\### Business Value



Simulates account and transaction decision making.



\---



\## transaction\_flowchart.py



\### Objective



Model transaction approval logic.



\### Skills Practised



\- Business rules

\- Decision trees

\- Conditional processing



\### Business Value



Represents how transaction systems make approval decisions.



\---



\## joins\_practice.sql



\### Objective



Combine information across multiple tables.



\### Skills Practised



\- INNER JOIN

\- LEFT JOIN

\- Multi-table JOINs



\---



\## aggregates\_report.sql



\### Objective



Generate summary reports.



\### Skills Practised



\- COUNT()

\- SUM()

\- AVG()

\- GROUP BY

\- HAVING



\---





