# Week 3 Reflection

This week I moved from small Python exercises to a repeatable data-cleaning process. The script reads inconsistent CSV data, normalises fields, writes a clean CSV and JSON summary, and records processing events through the logging module.

Structured logging and explicit validation made failures easier to trace than print statements alone. Separating reusable functions from the pipeline also made the code easier to test.

On the AWS side, I compared S3 storage classes, lifecycle rules, encryption, Object Lock, and private CloudFront origins. I also added tests for malformed CSV headers and invalid dates so unsuitable input is rejected before an output file is created.
