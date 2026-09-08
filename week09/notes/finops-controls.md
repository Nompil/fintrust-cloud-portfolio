# FinOps Controls

## Different jobs for different tools

Cost Explorer answers questions about previous spend and forecasts. AWS Budgets watches actual or forecast spend against a limit and sends notifications. The Cost and Usage Report provides resource level billing rows for chargeback and long term analysis. Compute Optimizer uses workload metrics to recommend a better resource size.

## FinTrust reporting path

The Cost and Usage Report lands in `fintrust-cur-data` as hourly Parquet. A Glue crawler updates the Data Catalog and the `fintrust-finops-queries` Athena workgroup runs the chargeback query. QuickSight imports the result to SPICE each day. The report groups by linked account, service, billing month and the activated `CostCentre` tag.

The eight business unit budgets use actual and forecast thresholds. An 80 percent notification goes to the account owner, 90 percent adds finance, and 100 percent starts an approval workflow. A restrictive SCP must not be applied automatically to production simply because a forecast is wrong. Finance Controller approval and a documented exception path are required.

## Right sizing

Compute Optimizer should be enabled at organisation level. EC2 memory recommendations require CloudWatch Agent metrics; CPU alone can make a memory bound instance look over provisioned. Recommendations are reviewed against peak periods before changing instance sizes. EBS `gp2` to `gp3` changes and Lambda memory recommendations are also tested before adoption.
