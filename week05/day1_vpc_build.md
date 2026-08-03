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

