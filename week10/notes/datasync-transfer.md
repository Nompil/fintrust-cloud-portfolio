# DataSync Transfer Plan

The initial 3 PB compliance archive uses Snowball Edge Storage Optimised devices. DataSync then handles changed files across Direct Connect until final cutover. This hybrid choice is more operationally complex than one DataSync bulk run, but it shortens the bulk movement period and keeps a repeatable delta process.

The DataSync agent is placed beside the NFS source. Transfer traffic is always protected by TLS, including when Direct Connect supplies the private path. The S3 bucket uses a customer managed KMS key and the task role receives only the required key and object permissions. Point in time consistent verification is used for the final complete check. Routine delta runs verify only transferred files.

Business hours use a 500 Mbps task limit. Overnight hours use 9,000 Mbps. EventBridge Scheduler changes the limit at the defined SAST boundaries. Before decommissioning the NAS, the dashboard must show a successful final execution, zero failed files, destination verification complete, the expected byte and file totals, an acceptable delta age and approval from the data owner.

Files and database rows use different tools. NFS, SMB and NAS content use DataSync. Structured database records and CDC use DMS. Snowball is the bulk option when the network would take too long, while MGN copies a complete server image to EC2.
