\# Week 3 CloudFront Architecture



\## Overview



FinTrust uses Amazon CloudFront in front of Amazon S3 to deliver customer portal content securely and with low latency.



The architecture provides:



\- HTTPS support

\- Global edge caching

\- Origin failover

\- Cross-Region disaster recovery

\- Private S3 access through OAC



\---



\## Architecture Diagram (Text-Based)



```text

Customer Browser

&#x20;       |

&#x20;       v

Route 53

&#x20;       |

&#x20;       v

CloudFront Distribution

&#x20;       |

&#x20;       +-------------------+

&#x20;       |                   |

&#x20;       v                   v

Primary Origin        Secondary Origin

S3 (af-south-1)       S3 (eu-west-1)

&#x20;       |

&#x20;       v

Cross-Region Replication (CRR)

