"""Produce the Week 6 FinTrust S3 security audit."""

from datetime import datetime


def _error_code(error):
    return getattr(error, "response", {}).get("Error", {}).get("Code", "")


def public_access_is_blocked(s3_client, bucket_name):
    """Return True only when all four S3 public-access controls are enabled."""
    try:
        response = s3_client.get_public_access_block(Bucket=bucket_name)
    except Exception as error:
        if _error_code(error) in {
            "NoSuchPublicAccessBlockConfiguration",
            "NoSuchPublicAccessBlockConfigurationException",
        }:
            return False
        raise

    config = response["PublicAccessBlockConfiguration"]
    return all(
        config.get(setting, False)
        for setting in (
            "BlockPublicAcls",
            "IgnorePublicAcls",
            "BlockPublicPolicy",
            "RestrictPublicBuckets",
        )
    )


def encryption_is_enabled(s3_client, bucket_name):
    """Return True when the bucket has a default encryption configuration."""
    try:
        response = s3_client.get_bucket_encryption(Bucket=bucket_name)
    except Exception as error:
        if _error_code(error) in {
            "ServerSideEncryptionConfigurationNotFoundError",
            "NoSuchBucket",
        }:
            return False
        raise

    rules = response.get("ServerSideEncryptionConfiguration", {}).get("Rules", [])
    return bool(rules)


def audit_buckets(s3_client):
    """Return a security summary for every S3 bucket in the account."""
    findings = []
    for bucket in s3_client.list_buckets().get("Buckets", []):
        name = bucket["Name"]
        location = s3_client.get_bucket_location(Bucket=name)
        region = location.get("LocationConstraint") or "us-east-1"
        created = bucket.get("CreationDate")
        created_text = created.strftime("%Y-%m-%d") if isinstance(created, datetime) else str(created)

        findings.append(
            {
                "bucket": name,
                "created": created_text,
                "region": region,
                "public_access": "SAFE" if public_access_is_blocked(s3_client, name) else "EXPOSED",
                "encryption": "ENCRYPTED" if encryption_is_enabled(s3_client, name) else "UNENCRYPTED",
            }
        )
    return findings


def print_report(findings):
    """Print the fixed-width report required by the lab."""
    print(f"{'BUCKET':45} {'CREATED':10} {'REGION':15} {'PUBLIC ACCESS':13} ENCRYPTION")
    print("=" * 108)
    for item in findings:
        print(
            f"{item['bucket']:45} {item['created']:10} {item['region']:15} "
            f"{item['public_access']:13} {item['encryption']}"
        )


def main():
    import boto3

    session = boto3.Session(region_name="af-south-1")
    print_report(audit_buckets(session.client("s3")))


if __name__ == "__main__":
    main()
