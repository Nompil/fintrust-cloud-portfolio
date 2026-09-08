"""Size an offline Snow transfer and compare it with network delivery."""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass


DEVICE_CAPACITY_TB = {
    "Snowcone SSD": 14,
    "Snowball Edge Storage Optimised": 80,
    "Snowball Edge Compute Optimised": 28,
    "Snowmobile": 100_000,
}


@dataclass(frozen=True)
class SnowTransferPlan:
    device: str
    count: int
    data_size_tb: float
    total_capacity_tb: int
    spare_capacity_tb: float
    internet_days: float


def internet_transfer_days(data_size_tb: float, bandwidth_gbps: float) -> float:
    """Calculate ideal transfer days using decimal network units."""
    if data_size_tb <= 0 or bandwidth_gbps <= 0:
        raise ValueError("Data size and bandwidth must be positive")
    seconds = data_size_tb * 8_000 / bandwidth_gbps
    return seconds / 86_400


def plan_snow_transfer(
    data_size_tb: float,
    purpose: str = "archive",
    bandwidth_gbps: float = 1.0,
) -> SnowTransferPlan:
    """Select the appropriate device and calculate the required quantity."""
    if data_size_tb <= 14:
        device = "Snowcone SSD"
    elif data_size_tb >= 10_000:
        device = "Snowmobile"
    elif purpose == "edge-compute":
        device = "Snowball Edge Compute Optimised"
    else:
        device = "Snowball Edge Storage Optimised"
    capacity = DEVICE_CAPACITY_TB[device]
    count = math.ceil(data_size_tb / capacity)
    total = count * capacity
    return SnowTransferPlan(
        device=device,
        count=count,
        data_size_tb=data_size_tb,
        total_capacity_tb=total,
        spare_capacity_tb=round(total - data_size_tb, 1),
        internet_days=round(internet_transfer_days(data_size_tb, bandwidth_gbps), 1),
    )


def main() -> None:
    plan = plan_snow_transfer(3000)
    for key, value in asdict(plan).items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
