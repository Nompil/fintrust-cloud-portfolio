# SAA Domains 1 and 2 Review

Domain 1 focuses on secure architectures. Start with the protection objective: IAM and Identity Center for access, KMS and ACM for encryption, CloudTrail for API traceability, and WAF or Shield for public application protection. Security Groups are stateful controls applied to resources. Network ACLs are stateless controls applied to subnets.

Domain 2 focuses on resilient architectures. Match recovery requirements to the disaster recovery design. Backup and restore suits recovery measured in hours. Pilot light keeps core data services ready for a sub-hour recovery. Warm standby keeps a scaled-down application running for recovery in minutes. Multi-site active-active is for near-zero recovery objectives and costs the most.

The useful discriminator is the stated problem. A database surviving an Availability Zone failure points to Multi-AZ and Reliability. A global application needing lower latency points to CloudFront, Global Accelerator or a regional design depending on the protocol and workload. A requirement to prevent a control being disabled across member accounts points to an SCP, not an IAM policy or Config rule.
