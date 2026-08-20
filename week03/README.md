# Week 3: S3 and Python Automation

Week 3 combines Amazon S3 design decisions with reusable Python modules, filesystem automation, CSV cleaning, JSON reporting, exception handling, and logging.

## AWS deliverables

- [S3 storage design](storage-design.md)
- [Storage security](storage-security.md)
- [CloudFront architecture](cloudfront-architecture.md)
- [Week 3 architecture diagrams PDF](diagrams/week03_architecture_diagrams.pdf)

## Python deliverables

- `python/fintrust_utils.py`: formatting, validation, calculation, and reporting helpers
- `python/test_utils.py`: checks for the reusable helper functions
- `python/setup_data_dirs.py`: creates a portable data directory structure
- `python/clean_transactions_v2.py`: validates and cleans CSV data, writes a JSON summary, and logs processing events
- `python/data/`: small input and output samples used by the cleaning pipeline

## Run the examples

The Week 3 scripts use only the Python standard library.

```powershell
python week03\python\test_utils.py
python week03\python\clean_transactions_v2.py
python week03\python\setup_data_dirs.py .\week03\python\demo-data
```

The generated log file and demo directory are local runtime artifacts and are not committed.
