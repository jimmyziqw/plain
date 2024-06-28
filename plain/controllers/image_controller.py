from PyQt6.QtCore import QObject, pyqtSlot
import os
class ImageController(QObject):
    def __init__(self, model, view):
        super().__init__()
        self.model = model
        self.view = view

        self.view.image_grid.add_image_signal.connect(self.add_image)
        self.view.image_grid.read_file_metadata_signal.connect(self.read_file_metadata)

        self.meta_container = self.view.right_sidebar
        self.meta_container.tag_container.add_tag_signal.connect(self.add_tag)

    @pyqtSlot(str)
    def add_image(self, file_path):
        print('[controller] add image')
        self.model.add_image(file_path)

    @pyqtSlot(str)
    def read_file_metadata(self, image_path):
        local_path = os.path.basename(image_path)
        self.current_image = image_path
      
        image_metadata = self.model.db_handler.read_image_metadata(local_path)
        self.current_image_id = image_metadata["id"]
        image_tags = self.model.db_handler.find_tags_by_image_id(image_metadata["id"])
        
        print('image_tag', image_tags)
        if image_metadata:
            self.view.right_sidebar.metadata.update_metadata(image_metadata)
            self.view.right_sidebar.tag_container.read_tags(image_tags)
        #TODO: send notification if null
        print("[controller] reading filedata")

    @pyqtSlot(str)
    def add_tag(self, tag):
        print('[controller] add tag')
        self.model.add_tag(self.current_image_id, tag)

    def get_model(self):
        return self.model
