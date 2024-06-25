import sqlite3
from PIL import Image

class ImageDatabase:
    def __init__(self, db_path='images.db'):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.setup_schema()
        self.db_path = db_path

    def add_image(self, file_info):
        self.cursor.execute('''
        INSERT INTO images (file_path, file_name, file_format,
            timestamp_created, timestamp_modified, file_size, width, height)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (file_info['file_path'], file_info['file_name'], file_info['file_format'], file_info['timestamp_created'], file_info['timestamp_modified'],file_info['file_size'], file_info['width'], file_info['height']))
        self.conn.commit()

    def add_tag(self, tag_name):
        self.cursor.execute('''
        INSERT INTO tags (name)
        VALUES (?)
        ON CONFLICT(name) DO NOTHING;
        ''', (tag_name,))
        self.conn.commit()

    def add_image_tag(self, file_name, tag_name):
        self.cursor.execute('''
            INSERT INTO image_tags (image_id, tag_id)
            SELECT images.id, tags.id
            FROM images, tags
            WHERE images.file_name = ? AND tags.name = ?
        ''', (file_name, tag_name))
        self.conn.commit()

    def read_image_metadata(self, file_path):
        self.cursor.execute('''
            SELECT * FROM images WHERE file_path = ?
        ''', (file_path,))
        image_data = self.cursor.fetchone()
        if image_data:
            print(image_data)
            image = {
                'id': image_data[0],
                'file_path': image_data[1],
                'file_name': image_data[2],
                'timestamp_created': image_data[3],
                'timestamp_modified': image_data[4],
                'file_format': image_data[5],
                'file_size': image_data[6],
                'width': image_data[7],
                'height': image_data[8]
            }
            return image
        else:
            return None

    def find_images_by_tag(self, tag_name):
        try:
            self.cursor.execute('''
                SELECT images.*
                FROM images
                JOIN image_tags ON images.id = image_tags.image_id
                JOIN tags ON image_tags.tag_id = tags.id
                WHERE tags.name = ?
            ''', (tag_name,))
            results = self.cursor.fetchall()
            return results
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return None

    def find_tags_by_image(self, image_id):
        self.cursor.execute('''
        SELECT tags.name
        FROM tags
        JOIN image_tags ON tags.id = image_tags.tag_id
        WHERE image_tags.image_id = ?
        ''', (image_id,))
        results = self.cursor.fetchall()
        return results
   
    def get_all_images(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, file_name FROM images')
            return cursor.fetchall()
    
    def setup_schema(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path TEXT NOT NULL,
            file_name TEXT NOT NULL,
            timestamp_created DATETIME DEFAULT CURRENT_TIMESTAMP,
            timestamp_modified DATETIME DEFAULT CURRENT_TIMESTAMP,
            file_format TEXT,
            file_size INTEGER,
            width INTEGER,
            height INTEGER
        );
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        );
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS image_tags (
            image_id INTEGER,
            tag_id INTEGER,
            FOREIGN KEY (image_id) REFERENCES images (id),
            FOREIGN KEY (tag_id) REFERENCES tags (id),
            PRIMARY KEY (image_id, tag_id)
        );
        ''')

        self.conn.commit()

    def close(self):
        self.conn.close()

# Example usage
if __name__ == "__main__":
    db = ImageDatabase()

    # Add an image with metadata
    file_info = {
        'file_path': '/images/photo1.jpg',
        'file_name': 'photo1.jpg',
        'file_format': 'JPEG',
        'file_size': 17870,
        'width': 1920,
        'height': 1080
    }
    db.add_image(file_info)

    # Add tags
    db.add_tag('vacation')
    db.add_tag('family')
    db.add_tag('landscape')
    db.add_tag('sunset')

    # Add image-tag relationships
    db.add_image_tag('photo1.jpg', 'vacation')
    db.add_image_tag('photo1.jpg', 'family')

    # Query images by tag
    print("Images tagged with 'vacation':")
    images_with_vacation_tag = db.find_images_by_tag('vacation')
    for image in images_with_vacation_tag:
        print(image)

    # Query tags by image
    print("Tags for image ID 1:")
    tags_for_image_1 = db.find_tags_by_image(1)
    for tag in tags_for_image_1:
        print(tag)

    # Close the connection
    db.close()
