from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QLineEdit, QPushButton
from gui.meta_container.flow_layout import FlowLayout

class Tags(QFrame):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)       
        # tags_label = QLabel("Tags")
        self.flow_layout = FlowLayout()
        self.add_tag_input = QLineEdit()
        self.add_tag_input.setPlaceholderText("Add new tag")
        self.add_tag_button = QPushButton("Add Tag")
        self.add_tag_button.clicked.connect(self.add_tag)

        layout.addLayout(self.flow_layout)
        layout.addWidget(self.add_tag_input)
        layout.addWidget(self.add_tag_button)

        self.setLayout(layout)

    def add_tag(self):
        new_tag = self.add_tag_input.text().strip()
        if new_tag and new_tag not in self.tags:
            self.tags.append(new_tag)
            self.add_tag_button_widget(new_tag)
            self.add_tag_input.clear()

    def add_tag_button_widget(self, tag):
        tag_button = QPushButton(tag)
        tag_button.setStyleSheet("margin: 2px; padding: 5px;")
        tag_button.clicked.connect(lambda: self.remove_tag(tag, tag_button))
        self.flow_layout.addWidget(tag_button)

    def remove_tag(self, tag, button):
        self.tags.remove(tag)
        self.flow_layout.removeWidget(button)
        button.deleteLater()
