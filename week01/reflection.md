Week 1 Reflection

1) What I built this week (3–5 sentences):

I consolidated the FinTrust conceptual model and governance notes, documenting the core entities (customers, accounts, transactions) and the multi-account AWS governance pattern. I drafted region and resilience decisions that justify `af-south-1` as the primary Region and a Pilot Light DR strategy to `eu-west-1`. I captured compute, storage, and recovery design choices that will guide later weeks' implementation.

2) Key technical decisions and why (3–5 sentences):

The primary Region is `af-south-1` for POPIA compliance and proximity to users. A multi-account Organization separates management, security, production and sandbox workloads for better audit and least-privilege controls. The data model uses `customers -> accounts -> transactions` to preserve referential integrity and support analytic queries.

3) What I struggled with and how I resolved it (2–4 sentences):

My biggest challenge was organising multiple notes and examples into a single, traceable portfolio structure. I resolved this by grouping files by week and purpose, creating a simple README and diagram notes so artifacts are easier to reproduce and explain.

4) What I'd add to make this portfolio artifact stronger (1–2 bullet points):

- Add an ER diagram exported to `week01/diagrams/` and link it from the README.
- Include a small sample dataset and basic SQL queries that exercise the model.
