# Week 5: AWS Networking

Week 5 develops the network and edge-delivery layer for FinTrust. The design keeps the application and database tiers private while exposing only the load balancer through public subnets.

## Deliverables

- [VPC build](day1_vpc_build.md)
- [Connectivity choices](day2_connectivity.md)
- [Route 53 routing](day3_route53.md)
- [CloudFront design](day4_cloudfront.md)
- [VPC architecture diagram PDF](diagrams/week05_vpc_architecture.pdf)
- [Mock exam review](mock_exam_review.md)

## Key design choices

- `af-south-1` is the primary Region.
- Public and private subnets span two Availability Zones.
- Each private application subnet uses a NAT Gateway in the same Availability Zone.
- The internet-facing Application Load Balancer is the only public entry point to the application tier.
- Security groups allow only the traffic required between the load balancer, application, and database tiers.
- Route 53 and CloudFront provide DNS routing, caching, TLS, and edge delivery.
