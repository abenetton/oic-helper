from PySide6.QtWidgets import QVBoxLayout, QPushButton, QLabel, QWidget

class BaseScreen(QWidget):
    def __init__(self, title, back_callback):
        super().__init__()
        layout = QVBoxLayout()

        # Title label
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title_label)

        # Back button
        back_button = QPushButton("Back")
        back_button.clicked.connect(back_callback)
        layout.addWidget(back_button)

        self.setLayout(layout)
