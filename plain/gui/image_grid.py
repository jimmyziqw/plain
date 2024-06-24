from PyQt6.QtWidgets import QLabel, QPushButton, QGridLayout, QSizePolicy, QScrollArea, QFrame
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QTimer, pyqtSlot
class ImageGridWidget(QFrame):
    def __init__(self, image_paths, image_size=100, spacing=5):
        super().__init__()
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.image_paths = image_paths
        self.image_size = image_size
        self.spacing = spacing
        self.init_ui()
        self.setup_timers()

    def init_ui(self):
        # Ensure size policy allows for ignoring size constraints
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.populate_images()

    def setup_timers(self):
        # Throttle timer for resize event
        self.resize_timer = QTimer()
        self.resize_timer.setSingleShot(True)
        self.resize_timer.timeout.connect(self.populate_images)

    def crop_center(self, pixmap):
        width = pixmap.width()
        height = pixmap.height()
        if width > height:
            x_offset = (width - height) // 2
            y_offset = 0
            side_length = height
        else:
            x_offset = 0
            y_offset = (height - width) // 2
            side_length = width
        return pixmap.copy(x_offset, y_offset, side_length, side_length)

    def populate_images(self):
        self.clear_layout()
        num_cols = self.images_per_row()
        for i, image_path in enumerate(self.image_paths):
            label = self.create_image_label(image_path)
            self.layout.addWidget(label, i // num_cols, i % num_cols)
        self.layout.setHorizontalSpacing(self.spacing)
        self.layout.setVerticalSpacing(self.spacing)

    def clear_layout(self):
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def images_per_row(self):
        available_width = self.width() - self.spacing
        return max(1, available_width // (self.image_size + self.spacing))

    def create_image_label(self, image_path):
        pixmap = QPixmap(image_path)
        cropped_pixmap = self.crop_center(pixmap)
        label = QLabel()
        label.setPixmap(cropped_pixmap.scaled(self.image_size, self.image_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        label.setFixedSize(self.image_size, self.image_size)
        return label

    def set_image_size(self, size):
        self.image_size = size
        self.populate_images()

