from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QScrollArea
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication
import sys, os
from gui.sidebar import Sidebar
from gui.image_grid import ImageGridWidget
from gui.meta_container import MetaContainer
from views.image_size_slider import ImageSizeSlider

class MainWindow(QMainWindow):
    def __init__(self, config):
        self.repository_path = config.root_path
        super().__init__()
        self.setWindowTitle("Image Management App")
        self.setGeometry(100, 100, 800, 600)
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        self.left_sidebar = Sidebar()
        self.right_sidebar = MetaContainer()
        
        # base_path = os.path.join(os.path.dirname(__file__), '..', '..','resources', 'images')
        # image_paths = [os.path.join(base_path, "ride.jpg"),
        #                os.path.join(base_path, "night.jpg"),
        #                os.path.join(base_path, "castle.jpg")] * 10  # Populate the same image 30 times
        
        # # Ensure images exist
        # image_paths = [path for path in image_paths if os.path.exists(path)]

        self.image_grid = ImageGridWidget(self.repository_path)

        scroll_area = QScrollArea()
        scroll_area.setWidget(self.image_grid)
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.image_size_slider = ImageSizeSlider()
        self.image_size_slider.set_image_grid(self.image_grid)

        center_layout = QVBoxLayout()
        center_layout.addWidget(scroll_area)
        center_layout.addWidget(self.image_size_slider)
        
        main_layout.addWidget(self.left_sidebar, 1)
        main_layout.addLayout(center_layout, 4)
        main_layout.addWidget(self.right_sidebar, 2)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
