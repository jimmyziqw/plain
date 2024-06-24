from PyQt6.QtWidgets import QApplication, QVBoxLayout, QPushButton, QTreeView, QFrame, QSplitter, QWidget, QGroupBox
from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtCore import Qt, QDir

class Sidebar(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create a QSplitter for collapsible sections
        splitter = QSplitter(Qt.Orientation.Vertical)
        layout.addWidget(splitter)

        # File System Section
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.rootPath())

        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(QDir.rootPath()))
        self.tree.setColumnWidth(0, 250)

        file_system_group = QGroupBox("File System")
        file_system_layout = QVBoxLayout()
        file_system_layout.addWidget(self.tree)
        file_system_group.setLayout(file_system_layout)

        # Tag Section
        tag_group = QGroupBox("Tag")
        tag_layout = QVBoxLayout()
        tag_button = QPushButton("Tag")
        tag_layout.addWidget(tag_button)
        tag_group.setLayout(tag_layout)

        # Untagged Section
        untagged_group = QGroupBox("Untagged")
        untagged_layout = QVBoxLayout()
        untagged_button = QPushButton("Untagged")
        untagged_layout.addWidget(untagged_button)
        untagged_group.setLayout(untagged_layout)

        # Add groups to the splitter
        splitter.addWidget(file_system_group)
        splitter.addWidget(tag_group)
        splitter.addWidget(untagged_group)
        splitter.setSizes([200, 100, 100])  # Initial sizes