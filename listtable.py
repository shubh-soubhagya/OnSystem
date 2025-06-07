import sqlite3

DB_PATH = 'system_files.db'

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
conn.close()

print("Tables in DB:")
for t in tables:
    print(t[0])
