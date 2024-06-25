from PyQt6.QtCore import QObject, pyqtSlot

class ImageController(QObject):
    def __init__(self, model, view):
        super().__init__()
        self.model = model
        self.view = view

        self.view.image_grid.add_image_signal.connect(self.add_image)
        self.view.image_grid.read_file_metadata_signal.connect(self.read_file_metadata)

    @pyqtSlot(str)
    def add_image(self, file_path):
        print('[controller] add image')
        self.model.add_image(file_path)

    @pyqtSlot(str)
    def read_file_metadata(self, image_path):
        print(image_path)
        image_metadata = self.model.db_handler.read_image_metadata(image_path)
        
        print(image_metadata)
        if image_metadata:
            self.view.right_sidebar.metadata.update_metadata(image_metadata)
        #TODO: send notification if null
        print("[controller] reading filedata")

    def get_model(self):
        return self.model
