# Week 5 Reflection

This week I designed the network path from the customer to the application and database tiers. The VPC uses public and private subnets across two Availability Zones, with the load balancer in public subnets and the application and database resources kept private.

The most important networking decision was avoiding a cross-AZ dependency for outbound traffic. Each private application subnet routes through a NAT Gateway in the same Availability Zone. Security groups then restrict traffic between the load balancer, application, and database tiers.

Route 53 and CloudFront complete the request path with DNS routing, TLS, caching, and edge delivery. Together, these decisions give FinTrust a clear network design that can be reviewed before deployment.
