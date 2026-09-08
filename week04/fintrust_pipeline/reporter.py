"""Build the daily transaction report from SQLite queries."""

from datetime import datetime
from pathlib import Path


def generate_report(connection, report_path):
    """Run four reporting queries and write the formatted result."""
    lines = [
        "=" * 60,
        "FINTRUST DAILY TRANSACTION REPORT",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "=" * 60,
    ]

    summary = connection.execute(
        """
        SELECT
            COUNT(*) AS total_count,
            ROUND(SUM(amount), 2) AS total_volume,
            ROUND(AVG(amount), 2) AS average_amount,
            ROUND(MIN(amount), 2) AS minimum_amount,
            ROUND(MAX(amount), 2) AS maximum_amount
        FROM transactions
        """
    ).fetchone()
    lines.extend(
        [
            "",
            "SUMMARY",
            f"  Total transactions : {summary['total_count']}",
            f"  Total volume       : ZAR {summary['total_volume']:,.2f}",
            f"  Average amount     : ZAR {summary['average_amount']:,.2f}",
            "  Min / Max          : "
            f"ZAR {summary['minimum_amount']:,.2f} / "
            f"ZAR {summary['maximum_amount']:,.2f}",
            "",
            "BREAKDOWN BY TYPE",
        ]
    )

    type_rows = connection.execute(
        """
        SELECT type, COUNT(*) AS count, ROUND(SUM(amount), 2) AS volume
        FROM transactions
        GROUP BY type
        ORDER BY volume DESC
        """
    ).fetchall()
    for row in type_rows:
        lines.append(
            f"  {row['type']:<12}  {row['count']:>3} txns   "
            f"ZAR {row['volume']:>10,.2f}"
        )

    lines.extend(["", "BREAKDOWN BY STATUS"])
    status_rows = connection.execute(
        """
        SELECT status, COUNT(*) AS count, ROUND(SUM(amount), 2) AS volume
        FROM transactions
        GROUP BY status
        ORDER BY count DESC, status
        """
    ).fetchall()
    for row in status_rows:
        lines.append(
            f"  {row['status']:<12}  {row['count']:>3} txns   "
            f"ZAR {row['volume']:>10,.2f}"
        )

    lines.extend(["", "TOP 3 LARGEST TRANSACTIONS"])
    largest_rows = connection.execute(
        """
        SELECT transaction_id, account_from, amount, type, status
        FROM transactions
        ORDER BY amount DESC
        LIMIT 3
        """
    ).fetchall()
    for position, row in enumerate(largest_rows, start=1):
        lines.append(
            f"  #{position}  {row['transaction_id']}  {row['account_from']}  "
            f"ZAR {row['amount']:,.2f}  [{row['type']} / {row['status']}]"
        )

    lines.extend(["", "=" * 60])
    report_text = "\n".join(lines)
    Path(report_path).write_text(report_text + "\n", encoding="utf-8")
    return report_text
