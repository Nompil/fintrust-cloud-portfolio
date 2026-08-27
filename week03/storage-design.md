# FinTrust S3 Storage Design

## Bucket strategy

| Bucket | Main use | Controls | Lifecycle |
| --- | --- | --- | --- |
| `fintrust-transactions-af-south-1` | Active transaction JSON records | Versioning, SSE-KMS and Object Lock in compliance mode for five years | S3 Standard, Standard-IA after 30 days, Glacier Instant Retrieval after 90 days and Glacier Deep Archive after one year |
| `fintrust-statements-af-south-1` | Monthly customer statements | Versioning, SSE-KMS and Block Public Access | S3 Standard because statements are downloaded on demand through the portal |
| `fintrust-ml-data-af-south-1` | Fraud-model training data | Versioning, SSE-KMS and Object Lock in governance mode | S3 Standard, then Glacier Flexible Retrieval after 90 days because models are retrained quarterly |

Bucket names are globally unique, so an account identifier can be added if one of these names is unavailable.

## Object Lock decision

Transaction records use compliance mode because no user, including the root user, can shorten the retention period or delete a protected object. This suits the five-year financial-record requirement. The machine-learning bucket uses governance mode because an authorised data owner may need to replace unsuitable training data.

Versioning must remain enabled on every bucket that uses Object Lock. Lifecycle rules also need separate handling for noncurrent versions so that an overwritten object does not remain in an expensive class indefinitely.

## Cost comparison

The course scenario estimates about R24,000 per month if all objects remain in S3 Standard. Applying the lifecycle tiers reduces the steady-state estimate to about R4,200 per month, a saving of R19,800 per month. Most of the saving comes from moving older transaction records into Glacier storage classes instead of paying the S3 Standard rate for the full retention period.
