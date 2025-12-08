import sqlite3

conn = sqlite3.connect('db/ecotrack.sqlite')
cursor = conn.cursor()

# Get all table schemas
cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table' ORDER BY name")
tables = cursor.fetchall()

for name, sql in tables:
    print(f"\n=== {name} ===")
    print(sql)

conn.close()
