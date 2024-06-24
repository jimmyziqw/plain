import sqlite3

class ImageDatabase:
    
    def __init__(self, db_name='image_manager.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.setup_schema()

    def setup_schema(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT NOT NULL,
            filename TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            meta TEXT,  -- JSON or TEXT field to store any additional metadata
            note TEXT   -- User note
        );
        ''')

        # Create tags Table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        );
        ''')

        # Create image_tags Table (Many-to-Many Relationship)
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

    def add_image(self, path, filename, meta, note):
        self.cursor.execute('''
        INSERT INTO images (path, filename, meta, note)
        VALUES (?, ?, ?, ?)
        ''', (path, filename, meta, note))
        self.conn.commit()

    def add_tag(self, tag_name):
        self.cursor.execute('''
        INSERT INTO tags (name)
        VALUES (?)
        ON CONFLICT(name) DO NOTHING;
        ''', (tag_name,))
        self.conn.commit()

    def add_image_tag(self, image_name, tag_name):
        self.cursor.execute('''
            INSERT INTO image_tags (image_id, tag_id)
            SELECT images.id, tags.id
            FROM images, tags
            WHERE images.filename = ? AND tags.name = ?
        ''', (image_name, tag_name))
        self.conn.commit()


    def read_image(self, filename):
        self.cursor.execute('''
            SELECT * FROM images WHERE filename = ?
        ''', (filename,))
        image_data = self.cursor.fetchone()
        if image_data:
            image = {
                'id': image_data[0],
                'path': image_data[1],
                'filename': image_data[2],
                'created_at': image_data[3],
                'meta': image_data[4],
                'note': image_data[5]
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
    def _print_flat_table(self):
        self.cursor.execute('''
            SELECT images.*
            FROM images
            JOIN image_tags ON images.id = image_tags.image_id
            JOIN tags ON image_tags.tag_id = tags.id
        ''')
        results = self.cursor.fetchall()
        return results

    def close(self):
        self.conn.close()

# Example usage
if __name__ == "__main__":
    manager = ImageDatabase()

    # Add images
    manager.add_image('/images/photo1.jpg', 'photo1.jpg', '{"resolution": "1920x1080"}', 'This is a sample note')
    manager.add_image('/images/photo2.jpg', 'photo2.jpg', '{"resolution": "1080x720"}', 'Another note')
    manager.add_image('/images/photo3.jpg', 'photo3.jpg', '{"resolution": "2048x1536"}', 'Third note')

    # Add tags
    manager.add_tag('vacation')
    manager.add_tag('family')
    manager.add_tag('landscape')
    manager.add_tag('sunset')

    # Add image-tag relationships
    manager.add_image_tag(1, 1)  # image_id 1 with tag_id 1 (vacation)
    manager.add_image_tag(1, 2)  # image_id 1 with tag_id 2 (family)
    manager.add_image_tag(2, 1)  # image_id 2 with tag_id 1 (vacation)
    manager.add_image_tag(2, 3)  # image_id 2 with tag_id 3 (landscape)
    manager.add_image_tag(3, 4)  # image_id 3 with tag_id 4 (sunset)
    manager.add_image_tag(3, 3)  # image_id 3 with tag_id 3 (landscape)

    # Query images by tag
    print("images tagged with 'vacation':")
    print(manager.get_images_by_tag('vacation'))

    # Query tags by image
    print("tags for image 1:")
    print(manager.get_tags_by_image(1))

    # Close the connection
    manager.close()
