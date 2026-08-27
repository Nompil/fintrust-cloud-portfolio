# Day 3: Route 53

The lab design uses a public hosted zone called `fintrust-lab.internal`. The name is suitable for a classroom exercise, although a real public application would use a registered public domain.

## Hosted zone records

| Record | Type | Target | Purpose |
| --- | --- | --- | --- |
| `app.fintrust-lab.internal` | Alias A | `fintrust-alb` | Main application entry point |
| `api.fintrust-lab.internal` | CNAME | ALB DNS name | API lab record |
| `canary.fintrust-lab.internal` | Weighted Alias A | Production ALB, weight 90 | Most traffic remains on production |
| `canary.fintrust-lab.internal` | Weighted Alias A | Canary ALB, weight 10 | A small share tests the new release |
| `test.fintrust-lab.internal` | A | Lab test address | Confirms record creation and resolution |

An Alias A record is preferred for the main application because it can point to an AWS load balancer and can be used at the zone apex. A CNAME maps one name to another name and cannot be used at the apex of a Route 53 hosted zone.

## Routing policy guide

| Policy | Best use |
| --- | --- |
| Simple | One resource with no special routing rule |
| Weighted | Controlled percentages for releases or experiments |
| Latency | Send users to the Region with the lowest measured latency |
| Failover | Active and passive disaster recovery with health checks |
| Geolocation | Route according to the user's geographic location |
| Geoproximity | Route by resource and user location, with optional traffic bias |
| Multivalue answer | Return several healthy records for simple DNS-level distribution |

## Decision exercise

| Scenario | Answer |
| --- | --- |
| Content changes according to the user's country | Geolocation |
| A release needs a controlled percentage of traffic | Weighted |
| Users should reach the Region with the lowest network latency | Latency |
| A secondary site should be used only after the primary fails | Failover |
| DNS should return several healthy endpoints | Multivalue answer, or weighted records for fixed shares |
| One healthy endpoint is sufficient | Simple |

## Canary rollout

| Stage | Production weight | Canary weight | Check before continuing |
| --- | ---: | ---: | --- |
| Baseline | 100 | 0 | Confirm production health |
| Initial test | 90 | 10 | Errors, latency and business transactions |
| Wider test | 50 | 50 | Compare both versions under load |
| Release | 0 | 100 | Confirm the new version is stable |

The canary records should use health checks so an unhealthy destination is not returned. Low DNS TTL values allow weight changes to take effect sooner, but cached responses mean the change is not instantaneous.

Geolocation answers the question, "Where is the user?" Geoproximity answers, "Which resource is geographically closest, after applying any configured bias?"

Route 53 cannot replace the ALB. Route 53 chooses a DNS destination, while the ALB makes request-level routing decisions, checks application targets and distributes connections continuously.

CloudFront is the better choice for cacheable HTTP content delivered through edge locations. Global Accelerator is useful when static anycast IP addresses and AWS backbone routing are needed for TCP or UDP applications. It does not provide content caching.

## Reflection

The weighted policy is useful because a release can move gradually instead of changing every user at once. Health checks and TTLs are part of the design because DNS routing depends on both endpoint health and cached answers. I would use failover for a standby Region and weighted records for a planned canary release.
