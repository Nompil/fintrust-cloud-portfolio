from fintrust_utils import (
    format_rand,
    mask_id_number,
    validate_id_number,
    calculate_monthly_fee,
    summarise_transactions,
    generate_report_header
)

# Formatting
print(format_rand(45230.75))
print(mask_id_number("8501015009084"))

# Validation
print(validate_id_number("8501015009084"))
print(validate_id_number("123"))

# Monthly Fees
print(calculate_monthly_fee("savings"))
print(calculate_monthly_fee("credit"))

# Transaction Summary
amounts = [
    5000,
    -250,
    1200,
    -800,
    3500,
    -1500
]

deposits, withdrawals, net = summarise_transactions(
    amounts
)

print(f"In: {format_rand(deposits)}")
print(f"Out: {format_rand(abs(withdrawals))}")
print(f"Net: {format_rand(net)}")

# Report Header
print(
    generate_report_header(
        "Thabo Nkosi",
        "ACC-10042"
    )
)