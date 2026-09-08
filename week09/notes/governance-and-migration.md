# Governance and Migration Planning

## Service Catalog and tags

FinTrust uses three portfolios: DataPlatform, FinancialServices and InfraOps. A launch role provisions each approved product, while template constraints limit instance families and parameter values. The product form requires `CostCentre`, `Team` and `Environment` before launch.

Tag controls work at several levels. Service Catalog prevents missing values for catalogue products. An organisation policy standardises spelling and allowed values. An SCP can reject selected create operations when a required request tag is absent. AWS Config detects resources that were created through another route or later drifted. The Python audit also checks allowed values, which catches a resource that has all three keys but uses an invalid cost centre.

## Seven strategy classification

The [classification table](../data/migration-classification.csv) preserves the figures from the supplied scenario and adds a unique estate count. The material states 2,847 servers, while the listed counts total 2,859 if the 12 Repurchase servers are added to all other categories. The table treats those 12 as part of the published 312 systems leaving the estate, giving 300 unique Retire servers plus 12 Repurchase servers. This keeps the unique total at 2,847 without hiding the overlap. Relocate has a zero count because the scenario states that FinTrust has no VMware Cloud contract.

Migration Evaluator builds the financial case before migration. Application Discovery Service supplies dependency information for wave planning. Migration Hub then tracks execution across MGN, DMS and manual workstreams.
