# Week 5 Day 3: Route 53 and Edge Services

This was the point where DNS started to feel like a real part of the architecture rather than a background detail. Route 53 is not just for mapping names to IPs. It also helps control traffic flow, support resilience, and shape how users reach services across regions.

## Route 53 record choices

| Scenario | Record type / policy | Reason |
|---|---|---|
| Point the root domain to an ALB | Alias A record | Works at the zone apex and is free and auto-updating |
| Point a subdomain to an ALB | CNAME | Works well for subdomains |
| Split traffic for a canary rollout | Weighted routing | Allows percentage-based distribution |
| Route to a backup site if the primary fails | Failover routing | Uses health checks to switch traffic automatically |
| Send users to the lowest-latency region | Latency routing | Uses network performance rather than geography alone |
| Route based on country | Geolocation routing | Useful for regulatory or regional access rules |

## Health checks

Route 53 health checks are important for failover patterns. If the primary target becomes unhealthy, Route 53 can direct traffic to the secondary target. That only works properly when the health check is configured and the TTL is low enough for the change to take effect quickly.

## CloudFront vs Global Accelerator

| Service | Best for | Key distinction |
|---|---|---|
| CloudFront | Static content, websites, and cached edge delivery | Caches content at edge locations |
| Global Accelerator | Non-HTTP applications and stable, global IP-based routing | Does not cache; accelerates traffic over the AWS backbone |

## Reflection

The most useful part of this day was understanding that DNS routing is really a business-logic layer. It is the place where availability, performance, compliance, and rollout strategy all become visible in the architecture.
