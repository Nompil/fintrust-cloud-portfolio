import importlib.util
import sqlite3
import sys
import tempfile
from pathlib import Path

from fintrust_pipeline.database import insert_transactions, setup_database
from fintrust_pipeline.loader import load_csv
from fintrust_pipeline.reporter import generate_report


BASE_DIR = Path(__file__).resolve().parent


def main() -> None:
    valid_rows, invalid_rows = load_csv(BASE_DIR / "transactions.csv")
    assert len(valid_rows) == 8, f"Expected 8 valid rows, got {len(valid_rows)}"
    assert len(invalid_rows) == 2, f"Expected 2 invalid rows, got {len(invalid_rows)}"

    with tempfile.TemporaryDirectory(prefix="fintrust-smoke-") as temporary:
        work_dir = Path(temporary)
        db_path = work_dir / "fintrust_analytics.db"
        report_path = work_dir / "daily_report.txt"

        connection = setup_database(db_path)
        inserted, skipped = insert_transactions(connection, valid_rows)
        assert (inserted, skipped) == (8, 0)

        inserted_again, skipped_again = insert_transactions(connection, valid_rows)
        assert (inserted_again, skipped_again) == (0, 8)

        row_count = connection.execute(
            "SELECT COUNT(*) FROM transactions"
        ).fetchone()[0]
        assert row_count == 8

        report = generate_report(connection, report_path)
        connection.close()
        assert "Total transactions : 8" in report
        assert report_path.exists()

        if importlib.util.find_spec("pandas") is not None:
            from analyse import analyse_transactions

            enriched_path = work_dir / "transactions_enriched.csv"
            analyse_transactions(db_path, enriched_path)
            assert enriched_path.exists()
            with enriched_path.open(encoding="utf-8") as output:
                assert output.readline().startswith("transaction_id,")
            print("Smoke tests passed: core pipeline and pandas analysis.")
        else:
            print("Smoke tests passed: core pipeline.")
            print(
                "Pandas analysis was skipped. Install week04/requirements.txt "
                "to validate the optional analysis step."
            )


if __name__ == "__main__":
    try:
        main()
    except (AssertionError, sqlite3.Error) as error:
        print(f"Smoke test failed: {error}", file=sys.stderr)
        raise SystemExit(1) from error
