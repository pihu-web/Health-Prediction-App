import sqlite3

conn = sqlite3.connect("database.db")

conn.execute("""
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    dob TEXT NOT NULL,
    email TEXT NOT NULL,
    glucose REAL,
    haemoglobin REAL,
    cholesterol REAL,
    remarks TEXT
)
""")

conn.commit()
conn.close()

print("Database Created Successfully")