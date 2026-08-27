# Week 5 Mock Exam Review

My target for the timed knowledge check was at least 10 out of 15. I used the review to group the networking topics that need more practice instead of memorising isolated service names.

## Answer review

| Question | Answer | Topic |
| ---: | :---: | --- |
| 1 | B | NAT Gateway for private subnet internet access |
| 2 | B | Stateless NACL return traffic |
| 3 | B | One NAT Gateway per Availability Zone |
| 4 | B | Transit Gateway for several VPCs |
| 5 | C | ALB for path-based HTTP routing |
| 6 | B | NLB for high-performance TCP traffic |
| 7 | C | Alias A record for an AWS load balancer |
| 8 | B | Latency-based routing |
| 9 | B | Route 53 health check for failover |
| 10 | B | CloudFront OAC and a restricted bucket policy |
| 11 | B | CloudFront cache invalidation |
| 12 | C | Direct Connect for predictable private connectivity |
| 13 | C | NACL deny rule for a CIDR block |
| 14 | B | Global Accelerator for static anycast IP addresses |
| 15 | B | ALB, Route 53 failover and CloudFront with OAC |

## Questions marked for revision

### Question 2: Network ACL return traffic

A NACL is stateless, so both directions require matching rules. Allowing the inbound service port is not enough. The response must be allowed to return through the client's ephemeral port range.

### Question 7: Alias A and CNAME

An Alias A record can target supported AWS resources and works at the hosted-zone apex. A CNAME points one hostname to another and cannot be placed at the apex.

### Question 10: Private S3 with CloudFront

Block Public Access remains enabled. OAC signs CloudFront requests, and the bucket policy grants read access only to the selected distribution.

### Question 14: CloudFront and Global Accelerator

CloudFront caches HTTP content at edge locations. Global Accelerator provides static anycast IP addresses and carries TCP or UDP traffic across the AWS global network. The requirement for static IP addresses is the deciding clue.

## Confidence check

| Area | Confidence | Revision action |
| --- | --- | --- |
| VPC CIDR and subnet routing | Green | Practise reading route tables |
| Security Groups and NACLs | Amber | Trace inbound and return traffic |
| Load balancer selection | Green | Compare ALB and NLB scenarios |
| VPC connectivity | Amber | Match each service to its scope |
| Route 53 policies | Amber | Practise policy signal words |
| CloudFront and OAC | Amber | Rebuild the request and permission path |

## Key takeaway

The strongest method for these questions is to identify the exact requirement first. Path rules point to ALB, static anycast IP addresses point to Global Accelerator, private access to one provider service points to PrivateLink, and an explicit network deny points to a NACL.
