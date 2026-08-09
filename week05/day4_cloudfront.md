# Week 5 Day 4 - CloudFront and Architecture Review

This final networking day tied the whole Week 5 story together. The important shift was from building isolated components to understanding how they work together as one secure, high-availability edge architecture.

## CloudFront distribution setup

FinTrust uses CloudFront in front of its portal assets so static content can be served quickly from edge locations while keeping the origin private.

### Distribution design

| Component | Configuration |
|---|---|
| Origin | Private S3 bucket for portal assets |
| Access model | Origin Access Control (OAC) |
| Viewer policy | Redirect HTTP to HTTPS |
| Default root object | index.html |
| API behaviour | /api/* with CachingDisabled |

## OAC vs OAI

Origin Access Control is the modern and recommended approach for private S3 access through CloudFront. It allows CloudFront to sign requests to S3 and gives the bucket policy a clear trust relationship with the distribution.

Why OAC is preferred:

- It is the current AWS-recommended method for new distributions
- It supports KMS-encrypted S3 content
- It is more flexible and clearer than the older OAI model

## Signed URLs and signed cookies

For FinTrust's customer statement PDFs, a signed URL is the right choice because each document is a specific file and the access window should be controlled per link.

- Signed URL: best for one file, one expiry window
- Signed Cookie: better for a group of protected files or a subscriber experience

## Cache invalidation

CloudFront can keep serving older content until its TTL expires. When an urgent fix is required, the fastest option is an invalidation for the specific path.

Example:

- /styles/main.css -> immediate cache purge for that path

This is often faster and cleaner than waiting for the full TTL to expire.

## Full Week 5 architecture summary

The Week 5 network architecture now includes:

- A Multi-AZ VPC with public, application, and data tiers
- Internet Gateway and NAT Gateways for controlled traffic flow
- ALB path-based routing for portal and API traffic
- Route 53 for domain routing, failover, and weighted traffic
- CloudFront with OAC in front of private S3 assets
- A secure layered Security Group model to keep tiers isolated

## Reflection

The main lesson from this week was that networking is really about trade-offs. The right design depends on whether the requirement is about resiliency, performance, security, or cost. The strongest architectures are the ones that combine these concerns deliberately rather than treating them as separate problems.
