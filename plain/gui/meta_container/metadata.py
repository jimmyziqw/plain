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

    def update_metadata(self, metadata):
        self.format_label.setText(f"Format: {metadata['file_format']}")
        self.pixels_label.setText(f"Pixels: {metadata['width']}x{metadata['height']}")
        self.date_created_label.setText(f"Date Created: {metadata['timestamp_created']}")
        self.date_modified_label.setText(f"Date Modified: {metadata['timestamp_modified']}")