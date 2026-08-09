#!/usr/bin/env python3
import sqlite3
import sys
from pathlib import Path

DB = Path('fintrust_analytics.db')
if not DB.exists():
    print('ERROR: fintrust_analytics.db not found in repo root')
    sys.exit(2)

conn = sqlite3.connect(DB)
c = conn.cursor()

print('Database:', DB)

c.execute("SELECT name, type FROM sqlite_master WHERE type IN ('table','view') ORDER BY name")
items = c.fetchall()
if not items:
    print('No tables or views found.')
else:
    for name, typ in items:
        print('\n', typ.upper(), name)
        try:
            cnt = c.execute(f"SELECT COUNT(*) FROM '{name}'").fetchone()[0]
        except Exception as e:
            cnt = f'COUNT ERROR: {e}'
        print('  rows:', cnt)
        try:
            for row in c.execute(f"PRAGMA table_info('{name}')"):
                print('   col:', row)
        except Exception as e:
            print('   schema error:', e)

# show sample rows for tables
for name, typ in items:
    if typ == 'table':
        print('\nSample rows from', name)
        try:
            for r in c.execute(f"SELECT * FROM '{name}' LIMIT 5"):
                print(' ', r)
        except Exception as e:
            print('  sample error:', e)

conn.close()
