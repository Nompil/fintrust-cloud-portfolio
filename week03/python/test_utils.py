import unittest
from decimal import Decimal

from fintrust_utils import (
    calculate_monthly_fee,
    calculate_simple_interest,
    categorise_transaction,
    format_rand,
    mask_id_number,
    summarise_transactions,
    validate_account_type,
    validate_id_number,
)
from clean_transactions_v2 import clean_transaction, normalise_date, validate_headers


class FinTrustUtilsTests(unittest.TestCase):
    def test_format_rand(self):
        self.assertEqual(format_rand(Decimal("45230.75")), "R 45,230.75")

    def test_mask_id_number(self):
        self.assertEqual(mask_id_number("8501015009084"), "850101******4")
        self.assertEqual(mask_id_number("123"), "123")

    def test_id_number_shape(self):
        self.assertTrue(validate_id_number("8501015009084"))
        self.assertFalse(validate_id_number("123"))
        self.assertFalse(validate_id_number("850101ABC9084"))

    def test_account_type(self):
        self.assertTrue(validate_account_type("savings"))
        self.assertFalse(validate_account_type("investment"))

    def test_interest_and_fees(self):
        self.assertEqual(calculate_simple_interest(1000, 0.12, 6), 60)
        self.assertEqual(calculate_monthly_fee("savings"), 0)
        self.assertEqual(calculate_monthly_fee("credit"), 120)

    def test_transaction_category(self):
        self.assertEqual(categorise_transaction(100), "small")
        self.assertEqual(categorise_transaction(-2500), "medium")
        self.assertEqual(categorise_transaction(7000), "large")

    def test_transaction_summary(self):
        amounts = [5000, -250, 1200, -800, 3500, -1500]
        self.assertEqual(summarise_transactions(amounts), (9700, -2550, 7150))

    def test_date_normalisation(self):
        self.assertEqual(normalise_date("2026-7-21"), "2026-07-21")
        self.assertEqual(normalise_date("26/07/21"), "2021-07-26")

    def test_invalid_date_is_rejected(self):
        row = {
            "TxID": "1006",
            "AcctID": "104",
            "TYPE": "DEPOSIT",
            "Amount": "100.00",
            "Date": "31/02/2026",
            "Desc": "Deposit",
        }
        with self.assertRaisesRegex(ValueError, "unrecognised date format"):
            clean_transaction(row, 7)

    def test_missing_csv_header_is_rejected(self):
        headers = ["TxID", "AcctID", "TYPE", "Amount", "Date"]
        with self.assertRaisesRegex(ValueError, "CSV header is missing: Desc"):
            validate_headers(headers)


if __name__ == "__main__":
    unittest.main(verbosity=2)
