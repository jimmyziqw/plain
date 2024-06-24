# from PyQt6.QtWidgets import QPushButton, QHBoxLayout, QLabel, QWidget
# from PyQt6.QtCore import pyqtSignal, QSize, Qt

# class TagButton(QWidget):
#     tag_clicked = pyqtSignal(str)
#     tag_removed = pyqtSignal(str)

#     def __init__(self, tag):
#         super().__init__()
#         self.tag = tag
#         self.init_ui()

#     def init_ui(self):
#         self.setLayout(QHBoxLayout())
#         self.setObjectName("tag_button")

#         self.label = QLabel(self.tag)
#         self.label.setStyleSheet("margin: 2px; padding: 5px;")
        
#         self.delete_button = QLabel(' x')
#         self.delete_button.setStyleSheet("margin-left: 5px; padding: 5px;")
#         self.delete_button.setFixedSize(QSize(16, 16))

#         self.layout().addWidget(self.label)
#         self.layout().addWidget(self.delete_button)
#         self.layout().setContentsMargins(0, 0, 0, 0)
#         self.layout().setSpacing(2)
        
#         self.setStyleSheet("""
#             QWidget#tag_button {
#                 border: 1px solid #ccc;
#                 border-radius: 5px;
#                 background-color: #f0f0f0;
#                 padding: 5px;
#             }
#         """)

#     def mousePressEvent(self, event):
#         # Check if the click was on the delete button
#         if event.button() == Qt.MouseButton.LeftButton and self.childAt(event.pos()) == self.delete_button:
#             self.tag_removed.emit(self.tag)
#         else:
#             self.tag_clicked.emit(self.tag)
#         super().mousePressEvent(event)
