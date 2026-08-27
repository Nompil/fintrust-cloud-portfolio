# Day 2: Load Balancing and Connectivity

The FinTrust web entry point uses an Application Load Balancer because the routing decisions depend on the URL path. The ALB terminates HTTPS and sends each request to the correct group of ECS tasks.

## Target groups

| Target group | Protocol and port | Health check | Expected result |
| --- | --- | --- | --- |
| `api-targets` | HTTP 8080 | `/api/health` | HTTP 200 |
| `portal-targets` | HTTP 8080 | `/portal/health` | HTTP 200 |

Both target groups use IP targets so they can register ECS tasks. Health checks prevent the ALB from sending customer traffic to an unhealthy task.

## ALB configuration

| Setting | Value |
| --- | --- |
| Name | `fintrust-alb` |
| Scheme | Internet facing |
| Subnets | Both public subnets |
| Security Group | `alb-sg` |
| HTTPS listener | Port 443 |
| HTTP listener for the lab | Port 80 |
| Default action | Forward to `portal-targets` |

## Listener rules

| Priority | Condition | Action |
| --- | --- | --- |
| 10 | Path is `/api/*` | Forward to `api-targets` |
| 20 | Path is `/portal/*` | Forward to `portal-targets` |
| Default | No earlier rule matched | Forward to `portal-targets` |

For a production deployment, port 80 should redirect to HTTPS. The certificate for port 443 would be stored in AWS Certificate Manager.

## Request path for `/api/transfer`

1. Route 53 returns an alias to the ALB or CloudFront distribution.
2. The client establishes an HTTPS connection.
3. The ALB listener evaluates the path rules.
4. `/api/*` matches the API rule.
5. The ALB chooses a healthy target from `api-targets`.
6. The ECS task processes the transfer and connects to the data tier through `db-sg`.
7. The response returns to the customer through the ALB.

## Connectivity worksheet

| Scenario | Selected service | Reason |
| --- | --- | --- |
| Production, development and audit VPCs need shared egress | Transit Gateway | It provides a central hub and avoids a growing peering mesh |
| FinTrust consumes a private fraud service from a SaaS provider | AWS PrivateLink | It exposes only the service and does not join the two networks |
| The on-premises mainframe needs consistent private connectivity | AWS Direct Connect | A dedicated connection provides more predictable performance than an internet VPN |
| Ten engineers need temporary private access | AWS Client VPN | It provides managed, user-based remote access without a site appliance |

VPC peering would be awkward for the three-account design because every required pair needs its own connection and peering is not transitive. Transit Gateway gives the accounts one central point for routing and control.

Direct Connect and Site-to-Site VPN solve different needs. Direct Connect is suitable for steady, business-critical traffic that needs predictable performance. A Site-to-Site VPN is quicker to establish and useful as an encrypted backup path, but it crosses the public internet.

PrivateLink is preferable to peering for the SaaS service because FinTrust receives access to a specific endpoint service rather than routes to the provider's whole VPC. This reduces network exposure and avoids overlapping CIDR concerns.

## Reflection

Path-based routing makes one ALB useful for more than one application component. The connectivity exercise also showed me that the correct service depends on the relationship being created: Transit Gateway joins networks at scale, PrivateLink publishes one service, Direct Connect links a site, and Client VPN connects individual users.
