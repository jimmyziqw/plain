from PyQt6.QtWidgets import QMainWindow, QTableView, QPushButton, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Image Manager')
        layout = QVBoxLayout()

        self.table_view = QTableView()
        self.table_view.setModel(self.controller.get_model())
        layout.addWidget(self.table_view)

        self.add_button = QPushButton('Add Image')
        self.add_button.clicked.connect(self.add_image)
        layout.addWidget(self.add_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def add_image(self):
        # For simplicity, we'll simulate adding a fixed image
        image_name = 'example.png'
        image_data = b'\x89PNG\r\n\x1a\n...'  # Example binary data
        self.controller.add_image(image_name, image_data)
