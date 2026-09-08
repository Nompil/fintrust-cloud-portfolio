# Week 8 Self Assessment

**Date completed:** 28 August 2026
**Learner:** Nompilo Eugenia Mchunu

| Topic | Confidence | What I can explain |
| --- | --- | --- |
| S3 lake zones | Got it | Raw data stays immutable, processed data uses partitioned Parquet, and curated data serves reporting. |
| Glue Data Catalog | Got it | Athena and EMR share the table and partition definitions registered by Glue. |
| Athena cost control | Got it | Parquet, partitions, workgroup limits and short-lived result files reduce scan cost. |
| Kinesis shard model | Got it | Each shard has fixed read and write capacity, and the partition key controls placement. |
| Kinesis and Firehose | Got it | Kinesis supports replay and custom consumers, while Firehose manages buffered delivery. |
| OpenSearch | Partly | I can design the ingestion path but want more practice with index lifecycle policies. |
| EMR node types | Got it | Primary and Core nodes stay On-Demand, while replaceable Task capacity can use Spot. |
| QuickSight SPICE | Partly | I understand imports and scheduled refreshes but need more practice sizing capacity. |
| SageMaker lifecycle | Partly | I can place training, endpoints and monitoring in the architecture but need more hands-on deployment practice. |
| Live fraud endpoint | Got it | API Gateway and Lambda call a real-time endpoint, while Batch Transform serves offline scoring. |
| Rekognition | Got it | CompareFaces supports the KYC check and DetectText supports document text extraction. |
| Comprehend | Got it | PII is detected before analytics storage, and sentiment can drive ticket routing. |
| Service selection | Got it | I can separate a custom SageMaker model, a pre-built AWS service and a Bedrock use case. |
| Pandas and Athena | Got it | Pandas suits local development on small extracts, while Athena queries shared S3 data. |

My next priorities are OpenSearch index management, SPICE capacity calculations and the operational steps around a SageMaker endpoint deployment. I will practise those as complete request paths rather than as isolated service definitions.
