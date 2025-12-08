import sqlite3

conn = sqlite3.connect('db/ecotrack.sqlite')
cursor = conn.cursor()

# Get all table schemas
print("=== TABLE SCHEMAS ===")
cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")
for row in cursor.fetchall():
    if row[1]:
        print(f"\n-- Table: {row[0]}")
        print(row[1])

# Get data from each table
print("\n\n=== TABLE DATA ===")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")
tables = [row[0] for row in cursor.fetchall()]

for table in tables:
    cursor.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()
    if rows:
        print(f"\n-- Data for {table} ({len(rows)} rows)")
        # Get column names
        cursor.execute(f"PRAGMA table_info({table})")
        columns = [col[1] for col in cursor.fetchall()]
        print(f"-- Columns: {', '.join(columns)}")
        for row in rows[:5]:  # Show first 5 rows
            print(row)
        if len(rows) > 5:
            print(f"... and {len(rows) - 5} more rows")

conn.close()
