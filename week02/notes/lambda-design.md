# FinTrust Lambda Design Notes

The thing that stood out to me most about Lambda is how well it fits short, event-driven work. It is a strong choice for FinTrust when a task needs to happen in response to something specific rather than running all day on a server.

## Why Lambda makes sense

Serverless does not mean there are no servers. It means AWS handles the infrastructure for me. That includes provisioning, scaling, patching, and availability, while I focus on the function logic itself.

For FinTrust, that is useful because many of the workloads are triggered by events. A file arrives, a transaction is created, or a scheduled report needs to be generated. In those cases, Lambda keeps the architecture simple and avoids the cost of leaving a server running all the time.

## The Lambda lifecycle

A Lambda invocation follows a simple pattern:

1. A trigger fires
2. The function executes
3. It returns a response
4. The environment is then recycled

The two startup patterns I need to keep in mind are:

- Cold start: the environment has to be created from scratch
- Warm start: the environment already exists, so the function responds much faster

That matters for FinTrust because a real-time fraud scorer should not suffer from avoidable delay, while a monthly compliance report can tolerate a slower startup.

## Limits I need to remember

Lambda is powerful, but it has clear boundaries:

- Maximum timeout: 15 minutes
- Memory: 128 MB to 10 GB
- Temporary storage: 512 MB to 10 GB
- Default concurrent executions: 1,000 per Region

That is why Lambda is best for short tasks and not for long-running batch jobs.

## FinTrust use cases

### Fraud scorer

This is a strong Lambda use case because each new transaction can trigger a scoring step almost immediately. The function is short-lived and event-driven.

### Compliance report generator

This also fits well because the report is generated once a month. There is no reason to keep a server running for a workload that only happens occasionally.

## My takeaway

Lambda works best when the workload is lightweight, event-driven, and not constantly running. For FinTrust, it is a strong option for automation and short processing tasks where cost and simplicity matter more than long-running execution.
