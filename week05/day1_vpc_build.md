# Day 1: VPC Build

The FinTrust network uses one VPC across two Availability Zones. Public, application and data subnets are separated so that each tier has only the routes it needs.

## VPC plan

| Item | Configuration |
| --- | --- |
| VPC name | `fintrust-vpc` |
| IPv4 CIDR | `10.0.0.0/16` |
| Availability Zones | `af-south-1a`, `af-south-1b` |
| DNS hostnames | Enabled |
| DNS resolution | Enabled |

## Subnet allocation

| Tier | Availability Zone | CIDR | Purpose |
| --- | --- | --- | --- |
| Public | `af-south-1a` | `10.0.0.0/24` | ALB and NAT Gateway |
| Public | `af-south-1b` | `10.0.1.0/24` | ALB and NAT Gateway |
| Application | `af-south-1a` | `10.0.10.0/24` | ECS workloads |
| Application | `af-south-1b` | `10.0.11.0/24` | ECS workloads |
| Data | `af-south-1a` | `10.0.20.0/24` | Database resources |
| Data | `af-south-1b` | `10.0.21.0/24` | Database resources |

## Route tables and internet access

An Internet Gateway is attached to the VPC. Each public subnet uses the public route table, while the private subnets use a route table for their own Availability Zone.

| Route table | Subnet associations | Default route |
| --- | --- | --- |
| `fintrust-public-rt` | Both public subnets | `0.0.0.0/0` to the Internet Gateway |
| `fintrust-private-rt-1a` | App and data subnets in `af-south-1a` | `0.0.0.0/0` to NAT Gateway 1a |
| `fintrust-private-rt-1b` | App and data subnets in `af-south-1b` | `0.0.0.0/0` to NAT Gateway 1b |

There is one NAT Gateway in each public subnet. A private subnet routes through the NAT Gateway in the same Availability Zone. This keeps outbound access available if one Availability Zone fails and avoids unnecessary cross-zone traffic charges.

The public subnets are public because their route table points to the Internet Gateway. The private subnets do not have that route. A public IP address alone does not make a subnet public.

## Security Group chain

| Security Group | Inbound rule | Source |
| --- | --- | --- |
| `alb-sg` | HTTPS on TCP 443 | `0.0.0.0/0` |
| `app-sg` | Application traffic on TCP 8080 | `alb-sg` |
| `db-sg` | PostgreSQL on TCP 5432 | `app-sg` |
| `db-sg` | Redis on TCP 6379 | `app-sg` |
| `db-sg` | MongoDB on TCP 27017 | `app-sg` |

The rules reference Security Groups instead of application IP addresses. This means a new ECS task receives the correct access without changing the database rules.

## Security Group and NACL challenge

| Requirement | Control | Reason |
| --- | --- | --- |
| Block traffic from `41.0.0.0/8` | Network ACL deny rule | Security Groups cannot create explicit deny rules |
| Allow only the ALB to reach ECS | `app-sg` inbound rule | A Security Group can reference `alb-sg` directly |
| Allow only the app tier to reach databases | `db-sg` inbound rules | The source is limited to `app-sg` |

Network ACLs are stateless. If the subnet NACL permits an inbound connection, the matching outbound response must also be permitted. For a client connection, the response normally returns to an ephemeral port in the range `1024` to `65535`.

## Request path

1. A customer resolves the application name through Route 53.
2. The request reaches CloudFront over HTTPS.
3. A dynamic request is forwarded to the public Application Load Balancer.
4. The ALB sends the request to a healthy ECS task in a private application subnet.
5. The task connects to the required data service through `db-sg`.
6. The response returns through the same controlled path.

## Reflection

The most important lesson was that a subnet is classified by its routing, not its name. I also understood why a NAT Gateway belongs in a public subnet even though it provides outbound access for private resources. Using Security Group references makes the three-tier design easier to maintain than rules based on changing IP addresses.
