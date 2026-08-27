# FinTrust CloudFront Architecture

CloudFront delivers the FinTrust customer portal while both S3 origins remain private.

The delivery path is shown in the [FinTrust S3 architecture diagram](diagrams/fintrust_s3_architecture.png) and the [PDF version](diagrams/fintrust_s3_architecture.pdf).

## Request path

1. Route 53 maps `portal.fintrust.co.za` to the CloudFront distribution with an Alias record.
2. CloudFront presents an ACM certificate issued in `us-east-1` and redirects HTTP requests to HTTPS.
3. Origin Access Control signs requests to `fintrust-portal-af-south-1` using Signature Version 4.
4. The S3 bucket policy allows reads from the named CloudFront distribution only. Block Public Access remains enabled.

## Cache behaviours

| Path | Origin | TTL | Reason |
| --- | --- | ---: | --- |
| `/assets/*` | Primary S3 bucket | 365 days | Asset filenames are versioned, so they can stay at the edge |
| `/*` | Primary S3 bucket | 3,600 seconds | HTML changes become available without a long wait |

Compression is enabled for text, CSS and JavaScript. A response-headers policy adds HSTS, `X-Content-Type-Options` and `X-Frame-Options`.

## Origin failover

The origin group uses `fintrust-portal-af-south-1` as primary and `fintrust-portal-eu-west-1` as secondary. Versioning is enabled on both buckets, and Cross-Region Replication copies new portal objects to the secondary Region. If the primary returns a configured server error, CloudFront retries the request against the secondary origin.

Cross-Region Replication does not copy old objects automatically. Existing objects need an S3 Batch Replication job, and delete-marker replication must be enabled deliberately if the recovery design requires it.
