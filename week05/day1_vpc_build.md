\# Week 5 Day 1 - FinTrust VPC Build



\## VPC Architecture



\### VPC Details



| Resource | Configuration |

|-----------|--------------|

| VPC Name | fintrust-vpc |

| Region | af-south-1 |

| CIDR | 10.0.0.0/16 |



\---



\## Subnet Design



| Tier | Subnet | CIDR | Availability Zone |

|--------|---------|---------|---------|

| Public | fintrust-public-1a | 10.0.0.0/24 | af-south-1a |

| Public | fintrust-public-1b | 10.0.1.0/24 | af-south-1b |

| Application | fintrust-app-1a | 10.0.10.0/24 | af-south-1a |

| Application | fintrust-app-1b | 10.0.11.0/24 | af-south-1b |

| Data | fintrust-data-1a | 10.0.20.0/24 | af-south-1a |

| Data | fintrust-data-1b | 10.0.21.0/24 | af-south-1b |



\---



\## Route Tables



\### Public Route Table



Default Route:



```text

0.0.0.0/0 → Internet Gateway (fintrust-igw)



\# Reflection



\## 1. What is the traffic path for a user HTTPS request from the internet to an ECS task?



A user initiates an HTTPS request from a web browser over the internet. The request reaches the Internet Gateway attached to the FinTrust VPC and is routed to the Application Load Balancer located in the public subnet. The ALB accepts HTTPS traffic on port 443 and forwards approved requests to ECS tasks in the application subnets using the app-sg Security Group rules. The ECS tasks then communicate with backend databases and services through the db-sg Security Group, ensuring that no backend resources are directly exposed to the internet.



\## 2. What is the difference between a public and private route table, and why does it matter?



A public route table contains a default route (0.0.0.0/0) pointing to an Internet Gateway, allowing resources with public IP addresses to communicate directly with the internet. A private route table does not point directly to an Internet Gateway and instead routes outbound traffic through a NAT Gateway. This design improves security because application servers and databases remain inaccessible from the internet while still being able to download updates or access external services when required.



\## 3. One thing about VPC networking that surprised me today



The most surprising concept was that attaching an Internet Gateway to a VPC does not automatically provide internet access. Internet connectivity requires three things to work together: the Internet Gateway must be attached, the subnet route table must contain a route to the Internet Gateway, and the resource must have a public IP address with Security Group rules allowing the traffic. Missing any one of these components breaks connectivity even though the VPC appears correctly configured.

