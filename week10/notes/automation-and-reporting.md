# Automation and Reporting Decisions

Operational code and reporting views serve different audiences. Python checks current AWS state, applies an approved throttle and resumes a migration task. SQL views assemble repeatable business measures from the migration database. QuickSight uses those views when programme leaders need filters, trends and drill down.

The orchestrator performs one short action per invocation. EventBridge starts classification, returns later to check the cutover gate, and then checks the final DataSync execution until it reaches a terminal state. This avoids sleeping inside Lambda for five minutes at a time and makes each transition visible in logs.

The next task I would automate is the DMS validation gate. It is repetitive, time sensitive and easy to record consistently. The automation would read every table statistic, block approval if failed rows increase and write the evidence to S3. A human would still approve cutover because data validation is only one part of application readiness.

## Estimated time saved

The estimate assumes five DMS checks per weekday at ten minutes each, two DataSync checks per day at fifteen minutes each, two hours of weekly portfolio reconciliation and one and a half hours of reporting. That totals 11 hours per week. Across a 14 week migration it is 154 hours. If the package takes 40 hours to build and test, the estimated net saving is 114 engineering hours, before reuse in later waves. These are planning assumptions, not measured production results.
