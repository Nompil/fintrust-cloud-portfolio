# Week 2 Reflection

This week connected workload requirements to technical choices. I used JOINs and aggregate queries to report across the FinTrust tables, then modelled transaction rules with Python functions and conditionals.

The compute exercises showed me why one AWS service does not fit every workload. I selected ECS on Fargate for continuously running, stateless application services, Lambda for short event-driven tasks, and AWS Batch for longer batch processing. The decision depends on runtime, scaling, state, and operational overhead.

Working through several transaction scenarios helped me check the decision rules and understand how small changes to their order affect the final result.
