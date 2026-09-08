# Migration Strategy Decisions

The Week 10 material describes two related but different scopes. The six strategy business portfolio contains 285 applications. The migration execution programme contains 2,847 discovered servers. Application decisions are recorded in [application-portfolio.csv](../data/application-portfolio.csv); server counts remain part of the Week 9 estate plan. Keeping these scopes separate prevents application counts from being presented as server counts.

| Strategy | Selection test | FinTrust use |
| --- | --- | --- |
| Retire | The capability is no longer required | Superseded reporting tools |
| Retain | A real constraint prevents this wave | SWIFT and mainframe dependencies |
| Repurchase | A suitable subscription replaces the application | HR and procurement |
| Rehost | Speed and no code change are the priority | Stable internal middleware |
| Replatform | A managed service fits without redesign | RDS and managed application runtimes |
| Refactor | The business need requires a new architecture | Fraud and onboarding services |

Migration Evaluator supports the cost case. The readiness assessment covers business, people, governance, platform, security and operations. Application Discovery Service maps technical dependencies, and Migration Hub reports execution progress. MGN performs the server replication; Migration Hub does not move workloads.
