# Day 4: CloudFront and Origin Access Control

CloudFront provides the public entry point for static portal content stored in a private S3 bucket. Origin Access Control keeps the bucket private while allowing the distribution to sign its origin requests.

## Distribution configuration

| Setting | Configuration |
| --- | --- |
| Static origin | Private S3 bucket |
| Origin access | Origin Access Control with signed requests |
| Default root object | `index.html` |
| Viewer protocol policy | Redirect HTTP to HTTPS |
| Default cache behaviour | Static portal content from S3 |
| `/api/*` behaviour | ALB origin with `CachingDisabled` |
| S3 public access | Block Public Access enabled |
| Custom certificate | AWS Certificate Manager certificate in `us-east-1` |

The S3 bucket policy grants `s3:GetObject` to the CloudFront service principal. Its condition limits access to the ARN of the intended distribution. There is no public principal in the policy.

## Verification

The setup is correct when the direct S3 object URL returns access denied and the CloudFront URL returns the object successfully. This proves that customers use the distribution and that the bucket is not publicly readable.

## Origin Access Control and Origin Access Identity

OAC is the current approach and supports signed requests using Signature Version 4. It also supports more S3 scenarios than the older OAI model. OAI remains relevant when maintaining an existing distribution, but I would choose OAC for a new FinTrust distribution.

Signed URLs are suitable for access to one protected file. Signed cookies are more convenient when a user needs access to several restricted files without placing a signature on every link.

## Failover timing

| Event | Approximate time |
| --- | --- |
| Primary health check fails once | 30 seconds |
| Three consecutive failures mark it unhealthy | About 90 seconds |
| Route 53 starts returning the secondary record | After health status changes |
| Clients receive the secondary answer | Depends on their remaining DNS cache time |

A TTL of 60 seconds gives a reasonable balance between response time and DNS query volume for this design. After the primary has recovered and passed its health checks, Route 53 can return traffic to it. The recovery should be observed before failback to avoid switching repeatedly between Regions.

## Other practical decisions

CloudFront can sit in front of the ALB for dynamic web traffic. The `/api/*` behaviour should forward the required headers, cookies and query strings, and use the managed `CachingDisabled` policy when responses must not be cached.

If `/styles/main.css` changes and the existing cached object must be replaced immediately, the invalidation path is `/styles/main.css`. Versioned file names are usually better for routine releases because they avoid repeated invalidations.

## Architecture review

The complete design includes Route 53, CloudFront, a private S3 origin using OAC, an ALB in two public subnets, ECS tasks in two private application subnets, and RDS, ElastiCache and DocumentDB in private data subnets. Each Availability Zone has its own NAT Gateway. Gateway endpoints provide private routes to S3 and DynamoDB. The Security Group chain is `alb-sg` to `app-sg` to `db-sg`. Global Accelerator is shown as an alternative entry path for applications that need static anycast IP addresses rather than caching.

[Open the detailed Week 5 network architecture](diagrams/week05_vpc_architecture.pdf)

## Reflection

Keeping S3 private was the most important part of the CloudFront exercise. OAC gives CloudFront permission without exposing the bucket. I also learned that failover time is not controlled by one setting: health-check intervals, failure thresholds and DNS caching all contribute to the customer experience.
