# Week 5 Mock Exam Review

## Score

My target for this week was 10/15 or better. I reviewed the questions carefully and used the answer key to identify the topics that need the most attention.

## Questions I found difficult

The most challenging questions were the ones around:

- NACL statelessness and ephemeral ports
- Route 53 Alias vs CNAME at the zone apex
- OAC setup for private S3 access via CloudFront
- The difference between CloudFront and Global Accelerator

## Revision notes

### VPC and NAT

A NAT Gateway is required for private subnets that need outbound internet access without being directly reachable from the internet. The correct highly available pattern is one NAT Gateway per Availability Zone, not a single shared NAT Gateway.

### Security Groups vs NACLs

Security Groups are stateful and resource-level. Network ACLs are stateless and subnet-level. If a NACL allows inbound traffic but not the corresponding outbound response traffic on ephemeral ports, clients will not receive a reply.

### Route 53

An Alias record is the correct choice for the root domain when pointing to an AWS resource such as an ALB or CloudFront distribution. A CNAME cannot be used at the zone apex.

### CloudFront and OAC

CloudFront should be configured with OAC when the origin is a private S3 bucket and access should be restricted to CloudFront only. This is the modern and recommended pattern for secure private content delivery.

### CloudFront vs Global Accelerator

CloudFront is the better choice for cacheable content and edge delivery. Global Accelerator is the better choice for non-HTTP traffic and stable IP-based routing over the AWS backbone.

## Final takeaway

The Week 5 topics now feel much more connected. The VPC, routing, DNS, and edge services all fit together as one networking platform rather than separate concepts.
