# API Design Decisions

## API inventory

| Consumer | API | Authorization | Reason |
| --- | --- | --- | --- |
| Retail mobile customers | API Gateway REST API | Cognito User Pool | Customer JWT validation plus production features such as WAF, caching, and canary releases |
| Internal Lambda and ECS services | API Gateway HTTP API | IAM with SigV4 | Lower cost for simple service calls that do not need usage plans or response caching |
| FCA regulatory system | API Gateway REST API | Lambda Authorizer | The caller supplies an OAuth token from an external identity provider |
| Mobile portfolio screen | AppSync | Cognito | One GraphQL query combines balance, transactions, and FX data with balance subscriptions |
| Institutional trade feed | API Gateway WebSocket API | IAM | The protocol needs persistent two-way messages and is not GraphQL |

## Production controls

The production REST stage has a 1,000 request per second burst limit and a 500 request per second sustained limit. The payment POST method is limited further to protect the downstream processor. New releases first reach the staging stage, then a 10 percent production canary. CloudWatch error and latency metrics determine promotion or rollback.

Lambda Authorizer results for the FCA integration are cached for 300 seconds. The cache period is short enough for token expiry while avoiding an authorizer invocation on every request. API keys identify clients for usage plans but are not an authentication mechanism.

## Flask and FastAPI decision

Flask is useful for a small internal prototype where a simple routing model makes the request flow easy to inspect. FastAPI is the better choice for the transaction contract because Pydantic validates amounts, currency codes, and status values before business logic runs, while OpenAPI documentation gives the consumer team a current interface description.

Both implementations provide health, create, list, retrieve, and status-update endpoints. They also return an `X-Request-ID` header for tracing. The API examples use in-memory data only for the exercise; production persistence belongs in a database and the create request publishes to SQS through a separate adapter.
