from PyQt6.QtCore import QAbstractTableModel, Qt, QModelIndex, QVariant
from models.image_ops import get_image_metadata
class ImageTableModel(QAbstractTableModel):
    def __init__(self, db_handler):
        super().__init__()
        self.db_handler = db_handler
        self.headers = ['ID', 'Name']
        self.images = []
        self.load_images()

    def load_images(self):
        self.images = self.db_handler.get_all_images()
        self.layoutChanged.emit()

    def add_image(self, file_path):
        print('[model] add imaged triggered')
        image_metadata = get_image_metadata(file_path)
        self.db_handler.add_image(image_metadata)
        self.load_images()
    
    def add_tag(self, image_id, tag):
        self.db_handler.add_tag(image_id, tag)


    def rowCount(self, parent=QModelIndex()):
        return len(self.images)

    def columnCount(self, parent=QModelIndex()):
        return len(self.headers)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return QVariant()
        return self.images[index.row()][index.column()]

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.headers[section]
        return QVariant()
