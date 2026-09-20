# Week 12 Reflection

The useful change in my cost thinking was separating a pricing commitment from a workload decision. A Savings Plan is not automatically the answer just because it has a discount. First I need to know whether the workload is stable, whether the instance family might change, and whether Lambda or Fargate needs to be covered. Spot remains the better option for a checkpointed batch process that can restart, while a payment workload with a strict availability target has different priorities.

The access-denied scenarios reinforced that an AdministratorAccess policy is not the end of evaluation. I would now check for an explicit deny first, then the effective SCP, permission boundary, resource policy and identity policy. That order saves time because the policy simulator alone cannot reveal an organisation SCP.

The SQL tuning exercise also made the order of work clearer. The index should follow an observed plan and a real access pattern. Adding an index before checking `EXPLAIN ANALYZE` can make writes more expensive without improving the query that matters. The practical next step is to capture the before and after plan from the supplied database rather than assuming the index is useful.
