# Week 5 Day 1 - FinTrust VPC Build

This was the first week where the networking layer started to feel real. Building the VPC made the difference between a diagram and an actual platform much clearer. The key lesson was that a VPC is not just a container; it is the control point for where traffic can go, who can reach which tier, and how the architecture stays secure.

## FinTrust VPC design

| Resource | Configuration |
|---|---|
| VPC name | fintrust-vpc |
| Region | af-south-1 |
| CIDR | 10.0.0.0/16 |
| Availability Zones | af-south-1a and af-south-1b |

## Subnet layout

| Tier | Subnet | CIDR | AZ |
|---|---|---|---|
| Public | fintrust-public-1a | 10.0.0.0/24 | af-south-1a |
| Public | fintrust-public-1b | 10.0.1.0/24 | af-south-1b |
| Application | fintrust-app-1a | 10.0.10.0/24 | af-south-1a |
| Application | fintrust-app-1b | 10.0.11.0/24 | af-south-1b |
| Data | fintrust-data-1a | 10.0.20.0/24 | af-south-1a |
| Data | fintrust-data-1b | 10.0.21.0/24 | af-south-1b |

## Route tables and gateways

### Public route table

- Default route: 0.0.0.0/0 -> Internet Gateway (fintrust-igw)
- Associated with both public subnets
- Used for internet-facing edge resources such as the ALB and NAT gateways

### Private route tables

- One private route table per AZ
- Route 0.0.0.0/0 -> NAT gateway in the same AZ
- Application and data subnets are associated with the private route table for their AZ

### NAT design

- One NAT Gateway in each public subnet
- This avoids a single point of failure if one AZ experiences issues

## Security groups

| Security group | Purpose | Key rule logic |
|---|---|---|
| alb-sg | Internet-facing entry point | Allow HTTPS 443 from 0.0.0.0/0 |
| app-sg | Application tier | Allow TCP 8080 from alb-sg only |
| db-sg | Data tier | Allow 5432, 6379, and 27017 from app-sg only |

## Security Group vs NACL challenge

### 1. Block traffic from a malicious IP range

Answer: NACL DENY rule on the app subnet.

Security Groups cannot deny traffic explicitly. They only allow what is permitted. If the requirement is to block an entire IP range, the correct control is a Network ACL DENY rule at the subnet boundary.

### 2. Allow the ALB to forward requests to containers on port 8080

Answer: Security Group rule on app-sg.

This is a resource-level, stateful control. The ALB should be allowed to reach the application tier on the required port, and the SG makes that easy without opening the app tier to the whole internet.

### 3. Keep the database tier reachable only from the application tier

Answer: Security Group rule on db-sg.

The database should accept traffic only from the application security group. This gives the data tier a clean trust boundary and avoids exposing it directly to the ALB or the internet.

## Traffic path reflection

1. A user sends an HTTPS request from the browser to the FinTrust portal.
2. The request reaches the public subnet through the Internet Gateway.
3. The Application Load Balancer accepts the request and forwards it to the app tier.
4. The application tier reaches the data tier through the appropriate security group rules.
5. The data tier remains private and is not directly reachable from the internet.

## What stood out to me

The biggest lesson was that internet access is not automatic. An Internet Gateway, a route table entry, and a resource with the right network permissions all have to align. That is why VPC design feels so much like architecture rather than just configuration.

