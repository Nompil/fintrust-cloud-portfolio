"""Pricing and total cost calculations for the FinTrust migration case."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from decimal import Decimal, ROUND_HALF_UP
from typing import Any


REGION_NAMES = {
    "af-south-1": "Africa (Cape Town)",
    "eu-west-1": "Europe (Ireland)",
    "us-east-1": "US East (N. Virginia)",
}


def money(value: Decimal) -> Decimal:
    """Round a currency amount to cents."""
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def get_ec2_ondemand_price(
    pricing_client: Any,
    instance_type: str,
    region: str = "af-south-1",
    operating_system: str = "Linux",
) -> Decimal | None:
    """Return one standard shared-tenancy EC2 On Demand hourly price."""
    if region not in REGION_NAMES:
        raise ValueError(f"Unsupported Pricing API region mapping: {region}")

    response = pricing_client.get_products(
        ServiceCode="AmazonEC2",
        Filters=[
            {"Type": "TERM_MATCH", "Field": "instanceType", "Value": instance_type},
            {"Type": "TERM_MATCH", "Field": "location", "Value": REGION_NAMES[region]},
            {"Type": "TERM_MATCH", "Field": "operatingSystem", "Value": operating_system},
            {"Type": "TERM_MATCH", "Field": "tenancy", "Value": "Shared"},
            {"Type": "TERM_MATCH", "Field": "preInstalledSw", "Value": "NA"},
            {"Type": "TERM_MATCH", "Field": "capacityStatus", "Value": "Used"},
        ],
        MaxResults=1,
    )
    if not response.get("PriceList"):
        return None

    product = response["PriceList"][0]
    if isinstance(product, str):
        product = json.loads(product)
    terms = product["terms"]["OnDemand"]
    term = next(iter(terms.values()))
    dimension = next(iter(term["priceDimensions"].values()))
    return Decimal(dimension["pricePerUnit"]["USD"])


@dataclass(frozen=True)
class SavingsPlanResult:
    commitment_per_hour: Decimal
    ondemand_capacity_per_hour: Decimal
    utilisation_percent: Decimal
    total_ondemand_equivalent: Decimal
    total_commitment_cost: Decimal
    total_saving: Decimal


def calculate_savings_plan_savings(
    hourly_commitment_usd: Decimal | str,
    term_years: int = 3,
    discount_percent: Decimal | str = "66",
    utilisation_percent: Decimal | str = "100",
) -> SavingsPlanResult:
    """Model commitment cost and savings, including unused commitment risk."""
    commitment = Decimal(hourly_commitment_usd)
    discount = Decimal(discount_percent) / Decimal(100)
    utilisation = Decimal(utilisation_percent) / Decimal(100)
    if commitment <= 0:
        raise ValueError("Hourly commitment must be greater than zero")
    if term_years not in {1, 3}:
        raise ValueError("Savings Plans terms are one or three years")
    if not Decimal(0) <= discount < Decimal(1):
        raise ValueError("Discount must be from 0 up to, but not including, 100 percent")
    if not Decimal(0) <= utilisation <= Decimal(1):
        raise ValueError("Utilisation must be between 0 and 100 percent")

    hours = Decimal(term_years * 365 * 24)
    ondemand_capacity = commitment / (Decimal(1) - discount)
    used_ondemand_equivalent = ondemand_capacity * utilisation * hours
    commitment_cost = commitment * hours
    return SavingsPlanResult(
        commitment_per_hour=money(commitment),
        ondemand_capacity_per_hour=money(ondemand_capacity),
        utilisation_percent=money(utilisation * Decimal(100)),
        total_ondemand_equivalent=money(used_ondemand_equivalent),
        total_commitment_cost=money(commitment_cost),
        total_saving=money(used_ondemand_equivalent - commitment_cost),
    )


@dataclass(frozen=True)
class YearlyTcoRow:
    month: int
    on_premises_cost: Decimal
    aws_cost: Decimal
    difference: Decimal


def tco_break_even(
    on_premises_annual_cost: Decimal | str,
    aws_monthly_cost: Decimal | str,
    migration_one_time_cost: Decimal | str,
    on_premises_inflation_percent: Decimal | str = "3",
    months: int = 60,
) -> tuple[int | None, list[YearlyTcoRow]]:
    """Return the first cheaper AWS month and yearly cumulative totals."""
    annual = Decimal(on_premises_annual_cost)
    aws_monthly = Decimal(aws_monthly_cost)
    migration = Decimal(migration_one_time_cost)
    inflation = Decimal(on_premises_inflation_percent) / Decimal(100)
    if min(annual, aws_monthly, migration) < 0 or months < 1:
        raise ValueError("Costs must be non-negative and months must be positive")

    monthly_rate = (Decimal(1) + inflation) ** (Decimal(1) / Decimal(12)) - Decimal(1)
    current_monthly_on_premises = annual / Decimal(12)
    cumulative_on_premises = Decimal(0)
    break_even_month = None
    rows: list[YearlyTcoRow] = []

    for month in range(1, months + 1):
        if month > 1:
            current_monthly_on_premises *= Decimal(1) + monthly_rate
        cumulative_on_premises += current_monthly_on_premises
        cumulative_aws = migration + aws_monthly * month
        if break_even_month is None and cumulative_aws < cumulative_on_premises:
            break_even_month = month
        if month % 12 == 0 or month == months:
            rows.append(
                YearlyTcoRow(
                    month=month,
                    on_premises_cost=money(cumulative_on_premises),
                    aws_cost=money(cumulative_aws),
                    difference=money(cumulative_on_premises - cumulative_aws),
                )
            )
    return break_even_month, rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the FinTrust cost model")
    parser.add_argument("--commitment", default="32.47")
    parser.add_argument("--utilisation", default="100")
    args = parser.parse_args()

    plan = calculate_savings_plan_savings(args.commitment, utilisation_percent=args.utilisation)
    print(json.dumps({key: str(value) for key, value in asdict(plan).items()}, indent=2))
    break_even, rows = tco_break_even("4200000", "248000", "850000")
    print(f"TCO break even month: {break_even}")
    for row in rows:
        print(
            f"Month {row.month:>2}: on premises ${row.on_premises_cost:>12,.2f} | "
            f"AWS ${row.aws_cost:>12,.2f} | difference ${row.difference:>12,.2f}"
        )


if __name__ == "__main__":
    main()
