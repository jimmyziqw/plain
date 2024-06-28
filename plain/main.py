from PyQt6.QtWidgets import QApplication
from database.image_db import ImageDatabase
from models.image_model import ImageTableModel
from controllers.image_controller import ImageController
from views.main_window import MainWindow
from config import Config
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)

    db = ImageDatabase('images.db')
    model = ImageTableModel(db)
    config = Config()
    print(config.__dict__)
    view = MainWindow(config)
    controller = ImageController(model, view)
    view.show()
    sys.exit(app.exec())
