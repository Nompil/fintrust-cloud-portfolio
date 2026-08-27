# FinTrust Hybrid Storage Architecture

FinTrust has three storage problems in its Johannesburg data centre. Each one needs a different AWS service because the transfer method and access pattern are different.

## Service decisions

| Requirement | Service | Design |
| --- | --- | --- |
| Move 45 TB of historical records over a limited connection | Snowball Edge Storage Optimised | Load the encrypted device on site, return it to AWS and import the files into `fintrust-archive-af-south-1`. Move the archive to Glacier Flexible Retrieval after 90 days. |
| Receive settlement files from partner banks over SFTP | AWS Transfer Family | Partners keep using SFTP. Transfer Family stores each upload in `fintrust-settlements-af-south-1`, where an S3 event can start settlement processing. |
| Keep an NFS share for the existing core-banking application | S3 File Gateway | The gateway VM presents an NFS mount and caches recent files locally. Reports and audit logs are stored as objects in `fintrust-compliance-logs-af-south-1`. |

## Why DataSync is not used for the NFS share

DataSync is a good choice for a one-time migration or a scheduled copy. It does not provide the always-available NFS share and local cache that the core-banking application expects. S3 File Gateway lets the application continue using its existing file interface while making each file available in S3.

## Service clues

| Words in a requirement | Service |
| --- | --- |
| Large data volume, limited bandwidth, physical transfer | Snowball Edge |
| Partner, SFTP, FTPS, FTP or AS2 | AWS Transfer Family |
| NFS or SMB, local cache, files stored as S3 objects | S3 File Gateway |
| Scheduled transfer, bulk migration or checksum verification | AWS DataSync |
