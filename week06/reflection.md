# Week 6 Reflection

Window functions were most useful when I needed the original transaction row and a comparison value at the same time. A grouped query alone would remove that row detail, while `LAG`, `DENSE_RANK`, and a running `SUM` kept the analysis readable.

The boto3 client interface was the right choice for the S3 and IAM audits because it exposes the service APIs directly and supports operations that do not have an equivalent resource interface. The scripts also reinforced why pagination and exception handling are necessary. A script that reads only the first response page can produce a report that looks complete while silently omitting resources.

The strongest review point was to keep constants such as bucket names, restricted ports, and KMS key identifiers outside the audit logic. I applied that by using named constants, command-line arguments, and environment variables. In Week 7 I will keep the AWS call, transformation logic, and report output separated so each part is easier to test.

For a Monday morning security audit, EventBridge Scheduler can invoke a Lambda function that runs the checks and stores the report in S3. A second option is an EventBridge schedule that submits an ECS Fargate task for a larger audit. Lambda is the simpler and more resilient choice while the work remains below its runtime limit because AWS manages availability, retries, and scaling. Fargate becomes the better option if the audit grows beyond Lambda limits or needs a container with additional tools.
