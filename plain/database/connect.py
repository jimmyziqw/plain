import sqlite3
conn = sqlite3.connect('file_tracker.db')
cursor = conn.cursor()

# Create a table to store file paths and their statuses
cursor.execute('''
CREATE TABLE IF NOT EXISTS files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    path TEXT UNIQUE,
    status TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

conn.commit()
conn.close()
