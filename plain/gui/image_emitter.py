# from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
# import sqlite3

# class ImageEmitter(QObject):
#     # Define a signal that can be emitted to add an image
#     add_image_signal = pyqtSignal(str, bytes)  # Assuming image name and binary data

#     def __init__(self):
#         super().__init__()

#     def emit_add_image(self, image_name, image_data):
#         # Emit the signal with the image name and data
#         self.add_image_signal.emit(image_name, image_data)

# class DatabaseHandler(QObject):
#     def __init__(self, db_path):
#         super().__init__()
#         self.db_path = db_path
#         self.init_db()

#     def init_db(self):
#         # Initialize the database connection and create table if not exists
#         with sqlite3.connect(self.db_path) as conn:
#             cursor = conn.cursor()
#             cursor.execute('''
#                 CREATE TABLE IF NOT EXISTS images (
#                     id INTEGER PRIMARY KEY,
#                     name TEXT NOT NULL,
#                     data BLOB NOT NULL
#                 )
#             ''')
#             conn.commit()

#     @pyqtSlot(str, bytes)
#     def add_image(self, image_name, image_data):
#         # Slot to add an image to the database
#         with sqlite3.connect(self.db_path) as conn:
#             cursor = conn.cursor()
#             cursor.execute('INSERT INTO images (name, data) VALUES (?, ?)', (image_name, image_data))
#             conn.commit()
#             print(f"Image '{image_name}' added to database.")

# # Create instances
# emitter = ImageEmitter()
# db_handler = DatabaseHandler('images.db')

# # Connect the signal to the slot
# emitter.add_image_signal.connect(db_handler.add_image)

# # Emit the signal to add an image
# image_name = 'example.png'
# image_data = b'\x89PNG\r\n\x1a\n...'  # Example binary data for a PNG image
# emitter.emit_add_image(image_name, image_data)
