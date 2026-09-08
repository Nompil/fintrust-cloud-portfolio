"""Create reviewable FinTrust budget requests and read current utilisation."""

from __future__ import annotations

from decimal import Decimal
from typing import Any, Iterable


def notification(threshold: Decimal | str, notification_type: str, email: str) -> dict[str, Any]:
    """Build one AWS Budgets notification and subscriber pair."""
    if notification_type not in {"ACTUAL", "FORECASTED"}:
        raise ValueError("Notification type must be ACTUAL or FORECASTED")
    value = Decimal(threshold)
    if value <= 0:
        raise ValueError("Threshold must be positive")
    return {
        "Notification": {
            "NotificationType": notification_type,
            "ComparisonOperator": "GREATER_THAN",
            "Threshold": float(value),
            "ThresholdType": "PERCENTAGE",
        },
        "Subscribers": [{"SubscriptionType": "EMAIL", "Address": email}],
    }


def create_monthly_budget(
    budgets_client: Any,
    account_id: str,
    budget_name: str,
    limit_usd: Decimal | str,
    email: str,
    actual_thresholds: Iterable[Decimal | str] = ("80", "90"),
    forecast_threshold: Decimal | str = "100",
) -> None:
    """Create a cost budget with staged actual and forecast notifications."""
    limit = Decimal(limit_usd)
    if limit <= 0:
        raise ValueError("Budget limit must be positive")
    notifications = [notification(value, "ACTUAL", email) for value in actual_thresholds]
    notifications.append(notification(forecast_threshold, "FORECASTED", email))
    budgets_client.create_budget(
        AccountId=account_id,
        Budget={
            "BudgetName": budget_name,
            "BudgetLimit": {"Amount": str(limit), "Unit": "USD"},
            "TimeUnit": "MONTHLY",
            "BudgetType": "COST",
        },
        NotificationsWithSubscribers=notifications,
    )


def describe_budget_usage(budgets_client: Any, account_id: str) -> list[dict[str, Decimal | str]]:
    """Return budget limits, actual spend and percentage used."""
    request: dict[str, Any] = {"AccountId": account_id}
    results = []
    while True:
        response = budgets_client.describe_budgets(**request)
        for item in response.get("Budgets", []):
            limit = Decimal(item["BudgetLimit"]["Amount"])
            actual = Decimal(
                item.get("CalculatedSpend", {}).get("ActualSpend", {}).get("Amount", "0")
            )
            results.append(
                {
                    "name": item["BudgetName"],
                    "limit_usd": limit,
                    "actual_usd": actual,
                    "used_percent": Decimal(0) if limit == 0 else (actual / limit * 100).quantize(Decimal("0.1")),
                }
            )
        token = response.get("NextToken")
        if not token:
            break
        request["NextToken"] = token
    return results
