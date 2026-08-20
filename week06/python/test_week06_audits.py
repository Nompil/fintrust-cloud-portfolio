"""Local tests for the Week 6 audit and reporting functions."""

import json
import unittest
from datetime import datetime, timedelta, timezone

import risk_activity_report
import s3_audit
import security_audit


class Pages:
    def __init__(self, pages):
        self.pages = pages

    def paginate(self, **unused):
        return iter(self.pages)


class RecordingS3:
    def __init__(self):
        self.requests = []

    def put_object(self, **request):
        self.requests.append(request)


class S3AuditClient:
    def list_buckets(self):
        return {
            "Buckets": [
                {
                    "Name": "fintrust-audit-evidence",
                    "CreationDate": datetime(2026, 8, 20, tzinfo=timezone.utc),
                }
            ]
        }

    def get_bucket_location(self, **unused):
        return {"LocationConstraint": "af-south-1"}

    def get_public_access_block(self, **unused):
        return {
            "PublicAccessBlockConfiguration": {
                "BlockPublicAcls": True,
                "IgnorePublicAcls": True,
                "BlockPublicPolicy": True,
                "RestrictPublicBuckets": True,
            }
        }

    def get_bucket_encryption(self, **unused):
        return {"ServerSideEncryptionConfiguration": {"Rules": [{}]}}


class IAMClient:
    def __init__(self, now):
        self.now = now

    def get_paginator(self, operation):
        if operation != "list_users":
            raise AssertionError(f"Unexpected operation: {operation}")
        return Pages(
            [
                {
                    "Users": [
                        {
                            "UserName": "analyst",
                            "CreateDate": self.now - timedelta(days=180),
                        }
                    ]
                }
            ]
        )

    def list_access_keys(self, **unused):
        return {
            "AccessKeyMetadata": [
                {
                    "AccessKeyId": "AKIAEXAMPLE",
                    "CreateDate": self.now - timedelta(days=120),
                    "Status": "Active",
                }
            ]
        }


class ActivityS3(RecordingS3):
    def __init__(self, modified):
        super().__init__()
        self.modified = modified

    def get_paginator(self, operation):
        if operation != "list_objects_v2":
            raise AssertionError(f"Unexpected operation: {operation}")
        return Pages([{"Contents": [{"LastModified": self.modified}]}])


class WeekSixTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 8, 20, 12, 0, tzinfo=timezone.utc)

    def test_s3_audit_reports_region_public_block_and_encryption(self):
        findings = s3_audit.audit_buckets(S3AuditClient())
        self.assertEqual(findings[0]["region"], "af-south-1")
        self.assertEqual(findings[0]["public_access"], "SAFE")
        self.assertEqual(findings[0]["encryption"], "ENCRYPTED")

    def test_stale_access_key_is_reported(self):
        findings = security_audit.stale_access_keys(IAMClient(self.now), self.now)
        self.assertEqual(findings[0]["username"], "analyst")
        self.assertEqual(findings[0]["age_days"], 120)

    def test_world_open_database_port_is_high_severity(self):
        group = {
            "GroupId": "sg-0123456789",
            "GroupName": "database",
            "IpPermissions": [
                {
                    "IpProtocol": "tcp",
                    "FromPort": 5432,
                    "ToPort": 5432,
                    "IpRanges": [{"CidrIp": "0.0.0.0/0"}],
                    "Ipv6Ranges": [],
                }
            ],
        }
        findings = security_audit.security_group_exposure(group)
        self.assertEqual(findings[0]["restricted_ports"], [5432])
        self.assertEqual(findings[0]["severity"], "HIGH")

    def test_security_report_uses_a_dated_kms_encrypted_key(self):
        client = RecordingS3()
        report = {"report_date": self.now.isoformat(), "findings": {}}
        location = security_audit.save_report(
            client, "fintrust-security-reports", report, "alias/fintrust-audit"
        )
        request = client.requests[0]
        self.assertEqual(
            location,
            "s3://fintrust-security-reports/security-audit/2026/08/20/findings.json",
        )
        self.assertEqual(request["ServerSideEncryption"], "aws:kms")
        self.assertEqual(request["SSEKMSKeyId"], "alias/fintrust-audit")

    def test_risk_rows_include_recent_s3_activity(self):
        client = ActivityS3(self.now - timedelta(days=2))
        rows = [{"customer_id": "8", "risk_score": "0.55", "spike_flag": "1"}]
        enriched = risk_activity_report.enrich_rows(
            client, "fintrust-transactions-prod", rows, self.now
        )
        self.assertEqual(
            enriched,
            [
                {
                    "customer_id": 8,
                    "risk_score": 0.55,
                    "spike_flag": 1,
                    "s3_activity_7d": True,
                }
            ],
        )

        location = risk_activity_report.upload_report(
            client, "fintrust-security-reports", enriched, self.now
        )
        request = client.requests[0]
        document = json.loads(request["Body"])
        self.assertEqual(document["customer_count"], 1)
        self.assertEqual(request["ServerSideEncryption"], "aws:kms")
        self.assertEqual(
            location,
            "s3://fintrust-security-reports/fraud-risk/2026/08/20/customer-risk.json",
        )


if __name__ == "__main__":
    unittest.main()
