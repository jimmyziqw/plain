import os
import shutil
from PyQt6.QtWidgets import QLabel, QGridLayout, QSizePolicy, QFrame, QFileDialog
from PyQt6.QtGui import QPixmap, QMouseEvent
from PyQt6.QtCore import Qt, QTimer, pyqtSignal

class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event: QMouseEvent):
        self.clicked.emit()
        super().mousePressEvent(event)

class ImageGridWidget(QFrame):
    add_image_signal = pyqtSignal(str)  # Define the signal
    read_file_metadata_signal = pyqtSignal(str) # TODO: swap to id

    def __init__(self, image_paths, image_size=100, spacing=5):
        super().__init__()
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.repo_path = "D:\AFUNFOLDER\plain\plain-desktop\\resources\images"
        self.image_paths = image_paths
        self.image_size = image_size
        self.spacing = spacing
        # self.root_path = os.path.join(os.path.dirname(__file__), '..', '..', 'resources', 'images')
        self.selected_image_path = None  # Track the selected image path
        self.init_ui()
        self.setup_timers()
        
        # Enable drag and drop
        self.setAcceptDrops(True)

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
        label = ClickableLabel()
        label.setPixmap(cropped_pixmap.scaled(self.image_size, self.image_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        label.setFixedSize(self.image_size, self.image_size)

        # Highlight selected image with a cyan border
        if image_path == self.selected_image_path:
            label.setStyleSheet('border: 2px solid cyan;')
        else:
            label.setStyleSheet('border: none;')

        label.clicked.connect(lambda: self.on_image_clicked(image_path))
        return label

    def on_image_clicked(self, file_path):
        self.selected_image_path = file_path
        self.read_file_metadata_signal.emit(file_path)
        self.populate_images()  # Refresh the UI to show the selection
        
    def set_image_size(self, size):
        self.image_size = size
        self.populate_images()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                import_path = url.toLocalFile()
                if os.path.isdir(import_path):
                    self.copy_directory(import_path)
                else:
                    self.copy_file(import_path)
                    local_path = os.path.basename(import_path)
                    self._emit_add_image(os.path.join(self.repo_path, local_path)) 
            self.refresh_image_paths()
            self.populate_images()
            event.acceptProposedAction()
        else:
            super().dropEvent(event)

    def _emit_add_image(self, local_path):
        print(f'image dropped {local_path}')
        #image_data = b'\x89PNG\r\n\x1a\n...'  # Example binary data
        self.add_image_signal.emit(local_path)

    def copy_file(self, file_path):
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            shutil.copy(file_path, self.repo_path)

    def copy_directory(self, dir_path):
        for root, _, files in os.walk(dir_path):
            for file in files:
                self.copy_file(os.path.join(root, file))

    def refresh_image_paths(self):
        self.image_paths = [os.path.join(self.repo_path, file) for file in os.listdir(self.repo_path) if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
