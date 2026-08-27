# Week 5 Reflection

This week helped me see networking as a complete request path rather than a list of separate AWS services. I can now trace a customer request from Route 53 and CloudFront to the ALB, through an ECS task and into the data tier. Building the subnet and route-table plan also made the difference between public and private subnets much clearer.

The Security Group and NACL exercises were the most useful. Security Groups are stateful and work well when one application tier needs to trust another. NACLs are stateless, work at subnet level and can create an explicit deny rule. Remembering the return path and ephemeral ports is still an area I want to practise.

For the FinTrust design, I would use Transit Gateway for the account network hub, PrivateLink for a specific provider service, Direct Connect for the mainframe connection and Client VPN for individual engineers. Route 53 weighted records support a controlled canary release, while CloudFront with OAC delivers static files without making the S3 bucket public. These choices keep the architecture resilient without giving each component more network access than it needs.
