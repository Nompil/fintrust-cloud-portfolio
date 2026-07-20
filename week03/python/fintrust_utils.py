"""
fintrust_utils.py
Shared utilities for FinTrust Bank data processing scripts.
"""

from datetime import date


# -----------------------------
# Formatting
# -----------------------------

def format_rand(amount):
    """Return amount formatted as South African Rand string."""
    return f"R {amount:,.2f}"


def mask_id_number(id_number):
    """Mask middle 6 digits of a 13-digit SA ID number."""
    s = str(id_number)

    if len(s) != 13:
        return s

    return s[:6] + "******" + s[-1]


# -----------------------------
# Validation
# -----------------------------

def validate_id_number(id_number):
    """Return True if id_number is a valid 13-digit numeric SA ID."""

    s = str(id_number)

    return len(s) == 13 and s.isdigit()


def validate_account_type(account_type):
    """Return True if account_type is valid."""

    return account_type in (
        "cheque",
        "savings",
        "credit"
    )


# -----------------------------
# Calculations
# -----------------------------

def calculate_simple_interest(
        principal,
        annual_rate,
        months):
    """Calculate simple interest."""

    return principal * annual_rate * (months / 12)


def calculate_monthly_fee(account_type):
    """Return monthly fee."""

    fees = {
        "savings": 0.00,
        "cheque": 65.00,
        "credit": 120.00
    }

    return fees.get(account_type, 0.00)


def categorise_transaction(amount):
    """Categorise transaction amount."""

    abs_amount = abs(amount)

    if abs_amount < 500:
        return "small"

    elif abs_amount < 5000:
        return "medium"

    return "large"


def summarise_transactions(amounts):
    """
    Returns:
    (deposits, withdrawals, net)
    """

    deposits = sum(a for a in amounts if a > 0)
    withdrawals = sum(a for a in amounts if a < 0)

    return (
        deposits,
        withdrawals,
        deposits + withdrawals
    )


# -----------------------------
# Report Helpers
# -----------------------------

def generate_report_header(
        customer_name,
        account_id):
    """Generate account statement header."""

    today = date.today().strftime("%d %B %Y")

    return (
        f"FinTrust Bank - Account Statement\n"
        f"Customer: {customer_name}\n"
        f"Account: {account_id}\n"
        f"Date: {today}\n"
        f"{'-' * 40}"
    )