from PyQt6.QtWidgets import QFrame, QVBoxLayout, QSlider
from PyQt6.QtCore import Qt, QTimer, pyqtSlot

class ImageSizeSlider(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setFrameShape(QFrame.Shape.NoFrame)
        slider_layout = QVBoxLayout(self)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(50)
        self.slider.setMaximum(200)
        self.slider.setValue(100)
        self.slider.valueChanged.connect(self.on_slider_value_changed)

        slider_layout.addWidget(self.slider)

        self.throttle_timer = QTimer()
        self.throttle_timer.setSingleShot(True)
        self.throttle_timer.timeout.connect(self.apply_slider_value)

    @pyqtSlot()
    def on_slider_value_changed(self):
        self.throttle_timer.start(100)  # Throttle to 100 milliseconds

    def apply_slider_value(self):
        value = self.slider.value()
        self.parent().image_grid.set_image_size(value)

    def set_image_grid(self, image_grid):
        self.image_grid = image_grid
