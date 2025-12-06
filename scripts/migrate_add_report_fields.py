"""
Migration script: ensure `environmental_reports` table has `report_type` and `severity` columns.
Run: python scripts/migrate_add_report_fields.py
"""
import os
import sqlite3

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE, 'db', 'ecotrack.sqlite')

if not os.path.exists(DB_PATH):
    print(f"Database file not found at {DB_PATH}")
    raise SystemExit(1)

con = sqlite3.connect(DB_PATH)
cur = con.cursor()

# Get existing columns for environmental_reports
cur.execute("PRAGMA table_info(environmental_reports);")
cols = [row[1] for row in cur.fetchall()]
print('Existing columns:', cols)

changes = []
if 'report_type' not in cols:
    # Add report_type as TEXT, default 'other'
    cur.execute("ALTER TABLE environmental_reports ADD COLUMN report_type TEXT DEFAULT 'other';")
    changes.append('report_type')

if 'severity' not in cols:
    # Add severity as TEXT, default 'Low'
    cur.execute("ALTER TABLE environmental_reports ADD COLUMN severity TEXT DEFAULT 'Low';")
    changes.append('severity')

if changes:
    con.commit()
    print('Added columns:', changes)
else:
    print('No changes needed. Columns already present.')

con.close()