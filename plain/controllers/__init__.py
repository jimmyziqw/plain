from PyQt6.QtCore import QObject, pyqtSlot

class ImageController(QObject):
    def __init__(self, model):
        super().__init__()
        self.model = model

    @pyqtSlot(str, bytes)
    def add_image(self, image_name, image_data):
        self.model.add_image(image_name, image_data)
