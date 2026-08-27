# Week 5: Networking and Content Delivery

Week 5 brings the FinTrust network together across two Availability Zones. The work covers VPC design, traffic controls, load balancing, private connectivity, DNS routing and secure content delivery.

## Portfolio work

| File | Evidence |
| --- | --- |
| [Day 1 VPC build](day1_vpc_build.md) | CIDR plan, route tables, Security Group chain and NACL challenge |
| [Day 2 connectivity](day2_connectivity.md) | ALB path rules, target groups and four connectivity scenarios |
| [Day 3 Route 53](day3_route53.md) | Hosted-zone records, seven routing policies and a canary rollout |
| [Day 4 CloudFront](day4_cloudfront.md) | OAC configuration, failover timing and architecture review |
| [Mock exam review](mock_exam_review.md) | Answer review, revision notes and confidence check |

## Supporting evidence

| File | Purpose |
| --- | --- |
| [Week 5 network architecture](diagrams/week05_vpc_architecture.pdf) | Detailed two-AZ design and network controls |
| [Weekly reflection](reflection.md) | Main lessons and design decisions |

## Design summary

The VPC uses the `10.0.0.0/16` range with public, application and data subnets in `af-south-1a` and `af-south-1b`. Internet traffic reaches CloudFront and the ALB, while application and data resources remain in private subnets. NAT Gateways provide resilient outbound access, gateway endpoints keep S3 and DynamoDB traffic on the AWS network, and Security Group references enforce the application path. Route 53 supplies weighted and failover routing, while OAC protects the private S3 origin.
