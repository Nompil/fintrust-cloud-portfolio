"""Compare the service costs used in the FinTrust file migration case."""

from __future__ import annotations

import math
from decimal import Decimal, ROUND_HALF_UP


def currency(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def compare_transfer_costs(
    data_tb: Decimal | str,
    datasync_per_gb: Decimal | str = "0.0125",
    snowball_capacity_tb: Decimal | str = "80",
    snowball_device_cost: Decimal | str = "600",
    snowball_labour_each: Decimal | str = "100",
    snowball_request_cost: Decimal | str = "1500",
    direct_connect_hours: Decimal | str = "1320",
    direct_connect_hourly: Decimal | str = "0.30",
    daily_delta_tb: Decimal | str = "10",
    delta_days: int = 30,
) -> dict[str, Decimal | int]:
    """Return visible cost components for DataSync, Snowball and hybrid paths."""
    size = Decimal(data_tb)
    capacity = Decimal(snowball_capacity_tb)
    if size <= 0 or capacity <= 0 or delta_days < 0:
        raise ValueError("Data size and device capacity must be positive")
    devices = math.ceil(size / capacity)
    data_gb = size * Decimal(1000)
    datasync_service = data_gb * Decimal(datasync_per_gb)
    direct_connect = Decimal(direct_connect_hours) * Decimal(direct_connect_hourly)
    datasync_total = datasync_service + direct_connect
    snowball_total = (
        Decimal(devices) * (Decimal(snowball_device_cost) + Decimal(snowball_labour_each))
        + Decimal(snowball_request_cost)
    )
    delta_gb = Decimal(daily_delta_tb) * Decimal(1000) * Decimal(delta_days)
    hybrid_total = snowball_total + delta_gb * Decimal(datasync_per_gb)
    return {
        "device_count": devices,
        "datasync_service_usd": currency(datasync_service),
        "direct_connect_port_usd": currency(direct_connect),
        "datasync_total_usd": currency(datasync_total),
        "snowball_total_usd": currency(snowball_total),
        "hybrid_total_usd": currency(hybrid_total),
    }
