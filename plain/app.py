import sys, os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QSlider, QScrollArea, QFrame
from PyQt6.QtCore import Qt, QTimer, pyqtSlot
from gui.sidebar import Sidebar
from gui.image_grid import ImageGridWidget
from gui.meta_container import MetaContainer
class ImageManagementApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Management App")
        self.setGeometry(100, 100, 800, 600)
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        self.sidebar = Sidebar()
        self.right_sidebar = MetaContainer()
        base_path = os.path.join(os.path.dirname(__file__), '..', 'resources', 'images')
        image_paths = [os.path.join(base_path, "ride.jpg"),
                   os.path.join(base_path, "night.jpg"),
                   os.path.join(base_path, "castle.jpg")] * 10  # Populate the same image 30 times
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


        self.setLayout(main_layout)

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

    @pyqtSlot()
    def on_slider_value_changed(self):
        self.throttle_timer.start(100)  # Throttle to 100 milliseconds

    def apply_slider_value(self):
        value = self.slider.value()
        self.image_grid.set_image_size(value)

def main():
    app = QApplication(sys.argv)
    window = ImageManagementApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
