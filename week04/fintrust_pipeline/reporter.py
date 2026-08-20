from datetime import datetime


def generate_report(conn, report_path):
    """Query the database and generate a formatted report."""

    lines = []

    lines.append("=" * 60)
    lines.append("FINTRUST DAILY TRANSACTION REPORT")
    lines.append(
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    lines.append("=" * 60)

    row = conn.execute("""
        SELECT
            COUNT(*) AS total_count,
            ROUND(SUM(amount), 2) AS total_volume,
            ROUND(AVG(amount), 2) AS avg_amount,
            ROUND(MIN(amount), 2) AS min_amount,
            ROUND(MAX(amount), 2) AS max_amount
        FROM transactions
    """).fetchone()

    if row["total_count"] == 0:
        lines.append("\nSUMMARY")
        lines.append("  No transactions loaded")
        report_text = "\n".join(lines)
        report_path.write_text(report_text, encoding="utf-8")
        return report_text

    lines.append("\nSUMMARY")
    lines.append(f"  Total transactions : {row['total_count']}")
    lines.append(f"  Total volume       : ZAR {row['total_volume']:,.2f}")
    lines.append(f"  Average amount     : ZAR {row['avg_amount']:,.2f}")
    lines.append(
        f"  Min / Max          : ZAR {row['min_amount']:,.2f} / "
        f"ZAR {row['max_amount']:,.2f}"
    )

    report_text = "\n".join(lines)

    report_path.write_text(
        report_text,
        encoding="utf-8"
    )

    return report_text
