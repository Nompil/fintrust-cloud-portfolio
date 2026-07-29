\# Week 4 - Advanced Python and AWS Networking



\## Day 1 - Custom Exception Classes



\### Concepts Learned



\- Exception hierarchy

\- Custom exception classes

\- Domain-specific errors

\- Exception inheritance

\- super().\_\_init\_\_()

\- TransactionError

\- BankingError



\### Portfolio Deliverable



\*\*transactions.py\*\*



Implemented:



\- BankingError

\- TransactionError

\- InsufficientFundsError

\- AccountFrozenError

\- InvalidAmountError

\- DailyLimitExceededError



\### Business Value



Custom exceptions provide meaningful business context when failures occur and allow banking applications to respond appropriately to different transaction failures.



\### AWS Connection



These same exception-handling patterns are commonly used in AWS Lambda functions, APIs and cloud-native applications where business errors must be treated differently from system failures.



\## Day 2 - Debugging Scenarios



\### Concepts Learned



\- Reading stack traces

\- Interpreting Python tracebacks

\- Using print debugging

\- Using breakpoint()

\- Understanding KeyError

\- Identifying logic bugs

\- Systematic troubleshooting



\### Portfolio Deliverable



\*\*debug\_me.py\*\*



Fixed five bugs in a transaction processing module:



\- Incorrect fee calculation

\- Dictionary key typo in account updates

\- Dictionary key typo in reporting

\- Incorrect total transaction calculation

\- Incorrect failed payment count



\### Business Value



Debugging skills are essential for production banking applications because not all defects cause immediate exceptions. Some bugs silently produce inaccurate financial results. Systematic debugging helps identify and resolve both runtime and logic errors.



\### AWS Connection



The same debugging techniques are used when troubleshooting Lambda functions, EC2 applications, API integrations and database transactions in AWS environments.



\## Day 3 – CSV to SQLite to Dashboard



\### Deliverables



\- transactions.csv

\- pipeline.py

\- daily\_report.txt

\- reflection.md



\### Concepts Learned



\- CSV validation

\- SQLite databases

\- Parameterized SQL queries

\- ETL pipelines

\- Idempotent data loading

\- Reporting and dashboards



\### Business Value



The pipeline simulates a nightly transaction-processing workflow where data is imported, validated, stored and reported. This pattern forms the foundation of analytics and fraud-monitoring systems.

