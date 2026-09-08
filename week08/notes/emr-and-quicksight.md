# EMR and QuickSight Decisions

## Monthly feature engineering

The `fintrust-fraud-emr` cluster starts on the first Monday of each month at 01:00. One `m5.xlarge` Primary node and three `r5.2xlarge` Core nodes use On-Demand capacity because they coordinate the job and hold HDFS data. Four `r5.xlarge` Task nodes use a Spot Instance Fleet with `r4.xlarge` as an alternative. Task nodes add compute but do not hold HDFS data, so losing one slows the job rather than losing the dataset.

The Spark step reads transaction Parquet from `s3://fintrust-processed/parquet/transactions/`, calculates 28 fraud features and writes the result to `s3://fintrust-curated/features/year=/month=/`. The cluster terminates after the step finishes. This fits a monthly workload better than paying for a permanent analytics cluster.

## Reporting layer

FinTrust uses QuickSight Enterprise for 12 executive and senior analyst users. Four datasets support Transaction Volume, Fraud Rate by Region, FX Exposure and Compliance Status dashboards. Their SPICE refresh begins at 03:00 after the daily Glue work completes. Row-level security limits provincial and product views, while direct Athena queries remain available for analysts who need current or unusual slices of the data.

SPICE keeps the regular dashboards responsive without running an Athena query for every viewer. The team must still monitor its purchased capacity and refresh failures because SPICE capacity does not grow automatically.
