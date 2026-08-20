# Week 6 Validation Record

**Date:** 20 August 2026

## PostgreSQL

The four SQL files were executed in order against PostgreSQL 16 with `ON_ERROR_STOP` enabled.

| Check | Result |
| --- | --- |
| Practice setup | 20 customers and 240 transactions created |
| Day 1 suspicious ratio CTE | Passed and returned 20 customer summaries |
| Day 1 branch comparison CTE | Passed and returned 24 monthly branch summaries |
| Day 2 `DENSE_RANK` query | Passed and returned ranked customer spending |
| Day 2 running `SUM` query | Passed and returned 48 suspicious transactions |
| Day 2 `LAG` query | Passed and identified five April spending spikes |
| Day 5 combined risk query | Passed and returned 20 customer risk scores |

## Python

`python -m compileall -q week06` completed successfully. The local audit test suite completed five tests with no failures.

| Tested behaviour | Result |
| --- | --- |
| S3 Region, public access, and encryption checks | Passed |
| IAM access key age check | Passed |
| Open PostgreSQL port detection | Passed |
| Dated KMS encrypted report request | Passed |
| Seven day S3 activity enrichment | Passed |

## Diagram PDFs

| File | Pages | Result |
| --- | ---: | --- |
| `diagrams/week06_architecture_diagrams.pdf` | 5 | Valid PDF |
