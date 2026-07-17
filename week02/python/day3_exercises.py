"""
Week 2 Day 3
Python Fundamentals Exercises
FinTrust Banking Scenario
"""

from decimal import Decimal


# ==================================================
# Exercise 1 - Account Formatter
# ==================================================

def format_account_summary(customer_name, account_type, balance):
    """
    Return a formatted customer account summary.
    """

    d_balance = Decimal(str(balance))

    return (
        f"Customer: {customer_name.title()}\n"
        f"Account:  {account_type.upper()}\n"
        f"Balance:  R {d_balance:,.2f}\n"
        f"Status:   ACTIVE"
    )


print("==== Exercise 1 ====")
print(
    format_account_summary(
        "thabo nkosi",
        "savings",
        52750.00
    )
)
print()


# ==================================================
# Exercise 2 - Compound Interest Calculator
# ==================================================

def calculate_compound_interest(
        principal,
        annual_rate,
        years,
        n=12):
    """
    Calculate compound interest.

    A = P(1 + r/n)^(nt)
    """

    p = float(principal)

    amount = p * (1 + annual_rate / n) ** (n * years)

    interest_earned = amount - p

    return (
        Decimal(str(round(amount, 2))),
        Decimal(str(round(interest_earned, 2)))
    )


print("==== Exercise 2 ====")

principal = Decimal("50000.00")

amount, interest = calculate_compound_interest(
    principal,
    0.085,
    3
)

print(
    f"After 3 years: "
    f"R {amount:,.2f} "
    f"(interest earned: R {interest:,.2f})"
)
print()


# ==================================================
# Exercise 3 - Transaction Statistics
# ==================================================

transactions = [
    Decimal("250.00"),
    Decimal("12500.00"),
    Decimal("750.50"),
    Decimal("88000.00"),
    Decimal("1200.00"),
    Decimal("3450.00"),
    Decimal("55000.00"),
    Decimal("125.00"),
    Decimal("9800.00")
]

total = sum(transactions)

average = total / len(transactions)

largest = max(transactions)

smallest = min(transactions)

count_above_5000 = len(
    [transaction for transaction in transactions
     if transaction > Decimal("5000")]
)

print("==== Exercise 3 ====")
print(f"Total: R {total:,.2f}")
print(f"Average: R {average:,.2f}")
print(f"Largest: R {largest:,.2f}")
print(f"Smallest: R {smallest:,.2f}")
print(f"Transactions above R5000: {count_above_5000}")
