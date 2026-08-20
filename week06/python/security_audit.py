"""Audit IAM and Security Group controls, then save a dated JSON report."""

import json
import os
from datetime import datetime, timezone


RESTRICTED_PORTS = {22, 3389, 5432, 3306, 1521}
OPEN_IPV4 = "0.0.0.0/0"
OPEN_IPV6 = "::/0"


def _isoformat(value):
    return value.isoformat() if hasattr(value, "isoformat") else str(value)


def users_without_mfa(iam_client):
    """Find console users who do not have an MFA device."""
    findings = []
    paginator = iam_client.get_paginator("list_users")

    for page in paginator.paginate():
        for user in page.get("Users", []):
            username = user["UserName"]
            try:
                iam_client.get_login_profile(UserName=username)
            except iam_client.exceptions.NoSuchEntityException:
                continue

            devices = iam_client.list_mfa_devices(UserName=username).get("MFADevices", [])
            if not devices:
                findings.append(
                    {
                        "username": username,
                        "created": _isoformat(user.get("CreateDate")),
                        "last_activity": _isoformat(user.get("PasswordLastUsed", "never")),
                    }
                )
    return findings


def stale_access_keys(iam_client, now=None, maximum_age_days=90):
    """Find active IAM access keys older than the permitted age."""
    current_time = now or datetime.now(timezone.utc)
    findings = []
    paginator = iam_client.get_paginator("list_users")

    for page in paginator.paginate():
        for user in page.get("Users", []):
            username = user["UserName"]
            for key in iam_client.list_access_keys(UserName=username).get("AccessKeyMetadata", []):
                created = key["CreateDate"]
                if created.tzinfo is None:
                    created = created.replace(tzinfo=timezone.utc)
                age_days = (current_time - created).days
                if key.get("Status") == "Active" and age_days > maximum_age_days:
                    findings.append(
                        {
                            "username": username,
                            "access_key_id": key["AccessKeyId"],
                            "created": created.isoformat(),
                            "age_days": age_days,
                        }
                    )
    return findings


def security_group_exposure(security_group):
    """Return findings for restricted ports exposed to the internet."""
    findings = []
    for rule in security_group.get("IpPermissions", []):
        all_traffic = rule.get("IpProtocol") == "-1"
        from_port = 0 if all_traffic else rule.get("FromPort", 0)
        to_port = 65535 if all_traffic else rule.get("ToPort", 65535)
        open_ranges = [item.get("CidrIp") for item in rule.get("IpRanges", [])]
        open_ranges += [item.get("CidrIpv6") for item in rule.get("Ipv6Ranges", [])]

        if OPEN_IPV4 not in open_ranges and OPEN_IPV6 not in open_ranges:
            continue

        exposed_ports = sorted(port for port in RESTRICTED_PORTS if from_port <= port <= to_port)
        if not exposed_ports and not all_traffic:
            continue

        findings.append(
            {
                "sg_id": security_group["GroupId"],
                "sg_name": security_group.get("GroupName", security_group["GroupId"]),
                "port_range": "all" if all_traffic else f"{from_port}-{to_port}",
                "restricted_ports": exposed_ports,
                "cidrs": sorted(set(open_ranges)),
                "severity": "CRITICAL" if all_traffic else "HIGH",
            }
        )
    return findings


def exposed_security_groups(ec2_client):
    """Audit every Security Group returned by the EC2 paginator."""
    findings = []
    paginator = ec2_client.get_paginator("describe_security_groups")
    for page in paginator.paginate():
        for security_group in page.get("SecurityGroups", []):
            findings.extend(security_group_exposure(security_group))
    return findings


def build_report(iam_client, ec2_client, sts_client, now=None):
    """Build the complete Week 6 security findings document."""
    current_time = now or datetime.now(timezone.utc)
    return {
        "report_date": current_time.isoformat(),
        "account_id": sts_client.get_caller_identity()["Account"],
        "findings": {
            "iam_mfa_violations": users_without_mfa(iam_client),
            "iam_stale_access_keys": stale_access_keys(iam_client, current_time),
            "sg_open_port_violations": exposed_security_groups(ec2_client),
        },
    }


def save_report(s3_client, bucket, report, kms_key_id=None):
    """Upload the report to a dated S3 key using KMS encryption."""
    report_time = datetime.fromisoformat(report["report_date"])
    key = f"security-audit/{report_time:%Y/%m/%d}/findings.json"
    request = {
        "Bucket": bucket,
        "Key": key,
        "Body": json.dumps(report, indent=2),
        "ContentType": "application/json",
        "ServerSideEncryption": "aws:kms",
    }
    if kms_key_id:
        request["SSEKMSKeyId"] = kms_key_id
    s3_client.put_object(**request)
    return f"s3://{bucket}/{key}"


def main():
    import boto3

    bucket = os.environ.get("FINTRUST_AUDIT_BUCKET")
    if not bucket:
        raise SystemExit("Set FINTRUST_AUDIT_BUCKET before running the audit.")

    session = boto3.Session(region_name="af-south-1")
    report = build_report(
        session.client("iam"),
        session.client("ec2"),
        session.client("sts"),
    )
    location = save_report(
        session.client("s3"),
        bucket,
        report,
        os.environ.get("FINTRUST_AUDIT_KMS_KEY_ID"),
    )
    print(f"Report saved to {location}")


if __name__ == "__main__":
    main()
