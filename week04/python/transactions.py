"""Custom banking exceptions used by the FinTrust transaction lab."""

from datetime import datetime


class BankingError(Exception):
    """Base class for FinTrust banking errors."""


class TransactionError(BankingError):
    """Base class for errors raised while processing one transaction."""

    def __init__(self, txn_id, message):
        self.txn_id = txn_id
        super().__init__(f"[TXN:{txn_id}] {message}")


class InsufficientFundsError(TransactionError):
    def __init__(self, txn_id, account_id, requested, available):
        self.account_id = account_id
        self.requested = requested
        self.available = available
        self.shortfall = requested - available
        super().__init__(
            txn_id,
            f"Account {account_id} is short by R{self.shortfall:.2f}",
        )


class AccountFrozenError(TransactionError):
    def __init__(self, txn_id, account_id, reason):
        self.account_id = account_id
        self.reason = reason
        super().__init__(txn_id, f"Account {account_id} is frozen: {reason}")


class InvalidAmountError(TransactionError):
    def __init__(self, txn_id, amount):
        self.amount = amount
        super().__init__(txn_id, f"Invalid amount: R{amount:.2f}")


class DailyLimitExceededError(TransactionError):
    def __init__(self, txn_id, account_id, limit, used, requested):
        self.account_id = account_id
        self.limit = limit
        self.used = used
        self.requested = requested
        remaining = limit - used
        super().__init__(
            txn_id,
            f"Daily limit R{limit:.2f}, used R{used:.2f}, "
            f"remaining R{remaining:.2f}, requested R{requested:.2f}",
        )


class CurrencyMismatchError(TransactionError):
    def __init__(self, txn_id, transaction_currency, account_currency):
        self.transaction_currency = transaction_currency
        self.account_currency = account_currency
        super().__init__(
            txn_id,
            f"Transaction currency {transaction_currency} does not match "
            f"account currency {account_currency}",
        )


ACCOUNTS = {
    "FT-001234": {
        "balance": 3200.50,
        "currency": "ZAR",
        "frozen": False,
        "daily_used": 0.0,
        "daily_limit": 10000.0,
    },
    "FT-005678": {
        "balance": 50000.00,
        "currency": "ZAR",
        "frozen": True,
        "daily_used": 0.0,
        "daily_limit": 50000.0,
        "freeze_reason": "POPIA compliance hold",
    },
    "FT-009999": {
        "balance": 1500.00,
        "currency": "ZAR",
        "frozen": False,
        "daily_used": 8500.0,
        "daily_limit": 10000.0,
    },
}

AUDIT_LOG = []


def log_transaction_error(error):
    """Record a structured entry for a transaction failure."""
    AUDIT_LOG.append(
        {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "txn_id": error.txn_id,
            "error_type": type(error).__name__,
            "message": str(error),
        }
    )


def process_withdrawal(txn_id, account_id, amount, currency="ZAR"):
    """Process one withdrawal or raise a specific transaction error."""
    try:
        if amount <= 0:
            raise InvalidAmountError(txn_id, amount)
        if account_id not in ACCOUNTS:
            raise TransactionError(txn_id, f"Account {account_id} not found")

        account = ACCOUNTS[account_id]
        if currency != account["currency"]:
            raise CurrencyMismatchError(
                txn_id,
                currency,
                account["currency"],
            )
        if account["frozen"]:
            raise AccountFrozenError(
                txn_id,
                account_id,
                account.get("freeze_reason", "Frozen"),
            )
        if account["daily_used"] + amount > account["daily_limit"]:
            raise DailyLimitExceededError(
                txn_id,
                account_id,
                account["daily_limit"],
                account["daily_used"],
                amount,
            )
        if amount > account["balance"]:
            raise InsufficientFundsError(
                txn_id,
                account_id,
                amount,
                account["balance"],
            )

        account["balance"] -= amount
        account["daily_used"] += amount
        return {
            "txn_id": txn_id,
            "account_id": account_id,
            "amount": amount,
            "currency": currency,
            "new_balance": account["balance"],
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "status": "SUCCESS",
        }
    except TransactionError as error:
        log_transaction_error(error)
        raise


def run_examples():
    cases = [
        ("TXN001", "FT-001234", 100.00, "ZAR"),
        ("TXN002", "FT-001234", 5000.00, "ZAR"),
        ("TXN003", "FT-005678", 500.00, "ZAR"),
        ("TXN004", "FT-009999", 2000.00, "ZAR"),
        ("TXN005", "FT-001234", -50.00, "ZAR"),
        ("TXN006", "FT-001234", 50.00, "USD"),
    ]

    for txn_id, account_id, amount, currency in cases:
        try:
            result = process_withdrawal(
                txn_id,
                account_id,
                amount,
                currency,
            )
            print(
                f"SUCCESS: {txn_id}  "
                f"New balance = R{result['new_balance']:.2f}"
            )
        except TransactionError as error:
            print(f"FAILED: {error}")

    print("\nAudit log")
    for entry in AUDIT_LOG:
        print(
            f"{entry['timestamp']}  {entry['txn_id']}  "
            f"{entry['error_type']}  {entry['message']}"
        )


if __name__ == "__main__":
    run_examples()
