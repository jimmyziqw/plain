from PyQt6.QtWidgets import QMainWindow, QTableView, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QSlider, QScrollArea, QFrame
import sys, os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt, QTimer, pyqtSlot
from gui.sidebar import Sidebar
from gui.image_grid import ImageGridWidget
from gui.meta_container import MetaContainer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        #self.controller = controller
        self.setWindowTitle("Image Management App")
        self.setGeometry(100, 100, 800, 600)
        self.init_ui()

    @pyqtSlot()
    def on_slider_value_changed(self):
        self.throttle_timer.start(100)  # Throttle to 100 milliseconds

    def apply_slider_value(self):
        value = self.slider.value()
        self.image_grid.set_image_size(value)

    # def emit_add_image_signal(self):
    #     # Emit the signal instead of directly calling the method
    #     image_name = 'example.png'
    #     image_data = b'\x89PNG\r\n\x1a\n...'  # Example binary data
    #     self.add_image_signal.emit(image_name, image_data)

    def init_ui(self):
        # Create a central widget and set the layout on it
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        self.sidebar = Sidebar()
        self.right_sidebar = MetaContainer()
        
        base_path = os.path.join(os.path.dirname(__file__), '..', '..','resources', 'images')
        image_paths = [os.path.join(base_path, "ride.jpg"),
                       os.path.join(base_path, "night.jpg"),
                       os.path.join(base_path, "castle.jpg")] * 10  # Populate the same image 30 times
        
        # Ensure images exist
        image_paths = [path for path in image_paths if os.path.exists(path)]

        self.image_grid = ImageGridWidget(image_paths)

        scroll_area = QScrollArea()
        scroll_area.setWidget(self.image_grid)
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.slider_frame = self.create_slider_frame()

        center_layout = QVBoxLayout()
        center_layout.addWidget(scroll_area)
        center_layout.addWidget(self.slider_frame)
        
        main_layout.addWidget(self.sidebar, 1)
        main_layout.addLayout(center_layout, 4)
        main_layout.addWidget(self.right_sidebar, 2)

    def create_slider_frame(self):
        slider_frame = QFrame()
        slider_frame.setFrameShape(QFrame.Shape.NoFrame)
        slider_layout = QVBoxLayout(slider_frame)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(50)
        self.slider.setMaximum(200)
        self.slider.setValue(100)
        self.slider.valueChanged.connect(self.on_slider_value_changed)

        slider_layout.addWidget(self.slider)

        self.throttle_timer = QTimer()
        self.throttle_timer.setSingleShot(True)
        self.throttle_timer.timeout.connect(self.apply_slider_value)

        return slider_frame

