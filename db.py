# db.py
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("contracts.db")

def get_conn():
    """Connect to the database and return the connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Create tables if they don’t exist."""
    conn = get_conn()
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS contracts (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      filename TEXT,
      filepath TEXT,
      uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    c.execute('''
    CREATE TABLE IF NOT EXISTS analyses (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      contract_id INTEGER,
      result TEXT,
      model TEXT,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY(contract_id) REFERENCES contracts(id)
    )
    ''')
    conn.commit()
    conn.close()

# Run this file directly once to create the database
if __name__ == "__main__":
    init_db()
    print("✅ Database created successfully.")