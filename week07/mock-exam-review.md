# Week 7 Mock Exam Review

| Question | Answer | Reason |
| ---: | :---: | --- |
| 1 | B | SQS FIFO preserves payment order and retains messages while the consumer is unavailable. |
| 2 | C | SWF remains appropriate when an external human worker polls AWS for an activity task. |
| 3 | C | A Lambda Authorizer can validate OAuth tokens from the partner's identity provider. |
| 4 | B | AppSync combines several data sources in one GraphQL query and supplies subscriptions. |
| 5 | C | Provisioned Concurrency keeps execution environments ready and reduces cold-start latency. |
| 6 | A | An S3 notification invokes Lambda asynchronously, so failure handling belongs on the function. |
| 7 | C | A VPC Lambda in a private subnet needs a NAT route to call a public HTTPS endpoint. |
| 8 | C | `DeletionPolicy: Retain` keeps the Aurora resource after stack deletion. |
| 9 | C | The Strangler Fig pattern moves one capability at a time while the monolith continues serving other paths. |
| 10 | D | Near-zero RPO and sub-minute RTO require Multi-Site Active-Active. |

The two distinctions most likely to cause mistakes are failure handling for asynchronous Lambda versus SQS event source mapping, and Pilot Light versus Warm Standby. Both are covered in the Week 7 notes and local tests.
