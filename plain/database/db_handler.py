import sqlite3

class DatabaseHandler:
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS images (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    data BLOB NOT NULL
                )
            ''')
            conn.commit()

    def add_image(self, image_name, image_data):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO images (name, data) VALUES (?, ?)', (image_name, image_data))
            conn.commit()

    def get_all_images(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, name FROM images')
            return cursor.fetchall()
