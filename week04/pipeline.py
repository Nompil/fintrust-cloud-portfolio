"""
FinTrust CSV to SQLite Pipeline
"""

import csv
import sqlite3
from datetime import datetime
from pathlib import Path

CSV_FILE = Path("week04/transactions.csv")
DB_FILE = Path("week04/fintrust_analytics.db")

VALID_TYPES = {"TRANSFER", "DEPOSIT", "WITHDRAWAL"}
VALID_STATUSES = {"COMPLETED", "FAILED", "PENDING"}
