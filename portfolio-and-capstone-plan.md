# FinTrust Portfolio and Capstone Plan

## Why this document exists

This is a plain-language record of the work completed during Weeks 1 to 12 and the practical work needed for the FinTrust capstone. It is based on the portfolio repository and the capstone, VPC, and assessment documents supplied in Week 12.

It is important to separate two things:

1. Work that is present in the repository, such as code, SQL, diagrams, design notes, tests, and reflections.
2. Work that must be demonstrated from a real AWS account, such as deployed services, Console screenshots, API responses, CloudWatch logs, and a live demo.

The repository documents the first category well. A document or script is not proof that a resource is running in AWS, so the Console evidence listed below still needs to be collected unless it already exists in the learner's AWS account.

## Where the portfolio stands

| Weeks | Main work recorded in the repository | How it supports the capstone |
| --- | --- | --- |
| 1 and 2 | AWS foundations, IAM, EC2, resilience, SQL queries, joins, aggregates, and Python basics | Supports least-privilege roles, SQL reporting, and clean Git practice |
| 3 | S3 design, bucket security, lifecycle choices, CSV and JSON processing, error handling | Provides the raw, processed, quarantine, and report storage patterns |
| 4 | Relational modelling, RDS, DynamoDB, database choices, Python packaging, and ETL work | Supports the ledger schema, event store, and Python package structure |
| 5 | Multi-AZ networking, route tables, security groups, Route 53, and CloudFront | Supports private RDS placement and controlled Lambda-to-database access |
| 6 | IAM boundaries, CloudTrail, CloudWatch, Config, incident response, and SQL analytics | Supports governance, monitoring, logging, and security decisions |
| 7 | SQS, SNS, EventBridge, Lambda, API design, and CloudFormation | Supports the event-driven transaction path, alerts, API, and monthly report schedule |
| 8 | S3 data lake, Athena, Glue, Kinesis, analytics, and machine-learning service choices | Supports analytics outputs and explains wider data-platform decisions |
| 9 | Cost management, tagging, migration planning, DMS, and recovery planning | Supports Free Tier decisions, the migration section, and cost controls |
| 10 | Migration package, DMS and DataSync helpers, migration SQL views, and transfer planning | Supports the legacy data migration strategy |
| 11 | Well-Architected review, CTEs, window functions, retry handling, and concurrent S3 work | Supports the design review, SQL reporting, and reliable Python patterns |
| 12 | Cost Explorer reporting, Organizations and SCPs, CloudFormation scheduling, and SQL tuning | Supports governance, automated reporting, and the final portfolio audit |

The repository already contains a README for each week, supporting notes, code or SQL where taught, and PDF architecture diagrams. It is a useful base for the capstone, but the capstone is a new integrated system rather than a copy of the weekly folders.

## The capstone in simple terms

The capstone is a **Cloud-Based Transaction Insights and Risk Monitoring System** for FinTrust Bank SA. A CSV transaction file is uploaded, each row is checked and risk scored, the data is stored, high-risk activity can trigger an alert, and the compliance team can use an API and monthly reports to review it.

The system is expected to work end to end and stay within the AWS Free Tier. It starts in Week 13, should be functionally ready by the end of Week 14, and is demonstrated live in Week 16.

### Required transaction flow

```text
CSV upload to S3
        |
        v
Ingest Lambda validates the rows
        |
        +--> RDS PostgreSQL transaction ledger
        |
        +--> DynamoDB event and risk-score store
        |
        v
SQS FIFO queue
        |
        v
Score Lambda
        |
        +--> Alert Lambda --> SES email for high-risk activity

API Gateway --> Query Lambda --> RDS and DynamoDB

EventBridge monthly schedule --> Report Lambda --> CSV and JSON reports in S3
```

## AWS services to use for the capstone

These are the services named in the capstone brief. The first group is the working system. The second group supports security, configuration, or visibility.

| Service | What FinTrust will use it for | What needs to be shown |
| --- | --- | --- |
| Amazon S3 | Raw CSV uploads, processed output, quarantine records, and monthly reports | Buckets, encryption, lifecycle rules, an uploaded test file, and a generated report |
| AWS Lambda | Ingest, score, alert, query, and monthly report functions | Five functions, correct triggers, logs, and a successful test run |
| Amazon SQS FIFO and DLQ | Ordered transaction processing by account and failed-message handling | FIFO queue, dead-letter queue, and Lambda event-source mapping |
| Amazon RDS for PostgreSQL | Normalised transaction ledger | Private instance status, schema loaded, and a controlled connection from Lambda |
| Amazon DynamoDB | Risk scores, session tokens, and transaction event log | Table with `account_id` partition key and `tx_timestamp` sort key, plus test items |
| Amazon API Gateway | Secure REST endpoints for compliance and fraud teams | Deployed stage, API key or usage plan, and working GET and POST responses |
| Amazon SES | High-risk transaction email alerts | Verified sandbox recipient and evidence of a safe test alert |
| Amazon EventBridge | Monthly report schedule | Rule that invokes the report Lambda and a recorded test invocation |
| Amazon CloudWatch | Logs, custom metrics, alarms, dashboard, and Logs Insights queries | Dashboard, alarms, structured log output, and an Insights query |
| AWS IAM | Separate least-privilege execution role for each Lambda function | Role matrix, policies scoped to real resources, no broad wildcard permissions |
| Amazon VPC | Private database subnets and Lambda-to-RDS security-group access | VPC, private database placement, and security-group rules proving RDS is not public |
| AWS Systems Manager Parameter Store | Runtime configuration values used by `config.py` | Parameters stored safely and read by the appropriate Lambda role |
| AWS KMS | Encryption for the S3 buckets specified in the build plan | Encryption setting and the policy or key choice used |
| AWS X-Ray | Trace requests while testing the API and Lambda path | Tracing enabled and one trace visible during a test |

### Governance services to apply where they are available

The programme also covered AWS Organizations, Control Tower, SCPs, CloudTrail, AWS Config, and Cost Explorer. They strengthen the written governance design and can be used if the learner's account or organisation permits it. They are not a reason to create unnecessary paid resources.

Use Cost Explorer and AWS Budgets to monitor spending. Use CloudTrail for audit history and AWS Config for configuration compliance if they are already available in the account. Document the intended Organization, Control Tower, and SCP controls in the governance section if a personal Free Tier account cannot create the organisational structure.

## Important VPC decision: do not copy the paid NAT Gateway lab into the capstone

The Week 5 VPC lab used six subnets and two NAT Gateways to demonstrate a production high-availability design. That is valid for the lab architecture.

The capstone brief explicitly excludes NAT Gateways because they incur charges outside the Free Tier. For the capstone, use the VPC only for the private RDS subnets and the security group that allows the relevant Lambda functions to connect to PostgreSQL on port 5432. Do not create the two NAT Gateways for this build.

This is not a shortcut. It is the stated cost constraint in the capstone architecture. The VPC lab can still remain in the portfolio as design evidence and learning evidence.

## AWS Console work still to do

The table below is the practical build sequence. It is ordered so that each later step has the services it depends on. Mark an item complete only after the resource exists in the correct Region and its evidence has been saved.

### 1. Account safety and naming

1. Confirm the target AWS Region and use it consistently. The weekly FinTrust VPC work uses `af-south-1`; confirm this is available for every service before building.
2. Check the billing alarm and create a budget if one is not already active. Keep the alert threshold at the programme's R200 safety level.
3. Choose one consistent name prefix, for example `fintrust-`. Do not use personal names in resource names, screenshots, or documentation.
4. Create a simple tag set such as `Project=FinTrust`, `Environment=dev`, and `Owner=Nompilo`. Do not add a tag that exposes personal contact details.

### 2. Foundation and access

1. Create the IAM roles for `ingest`, `score`, `alert`, `query`, and `report` Lambda functions.
2. Give every role only the resources and actions it needs. For example, the report role writes only to the report bucket; it does not need access to the quarantine bucket.
3. Store non-secret configuration in Parameter Store. Keep database credentials out of source control and out of screenshots.
4. Create the S3 buckets for raw input, processed output, quarantine records, and reports. Enable the required encryption and block public access.

### 3. Network and databases

1. Create the capstone VPC and two private database subnets across two Availability Zones.
2. Create a database security group that allows PostgreSQL port 5432 from the approved Lambda security group only. Do not make the database publicly accessible.
3. Create the RDS PostgreSQL instance within Free Tier limits. Stop it whenever the team is not actively using it.
4. Create the DynamoDB table with `account_id` as the partition key and `tx_timestamp` as the sort key.
5. Run the capstone schema and seed data against the RDS instance only after they have been reviewed locally.

### 4. Event path and API

1. Create the SQS FIFO queue and a dead-letter queue. Configure the ingest and scoring hand-off as designed.
2. Deploy the ingest, score, alert, query, and report Lambda functions. Configure the S3 trigger for ingest and the SQS trigger for score.
3. Configure SES in sandbox mode and verify only the addresses needed for safe test alerts.
4. Create API Gateway endpoints for `GET /transactions`, `GET /insights`, `POST /upload`, `POST /flag`, and `POST /resolve`. Protect them with the required API key and usage plan.
5. Create the EventBridge monthly rule for the report Lambda and test it manually before relying on the schedule.

### 5. Monitoring, tests, and final proof

1. Add CloudWatch custom metrics for ingestion errors and high-risk transaction counts. Create alarms and a small dashboard.
2. Enable X-Ray tracing for the Lambda and API testing path.
3. Upload a non-sensitive sample CSV. Confirm the full path: S3 upload, validation, RDS and DynamoDB records, queue processing, risk score, alert where appropriate, and report output.
4. Run the API tests using Postman or curl. Capture only the responses required as evidence and remove account IDs or personal data where necessary.
5. Open CloudWatch Logs Insights and save evidence of structured JSON logs from at least one Lambda invocation.

## What still needs to be built in the repository

The weekly work is organised by week. The capstone needs one clean package for the integrated application. The required deliverables are listed below.

| Area | Deliverable | Status at the start of Week 13 |
| --- | --- | --- |
| Architecture | A PDF architecture diagram showing services, data flows, and security boundaries | New capstone deliverable |
| Data model | A 3NF ERD with attributes, primary keys, and foreign keys | New capstone deliverable |
| SQL | `schema.sql`, `seed.sql` with at least 200 transactions, `risk_report.sql`, `monthly_summary.sql`, `views.sql`, and a PostgreSQL stored procedure or function | New capstone deliverable |
| Python | A `fintrust` package with `config`, `db`, `dynamo`, `models`, `validators`, `ingest`, `score`, `alert`, `query`, and `report` modules | New capstone deliverable |
| Testing | `pytest` tests with `moto`, reusable fixtures, and an end-to-end verification script | New capstone deliverable |
| Continuous integration | GitHub Actions workflow: unit tests on every push and integration tests only on the `develop` branch | New capstone deliverable |
| API design | Routes, methods, request format, response format, and authentication approach | New capstone deliverable |
| Security | IAM role matrix and security plan | New capstone deliverable |
| Data governance | One-page POPIA and lifecycle statement, migration choice, data-quality framework, and a three-item risk register | New capstone deliverable |
| Evidence | Console screenshots, API output, GitHub Actions pass, and CloudWatch Logs Insights output | Requires real AWS and GitHub evidence |

The capstone package should reuse lessons and patterns from earlier weeks, but it should not copy old demo scripts into the new package without checking that they match the capstone design.

## SQL and Python quality checklist

Before deploying, confirm the following requirements from the brief:

- The schema has tables for accounts, transactions, risk events, and alerts, with primary keys, foreign keys, indexes on account ID and transaction date, and appropriate `NOT NULL` rules.
- Seed data contains at least 200 realistic transactions across several accounts and a three-month period.
- The risk report uses a CTE to find accounts with more than three high-risk transactions in a rolling 30-day window.
- The monthly summary uses a running balance with `SUM() OVER (PARTITION BY account_id ORDER BY tx_date ROWS UNBOUNDED PRECEDING)`.
- The PostgreSQL function updates the account state and creates the risk event atomically.
- Boto3 clients are created outside Lambda handlers for connection reuse.
- Database exception handling rolls back before returning an error.
- API data is serialised safely for `Decimal` and date-time values.
- Tests use safe mocked AWS resources. No test should require real credentials or create live billable resources.

## Evidence to collect for the portfolio and the live presentation

The capstone brief specifically asks for the following evidence. Save it in an `evidence` folder with clear names and no sensitive information.

| Evidence | What a good capture shows |
| --- | --- |
| API Gateway | The deployed stage and the protected routes |
| Lambda | The list of five functions and the relevant trigger configuration |
| CloudWatch | Dashboard, alarms, and structured JSON log output from a real invocation |
| RDS | Instance status and proof that it is not publicly accessible |
| API test | Successful `GET /transactions` and `POST /upload` responses |
| CI | A green GitHub Actions run for the test suite |
| End-to-end run | One sample file moving from upload to stored data, risk result, and report or alert |

For every screenshot, hide account numbers, email addresses, access keys, database passwords, and any real personal information. Use only safe sample transaction data.

## Suggested build schedule

### Week 13

| Day | Main result |
| --- | --- |
| Day 1 | Capstone folder structure, architecture diagram, API design, Parameter Store configuration, and Lambda roles |
| Day 2 | RDS schema, seed data, DynamoDB table, database and DynamoDB helpers, and unit tests |
| Day 3 | Encrypted S3 buckets, least-privilege policies, S3 trigger, and dead-letter queue |
| Day 4 | Ingest Lambda with validation, storage writes, risk pre-score, and structured logging |
| Day 5 | Read API with paginated and filtered transactions plus risk insights |

### Week 14

| Day | Main result |
| --- | --- |
| Day 1 | Write endpoints, SQS FIFO processing, high-risk alerts, and SES testing |
| Day 2 | CloudWatch metrics, alarms, Logs Insights queries, dashboard, and X-Ray tracing |
| Day 3 | Full tests, reusable `moto` fixtures, GitHub Actions, and end-to-end script |
| Day 4 | Final SQL analytics, monthly report Lambda, and EventBridge schedule |
| Day 5 | Full demo rehearsal, Well-Architected self-assessment, evidence check, and repository review |

## What the assessment will look for

The build is worth 70 points before the live presentation. The strongest preparation is to make each of these visible in the repository and in the AWS account:

| Assessment area | Points | Best preparation |
| --- | --- | --- |
| Cloud architecture and AWS implementation | 20 | A deployed end-to-end system, deliberate least-privilege roles, and a clear architecture diagram |
| SQL and data modelling | 15 | Working 3NF ERD, runnable schema and seed data, all required analytical SQL artefacts |
| Python development and code quality | 15 | Complete ten-module package using the taught error handling and connection-reuse patterns |
| Testing and CI/CD | 10 | Meaningful tests, passing GitHub Actions, and an end-to-end check |
| Data governance and compliance | 10 | Specific POPIA classification, retention lifecycle, migration approach, and named controls in the risk register |
| Documentation and portfolio completeness | 10 | Clear README, instructions, diagrams, evidence, and an organised repository |
| Live demo and technical panel | 10 | A rehearsed upload-to-alert journey and answers based on this exact architecture |
| Business and stakeholder presentation | 10 | A simple explanation of fraud risk, compliance value, controls, cost, and resilience |

## Final working rule

Do not claim that a service has been deployed, a lab has been completed, or a test has passed in AWS until there is real evidence for it. The portfolio can honestly show the design and prepared code now. The Console build, evidence collection, testing, and live rehearsal are the work that turns it into a complete capstone.
