# Week 7: Messaging, APIs, Lambda, and Infrastructure as Code

Week 7 extends FinTrust with an event-driven payment path, production API decisions, Lambda handlers, CloudFormation, microservice migration, and disaster recovery choices.

## Architecture

- [Week 7 architecture diagram pack](diagrams/week07_architecture_diagrams.pdf)

## Application code

- [Flask transaction API](api/flask_app.py)
- [FastAPI transaction API](api/fastapi_app.py)
- [SQS FIFO publisher](messaging/payment_publisher.py)
- [Lambda event explorer](lambda/event_explorer.py)
- [API Gateway transaction handler](lambda/transaction_handler.py)
- [SQS fraud scorer](lambda/fraud_scorer.py)
- [Local test suite](tests/test_week07.py)

The Flask and FastAPI services implement health, create, list, retrieve, and status-update routes. Both add an `X-Request-ID` response header. The Flask application can publish accepted transactions to SQS when `PAYMENT_QUEUE_URL` is configured.

| Method and route | Purpose |
| --- | --- |
| `GET /health` | Confirm that the API process is ready |
| `POST /transactions` | Validate and create a pending transaction |
| `GET /transactions` | List transactions, optionally filtered by `account_id` |
| `GET /transactions/{id}` | Retrieve one transaction or return 404 |
| `PATCH /transactions/{id}/status` | Approve or reject an existing transaction |

## Implementation rationale

| Component | Reason for the choice |
| --- | --- |
| SQS FIFO publisher | Preserves transaction order within each account and supplies a durable hand-off |
| Fraud scorer Lambda | Scales with queue demand and reports individual failed records for safe retries |
| SNS alert topic | Separates fraud scoring from compliance notification subscribers |
| Step Functions Standard | Records every wire-transfer step and coordinates compensating actions |
| CloudFormation | Makes the queue, permissions, Lambda, and protection rules repeatable and reviewable |

## Infrastructure code

- [Event-driven pipeline template](infrastructure/event_pipeline.yaml)
- [Protected Aurora example](infrastructure/protected_aurora.yaml)
- [Wire transfer Saga](infrastructure/wire_transfer.asl.json)

The event template creates an encrypted FIFO queue, FIFO dead-letter queue, encrypted SNS topic, least-privilege Lambda role, scorer function, and event source mapping. The Aurora template is an example for Change Set review and incurs database charges if deployed.

## Design notes

- [Messaging and workflows](notes/messaging-and-workflows.md)
- [API decisions](notes/api-design.md)
- [Lambda deep dive](notes/lambda-deep-dive.md)
- [Infrastructure, microservices, and recovery](notes/infrastructure-and-dr.md)
- [Week 8 preparation](notes/week08-preparation.md)

## Review

- [Mock exam review](mock-exam-review.md)
- [Self-assessment](self-assessment.md)
- [Week 7 reflection](reflection.md)
- [Portfolio evidence checklist](evidence/portfolio-checklist.md)
- [Validation record](evidence/validation.md)

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r week07\requirements.txt
.\.venv\Scripts\python.exe -m week07.api.flask_app
```

Run FastAPI in a second terminal with:

```powershell
.\.venv\Scripts\python.exe -m uvicorn week07.api.fastapi_app:app --port 8000
```

Run all local checks with:

```powershell
.\.venv\Scripts\python.exe -m unittest week07.tests.test_week07 -v
```

AWS credentials are obtained through the normal boto3 credential chain. No access key is stored in this repository.
