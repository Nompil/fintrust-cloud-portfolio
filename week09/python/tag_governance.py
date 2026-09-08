"""Audit FinTrust resource tags and inventory Service Catalog portfolios."""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import date
from typing import Any, Mapping


REQUIRED_TAGS = ("CostCentre", "Team", "Environment")
ALLOWED_VALUES: dict[str, set[str]] = {
    "CostCentre": {"CoreBanking", "Analytics", "Security", "DevOps", "Migration"},
    "Team": {"Platform", "DataEngineering", "AppSec", "SRE", "DataMigration"},
    "Environment": {"Production", "Staging", "Dev", "Sandbox", "DR"},
}


@dataclass(frozen=True)
class TagViolation:
    resource_arn: str
    service: str
    missing: tuple[str, ...]
    invalid: tuple[str, ...]


@dataclass(frozen=True)
class TagAudit:
    total_scanned: int
    compliant: int
    violations: tuple[TagViolation, ...]


def service_from_arn(arn: str) -> str:
    parts = arn.split(":")
    return parts[2] if len(parts) > 2 and parts[2] else "unknown"


def audit_tag_compliance(tagging_client: Any) -> TagAudit:
    """Check required keys and approved values across every returned page."""
    paginator = tagging_client.get_paginator("get_resources")
    total = 0
    violations = []
    for page in paginator.paginate(ResourcesPerPage=100):
        for resource in page.get("ResourceTagMappingList", []):
            total += 1
            arn = resource["ResourceARN"]
            tags = {tag["Key"]: tag["Value"] for tag in resource.get("Tags", [])}
            missing = tuple(key for key in REQUIRED_TAGS if key not in tags)
            invalid = tuple(
                key
                for key in REQUIRED_TAGS
                if key in tags and tags[key] not in ALLOWED_VALUES[key]
            )
            if missing or invalid:
                violations.append(
                    TagViolation(
                        resource_arn=arn,
                        service=service_from_arn(arn),
                        missing=missing,
                        invalid=invalid,
                    )
                )
    return TagAudit(total, total - len(violations), tuple(violations))


def list_portfolios(service_catalog_client: Any) -> list[dict[str, Any]]:
    """Return locally owned and shared portfolios with their products."""
    portfolios: dict[str, dict[str, Any]] = {}
    for operation in (
        service_catalog_client.list_portfolios,
        service_catalog_client.list_accepted_portfolio_shares,
    ):
        request = {}
        while True:
            response = operation(**request)
            for portfolio in response.get("PortfolioDetails", []):
                portfolios[portfolio["Id"]] = portfolio
            token = response.get("NextPageToken")
            if not token:
                break
            request["PageToken"] = token

    result = []
    for portfolio_id, portfolio in sorted(
        portfolios.items(), key=lambda item: item[1].get("DisplayName", "")
    ):
        products = []
        request = {"PortfolioId": portfolio_id}
        while True:
            response = service_catalog_client.search_products_as_admin(**request)
            products.extend(
                detail["ProductViewSummary"]
                for detail in response.get("ProductViewDetails", [])
            )
            token = response.get("NextPageToken")
            if not token:
                break
            request["PageToken"] = token
        result.append(
            {
                "portfolio_id": portfolio_id,
                "display_name": portfolio.get("DisplayName", "Unnamed"),
                "products": [
                    {
                        "name": product.get("Name", "Unnamed"),
                        "owner": product.get("Owner", "Unknown"),
                        "type": product.get("Type", "Unknown"),
                    }
                    for product in products
                ],
            }
        )
    return result


def governance_summary(audit: TagAudit) -> dict[str, Any]:
    by_service = Counter(item.service for item in audit.violations)
    return {
        "total_scanned": audit.total_scanned,
        "compliant": audit.compliant,
        "violation_count": len(audit.violations),
        "violations_by_service": dict(sorted(by_service.items())),
        "violations": [asdict(item) for item in audit.violations],
    }


def write_governance_report(
    s3_client: Any,
    bucket: str,
    audit: TagAudit,
    report_date: date | None = None,
) -> str:
    """Store the read-only audit result as encrypted JSON."""
    report_date = report_date or date.today()
    key = f"tag-audit/{report_date:%Y-%m-%d}.json"
    body = json.dumps(governance_summary(audit), indent=2, default=list).encode("utf-8")
    s3_client.put_object(
        Bucket=bucket,
        Key=key,
        Body=body,
        ContentType="application/json",
        ServerSideEncryption="AES256",
    )
    return f"s3://{bucket}/{key}"


def apply_environment_tag(
    tagging_client: Any,
    resource_arns: list[str],
    environment: str,
    approved: bool = False,
) -> Mapping[str, Any]:
    """Apply a reviewed Environment value only after explicit approval."""
    if not approved:
        raise PermissionError("Tag changes require explicit approval")
    if environment not in ALLOWED_VALUES["Environment"]:
        raise ValueError("Environment is not in the approved value set")
    return tagging_client.tag_resources(
        ResourceARNList=resource_arns,
        Tags={"Environment": environment},
    )
