from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel

class Metadata(QFrame):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        metadata_label = QLabel("Metadata")
        self.format_label = QLabel("Format: JPEG")
        self.pixels_label = QLabel("Pixels: 1920x1080")
        self.date_created_label = QLabel("Date Created: 2024-06-23")
        self.date_modified_label = QLabel("Date Modified: 2024-06-23")

        layout.addWidget(metadata_label)
        layout.addWidget(self.format_label)
        layout.addWidget(self.pixels_label)
        layout.addWidget(self.date_created_label)
        layout.addWidget(self.date_modified_label)

        self.setLayout(layout)
