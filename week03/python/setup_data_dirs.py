"""
setup_data_dirs.py

Sets up the FinTrust data directory structure
and reports directory contents.

Usage:
    python setup_data_dirs.py [base_dir]
"""

import sys
import os
from pathlib import Path
from datetime import date


def setup_directories(base_dir):
    """Create standard FinTrust data directories."""

    directories = [
        base_dir / "transactions" / "current",
        base_dir / "transactions" / "archive",
        base_dir / "statements" / str(date.today().year),
        base_dir / "reports" / "monthly",
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"Created: {directory}")

    return directories


def report_directory(base_dir):
    """Display directory summary."""

    all_items = list(base_dir.rglob("*"))

    files = [item for item in all_items if item.is_file()]
    directories = [item for item in all_items if item.is_dir()]

    print("\nDirectory Report")
    print("-" * 40)
    print(f"Location       : {base_dir.resolve()}")
    print(f"Directories    : {len(directories)}")
    print(f"Files          : {len(files)}")

    if files:
        total_size = sum(file.stat().st_size for file in files)

        print(f"Total Size     : {total_size:,} bytes")

        print("\nFiles Found:")

        for file in sorted(files):
            print(
                f"  {file.relative_to(base_dir)} "
                f"({file.stat().st_size:,} bytes)"
            )


def main():
    """
    Determine base directory from:
    1. Command-line argument
    2. Environment variable
    3. Default value
    """

    if len(sys.argv) > 1:
        base_dir = Path(sys.argv[1])

    else:
        base_dir = Path(
            os.environ.get(
                "FINTRUST_DATA_DIR",
                "data/fintrust"
            )
        )

    print(
        f"Setting up FinTrust data directories in: "
        f"{base_dir}"
    )

    setup_directories(base_dir)

    report_directory(base_dir)

    print("\nSetup complete.")

    sys.exit(0)


if __name__ == "__main__":
    main()