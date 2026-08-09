Week 5 Reflection

1) What I built this week (3–5 sentences):

I designed and documented the FinTrust VPC, including subnet layout, route tables, NAT design and security group rules. I captured the traffic path from the internet through the ALB to application and data tiers, and documented practical examples of when to use NACLs vs Security Groups. The documentation includes configuration choices and a checklist for building the VPC in `af-south-1`.

2) Key technical decisions and why (3–5 sentences):

The VPC uses multiple public and private subnets across two AZs to improve resilience and reduce blast radius. NAT gateways are deployed per AZ to avoid cross-AZ dependency for private-to-internet egress. Security groups are used for resource-level, stateful controls and NACLs for coarse-grained subnet-level deny rules when required.

3) What I struggled with and how I resolved it (2–4 sentences):

The trickiest area was the NAT and route design for multi-AZ resilience; I resolved this by documenting a per-AZ NAT gateway pattern and associating private subnets with same-AZ NAT gateways. I also clarified when to use NACL DENY rules versus security group allow rules.

4) What I'd add to make this portfolio artifact stronger (1–2 bullet points):

- Add a draw.io exported diagram in `week05/diagrams/` showing subnets and route tables.
- Include a minimal CloudFormation or Terraform example for the VPC to make the design reproducible.
