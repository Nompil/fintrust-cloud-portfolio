# Monitoring and Infrastructure as Code

CloudWatch answers whether the workload is performing now. CloudTrail answers who made an API call. Config answers whether a resource is compliant with the required configuration. The distinction matters when investigating a public S3 bucket: Config identifies the non-compliant state, while CloudTrail identifies who changed it.

The included CloudFormation template is deliberately small. It schedules the cost-report Lambda for the first Monday of each month at 08:00 SAST, represented as 06:00 UTC in EventBridge. It grants only EventBridge invocation permission for the supplied Lambda ARN. Deploying it still requires a reviewed change set and an authorised account.

Change sets preview the effect of a CloudFormation update. Drift detection identifies a difference between a template and a resource changed outside CloudFormation, but it does not repair that difference. A team must either update the template to match an approved manual change or restore the resource to the template's intended state.

Control Tower is appropriate when a team needs an opinionated landing zone, account vending and baseline guardrails. Preventive guardrails use SCPs. Detective guardrails use Config rules. Proactive guardrails use CloudFormation Hooks before a resource is created.
