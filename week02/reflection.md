Week 2 Reflection

1) What I built this week (3–5 sentences):

I completed SQL JOIN and aggregate exercises against the FinTrust dataset and implemented Python conditional exercises that model transaction decision logic. I mapped compute choices for FinTrust workloads (API, batch, reports) and documented shared-storage and file-system trade-offs for analytics workloads. I produced notes and small helper scripts that show how to run the SQL and Python examples locally.

2) Key technical decisions and why (3–5 sentences):

I chose containerised ECS/Fargate for stateful, long-running services (transaction API, account service) and Lambda for scheduled or short-lived tasks (compliance reports) to balance operational overhead and cost. For shared model/artifact storage I recommended EFS or FSx depending on access patterns and performance needs, and S3 for archival data.

3) What I struggled with and how I resolved it (2–4 sentences):

The hardest part was picking the single best compute option; the resolution was to match service type to workload characteristics (latency, runtime, statefulness) rather than force one pattern. I documented the tradeoffs in `notes/compute-decision-map.md` which helped crystallise the choices.

4) What I'd add to make this portfolio artifact stronger (1–2 bullet points):

- Include runnable sample Docker configuration or a minimal `docker-compose` for the API example.
- Remove or consolidate duplicate notes (e.g., `shared-storage-decision.md` duplicates) so reviewers see a single canonical file.

