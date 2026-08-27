"""Corrected version of the Week 4 payment debugging exercise."""

ACCOUNTS = {
    "FT-001": {
        "balance": 10000.0,
        "daily_limit": 5000.0,
        "daily_used": 0.0,
        "frozen": False,
    },
    "FT-002": {
        "balance": 500.0,
        "daily_limit": 2000.0,
        "daily_used": 0.0,
        "frozen": False,
    },
    "FT-003": {
        "balance": 25000.0,
        "daily_limit": 10000.0,
        "daily_used": 0.0,
        "frozen": True,
    },
}


def calculate_fee(amount):
    """Calculate a 0.5 percent fee with a minimum of R5.00."""
    return max(amount * 0.005, 5.0)


def check_daily_limit(account, amount):
    """Return whether the payment fits within the remaining daily limit."""
    remaining = account["daily_limit"] - account["daily_used"]
    return amount <= remaining


def process_payment(sender_id, receiver_id, amount):
    if sender_id not in ACCOUNTS:
        raise ValueError(f"Sender {sender_id} not found")
    if receiver_id not in ACCOUNTS:
        raise ValueError(f"Receiver {receiver_id} not found")

    sender = ACCOUNTS[sender_id]
    receiver = ACCOUNTS[receiver_id]
    if sender["frozen"]:
        raise RuntimeError(f"Sender account {sender_id} is frozen")
    if not check_daily_limit(sender, amount):
        raise RuntimeError(f"Daily limit exceeded for {sender_id}")

    fee = calculate_fee(amount)
    total_deducted = amount + fee
    if total_deducted > sender["balance"]:
        raise RuntimeError(f"Insufficient funds in {sender_id}")

    sender["balance"] -= total_deducted
    sender["daily_used"] += amount
    receiver["balance"] += amount
    return {
        "sender": sender_id,
        "receiver": receiver_id,
        "amount": amount,
        "fee": fee,
        "sender_new_balance": sender["balance"],
    }


def run_demo():
    payments = [
        ("FT-001", "FT-002", 200.0),
        ("FT-001", "FT-002", 300.0),
        ("FT-002", "FT-001", 100.0),
        ("FT-003", "FT-001", 500.0),
    ]

    results = []
    for sender, receiver, amount in payments:
        try:
            result = process_payment(sender, receiver, amount)
            results.append(result)
            print(
                f"PASS {sender} to {receiver}: R{amount:.2f} "
                f"(fee: R{result['fee']:.2f})"
            )
        except RuntimeError as error:
            print(f"FAIL {sender} to {receiver}: {error}")

    total_sent = sum(result["amount"] for result in results)
    failed_count = len(payments) - len(results)
    print(f"\nFT-001 final balance: R{ACCOUNTS['FT-001']['balance']:.2f}")
    print(f"Total processed (excluding failed): R{total_sent:.2f}")
    print(f"Failed payments: {failed_count}")
    return results, failed_count


if __name__ == "__main__":
    run_demo()
