# FinTrust CloudFront Architecture

CloudFront delivers the public portal's static assets while the S3 origins remain private.

The delivery path is shown in the [Week 3 architecture diagrams PDF](diagrams/week03_architecture_diagrams.pdf).

## Controls and behaviour

- Use Origin Access Control with SigV4 so S3 does not need public access.
- Redirect HTTP requests to HTTPS and use an ACM certificate in `us-east-1`, as required by CloudFront.
- Apply a response-headers policy for HSTS and other browser security headers.
- Cache versioned static assets with long TTLs; use invalidations only for urgent unversioned changes.
- Attach AWS WAF for managed threat rules and rate-based controls.
- Send CloudFront access logs to the central logging location.
- Use an origin group only if the business has approved the secondary Region and its data-residency implications.
