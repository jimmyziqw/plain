from src.database import connect
import sqlite3
conn = sqlite3.connect("tutorial.db")
cursor = conn.cursor()
# cursor.execute("CREATE TABLE movie(title, year, score)")

res = cursor.execute("SELECT name FROM sqlite_master")
res.fetchone()
data = [
    ("Monty Python at the hoooy" ,1982, 7.9),
    ("The meaning of Life", 1983, 7.5),
    ("Life of Brian", 1979, 8.0),
]

cursor.executemany("INSERT INTO movie VALUES(?,?,?)", data)
conn.commit()