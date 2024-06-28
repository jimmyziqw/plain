from PyQt6.QtWidgets import QFrame, QVBoxLayout
from gui.meta_container.metadata import Metadata
from gui.meta_container.tag_container import TagContainer

class MetaContainer(QFrame):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.metadata = Metadata()
        self.tag_container = TagContainer()

        layout.addWidget(self.tag_container)
        layout.addWidget(self.metadata)
        self.setLayout(layout)
        self.setFixedWidth(200)  # Set the desired width here

    