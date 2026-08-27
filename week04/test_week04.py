"""Checks for the Week 4 Python exercises and transaction pipeline."""

import copy
import tempfile
import unittest
from pathlib import Path

import pipeline
from python import debug_me, transactions


class PipelineTests(unittest.TestCase):
    def test_source_rows_and_validation(self):
        valid_rows, invalid_rows = pipeline.load_csv(pipeline.CSV_FILE)
        self.assertEqual(len(valid_rows), 8)
        self.assertEqual(len(invalid_rows), 2)
        self.assertEqual(
            {item["row"]["transaction_id"] for item in invalid_rows},
            {"TXN-004", "TXN-006"},
        )

    def test_database_is_idempotent_and_report_is_complete(self):
        valid_rows, _ = pipeline.load_csv(pipeline.CSV_FILE)
        with tempfile.TemporaryDirectory(prefix="fintrust-week04-") as temporary:
            temp_dir = Path(temporary)
            connection = pipeline.setup_database(temp_dir / "test.db")
            try:
                self.assertEqual(
                    pipeline.insert_transactions(connection, valid_rows),
                    (8, 0),
                )
                self.assertEqual(
                    pipeline.insert_transactions(connection, valid_rows),
                    (0, 8),
                )
                account_to = connection.execute(
                    "SELECT account_to FROM transactions "
                    "WHERE transaction_id = 'TXN-003'"
                ).fetchone()[0]
                self.assertIsNone(account_to)

                report = pipeline.generate_report(
                    connection,
                    temp_dir / "daily_report.txt",
                )
            finally:
                connection.close()

            self.assertIn("Total transactions : 8", report)
            self.assertIn("Total volume       : ZAR 16,996.49", report)
            self.assertIn("BREAKDOWN BY TYPE", report)
            self.assertIn("BREAKDOWN BY STATUS", report)
            self.assertIn("#1  TXN-008", report)


class ExceptionTests(unittest.TestCase):
    def setUp(self):
        self.original_accounts = copy.deepcopy(transactions.ACCOUNTS)
        transactions.AUDIT_LOG.clear()

    def tearDown(self):
        transactions.ACCOUNTS.clear()
        transactions.ACCOUNTS.update(self.original_accounts)
        transactions.AUDIT_LOG.clear()

    def test_specific_transaction_errors_are_raised_and_logged(self):
        with self.assertRaises(transactions.InvalidAmountError):
            transactions.process_withdrawal("T1", "FT-001234", -1)
        with self.assertRaises(transactions.AccountFrozenError):
            transactions.process_withdrawal("T2", "FT-005678", 100)
        with self.assertRaises(transactions.DailyLimitExceededError):
            transactions.process_withdrawal("T3", "FT-009999", 2000)
        with self.assertRaises(transactions.CurrencyMismatchError):
            transactions.process_withdrawal("T4", "FT-001234", 10, "USD")
        self.assertEqual(len(transactions.AUDIT_LOG), 4)


class DebuggingLabTests(unittest.TestCase):
    def setUp(self):
        self.original_accounts = copy.deepcopy(debug_me.ACCOUNTS)

    def tearDown(self):
        debug_me.ACCOUNTS.clear()
        debug_me.ACCOUNTS.update(self.original_accounts)

    def test_fee_and_balance_calculation(self):
        self.assertEqual(debug_me.calculate_fee(200), 5.0)
        result = debug_me.process_payment("FT-001", "FT-002", 200)
        self.assertEqual(result["sender_new_balance"], 9795.0)
        self.assertEqual(debug_me.ACCOUNTS["FT-002"]["balance"], 700.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
