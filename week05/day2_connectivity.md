# Week 5 Day 2: FinTrust Connectivity and Load Balancing

This day made the networking story much more practical. The main idea was that a good AWS network is not just about subnets and routes. It is also about choosing the right service for traffic flow, balancing, and connectivity between environments.

## Load balancer choice

### Application Load Balancer

The Application Load Balancer is the correct fit for FinTrust's portal and API traffic because it supports Layer 7 routing. That means it can inspect the URL path and send requests to the correct target group.

Example:

- /api/* -> api-targets
- /portal/* -> portal-targets

This is the right pattern for a modern web application with multiple services behind one entry point.

## ALB path-based routing

The ALB uses listener rules to forward traffic based on the request path. This is useful because the portal and API services can share one public entry point while still being routed separately.

## NAT high availability

A single NAT Gateway is not enough for a resilient Multi-AZ design. The correct pattern is one NAT Gateway per Availability Zone. That way, if one AZ is disrupted, the private subnets in the other AZ can still reach the internet.

## Connectivity decision summary

| Requirement | Service | Why |
|---|---|---|
| Connect three VPCs with central routing | Transit Gateway | Supports transitive routing and hub-and-spoke design |
| Provide private access to a SaaS service | AWS PrivateLink | Gives private service access without full VPC connectivity |
| Connect an on-premises mainframe with dedicated low-latency access | AWS Direct Connect | Provides a private, predictable connection |
| Give remote developers access to a dev VPC | Client VPN | Designed for individual user access |

## Reflection

The biggest takeaway from this day was that networking decisions are heavily shaped by the type of traffic and the growth pattern of the environment. A single solution rarely fits every need, which is why AWS offers multiple connectivity options rather than one universal answer.
