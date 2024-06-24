from PyQt6.QtWidgets import QApplication
from database.db_handler import DatabaseHandler
from models.image_model import ImageTableModel
from controllers.image_controller import ImageController
from views.main_window import MainWindow
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)

    db_handler = DatabaseHandler('images.db')
    model = ImageTableModel(db_handler)
    controller = ImageController(model)
    main_window = MainWindow(controller)
    main_window.show()

    sys.exit(app.exec())
