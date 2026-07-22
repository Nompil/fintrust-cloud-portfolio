\# Week 3 - Python Automation and Standard Library



\## Objective



The objective of Week 3 was to move beyond basic Python scripting and begin building reusable, maintainable and configurable tools using Python.



Throughout the week I learned how to organise code into modules, work with the Python Standard Library, interact with files and directories, and process structured data such as CSV and JSON files.



These skills form the foundation for future AWS automation using boto3, Lambda and S3.



\---



\# Day 1 - Functions and Modules



\## Concepts Learned



Functions allow code to be written once and reused multiple times.



Benefits include:



\- Reduced duplication

\- Better organisation

\- Easier testing

\- Improved maintenance



Topics covered:



\- Function creation

\- Parameters

\- Return values

\- Function reuse

\- Code modularisation



\---



\## Modules



Modules allow related functions to be grouped together into reusable files.



Benefits:



\- Better code organisation

\- Improved reusability

\- Easier maintenance

\- Separation of concerns



\---



\## Portfolio Deliverables



\### fintrust\_utils.py



Reusable utility functions including:



\- Currency formatting

\- Account validation

\- Transaction summaries

\- Basic reporting helpers



\### test\_utils.py



Script used to test and validate utility functions.



\---



\## Business Value



Reusable modules reduce duplicated code and simplify maintenance of larger applications.



This approach is commonly used in production systems where many applications share common functionality.



\---



\# Day 2 - Python Standard Library



\## pathlib



Used for working with files and directories.



Concepts learned:



\- Path objects

\- Directory creation

\- File existence checks

\- Recursive searching

\- Platform-independent paths



Example:



```python

from pathlib import Path



data\_dir = Path("data") / "transactions"

```



\---



\## os



Used for interacting with the operating system.



Concepts learned:



\- Environment variables

\- File system interactions

\- Configuration management



Example:



```python

import os



region = os.environ.get("AWS\_DEFAULT\_REGION")

```



\---



\## sys



Used for interacting with the Python interpreter.



Concepts learned:



\- Command-line arguments

\- Exit codes

\- Error reporting



Example:



```python

import sys



print(sys.argv)

```



\---



\## Portfolio Deliverables



\### setup\_data\_dirs.py



Creates a standard FinTrust data directory structure.



Capabilities:



\- Creates required folders

\- Supports command-line arguments

\- Supports environment variables

\- Generates a directory report



\---



\## Business Value



Creates a repeatable directory structure that can be deployed consistently across environments.



\---



\# Day 3 - File I/O and Data Processing



\## Concepts Learned



This day introduced working with external data files.



Topics covered:



\- Reading text files

\- Writing text files

\- CSV processing

\- JSON processing

\- Data cleaning

\- Data transformation

\- Context managers

\- UTF-8 encoding



\---



\## File I/O



Python files are typically accessed using the `open()` function together with a context manager.



Example:



```python

with open("report.txt", "r", encoding="utf-8") as f:

&#x20;   data = f.read()

```



Benefits:



\- Automatically closes files

\- Prevents resource leaks

\- Produces cleaner code



\---



\## CSV Processing



The csv module provides reliable handling of structured tabular data.



\### DictReader



Reads CSV rows into dictionaries.



Example:



```python

reader = csv.DictReader(file)

```



\### DictWriter



Writes dictionaries back to CSV files.



Example:



```python

writer = csv.DictWriter(file, fieldnames=headers)

```



Benefits:



\- Easy access to columns

\- More readable code

\- Reduces indexing mistakes



\---



\## JSON Processing



JSON is one of the most common formats used in cloud environments.



Topics covered:



\- json.load()

\- json.dump()

\- json.loads()

\- json.dumps()



Example:



```python

with open("summary.json", "w") as f:

&#x20;   json.dump(data, f, indent=2)

```



\---



\## Portfolio Deliverables



\### clean\_transactions.py



Reads raw transaction data, cleans and standardises records, then outputs:



\- clean\_transactions.csv

\- daily\_summary.json



\---



\### raw\_transactions.csv



Contains intentionally inconsistent transaction data used for testing and cleaning.



Issues handled:



\- Mixed case transaction types

\- Inconsistent date formats

\- Extra whitespace

\- Missing descriptions

\- Inconsistent formatting



\---



\### clean\_transactions.csv



Contains standardised transaction records.



Transformations include:



\- Normalised dates

\- Consistent transaction types

\- Trimmed values

\- Default descriptions where missing



\---



\### daily\_summary.json



Automatically generated summary report containing:



\- Total transactions

\- Deposit count

\- Withdrawal count

\- Total deposit value

\- Total withdrawal value



\---



\## Business Value



This exercise simulates a lightweight ETL process.



ETL stands for:



\- Extract

\- Transform

\- Load



This is a common requirement in banking, analytics and cloud data platforms.



\---



\## AWS Connection



The concepts learned this week connect directly to AWS services.



\### Amazon S3



Files processed locally today could later be stored in S3 buckets.



\### AWS Lambda



The cleaning script could be executed automatically when a new file is uploaded.



\### boto3



Future scripts will use boto3 to interact with AWS resources directly.



\### Amazon EventBridge



Could be used to trigger scheduled processing pipelines.



\---



\## Key Skills Developed



By the end of Week 3 I was able to:



\- Create reusable functions

\- Build Python modules

\- Organise application code

\- Create directory structures

\- Read environment variables

\- Use command-line arguments

\- Process CSV files

\- Process JSON files

\- Clean raw data

\- Generate structured reports



\---



\## Reflection



Week 3 helped me move from writing simple Python exercises to building practical tools.



The biggest lesson was understanding that real-world data is rarely clean and often requires transformation before it can be used effectively.



I also learned that many cloud workflows involve reading, processing and generating files, making these skills directly relevant to future AWS projects.



I can clearly see how the concepts covered this week will eventually connect to Amazon S3, AWS Lambda and automated data processing pipelines within the FinTrust project.



\### What I Found Interesting



One of the biggest observations during this exercise was that raw data is rarely perfect.



The transaction file contained inconsistent date formats, different transaction type formats, missing descriptions and unnecessary spaces.



This demonstrated why data cleaning is an important part of any reporting or analytics process before meaningful insights can be produced.

