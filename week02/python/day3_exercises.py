"""Week 2 Day 3 Python fundamentals exercises for FinTrust Bank."""

from decimal import Decimal


def format_account_summary(customer_name, account_type, balance):
    """Return a display-ready account summary."""
    d_balance = Decimal(str(balance))
    return (
        f"Customer: {customer_name.title()}\n"
        f"Account:  {account_type.upper()}\n"
        f"Balance:  R {d_balance:,.2f}\n"
        f"Status:   ACTIVE"
    )


def calculate_compound_interest(principal, annual_rate, years, n=12):
    """Return the final amount and interest earned, rounded to cents."""
    principal_value = Decimal(str(principal))
    rate = Decimal(str(annual_rate))
    periods = Decimal(n)
    final_amount = principal_value * (Decimal("1") + rate / periods) ** (n * years)
    final_amount = final_amount.quantize(Decimal("0.01"))
    interest_earned = final_amount - principal_value
    return final_amount, interest_earned


def transaction_statistics(transactions):
    """Calculate the five statistics required by Exercise 3."""
    amounts = [Decimal(str(value)) for value in transactions]
    total = sum(amounts, Decimal("0"))
    return {
        "total": total,
        "average": total / len(amounts),
        "largest": max(amounts),
        "smallest": min(amounts),
        "above_5000": sum(value > Decimal("5000") for value in amounts),
    }


def main():
    print("Exercise 1")
    print(format_account_summary("thabo nkosi", "savings", "52750.00"))

    print("\nExercise 2")
    amount, interest = calculate_compound_interest("50000.00", "0.085", 3)
    print(f"After 3 years: R {amount:,.2f} (interest earned: R {interest:,.2f})")

    transactions = [
        "250.00", "12500.00", "750.50", "88000.00", "1200.00",
        "3450.00", "55000.00", "125.00", "9800.00",
    ]
    stats = transaction_statistics(transactions)
    print("\nExercise 3")
    print(f"Total: R {stats['total']:,.2f}")
    print(f"Average: R {stats['average']:,.2f}")
    print(f"Largest: R {stats['largest']:,.2f}")
    print(f"Smallest: R {stats['smallest']:,.2f}")
    print(f"Transactions above R5 000: {stats['above_5000']}")


if __name__ == "__main__":
    main()
