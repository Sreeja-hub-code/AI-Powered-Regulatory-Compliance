import sqlite3

# Connect to your database
conn = sqlite3.connect("contracts.db")
cur = conn.cursor()

# Show all tables in the DB
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in cur.fetchall()]
print("🗂️ Tables:", tables)

# Optionally, show table structure for 'contracts'
if "contracts" in tables:
    print("\n📋 Schema for contracts table:")
    for row in cur.execute("PRAGMA table_info(contracts)"):
        print(row)

conn.close()
