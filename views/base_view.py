from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QWidget, QSpacerItem, QSizePolicy

class BaseView(QWidget):
    def __init__(self, title, back_callback):
        super().__init__()
        main_layout = QVBoxLayout()

        # Header layout
        header_layout = QHBoxLayout()

        # Back button
        back_button = QPushButton("Back")
        back_button.clicked.connect(back_callback)
        header_layout.addWidget(back_button)

        # Spacer to center the title
        header_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Title label
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        header_layout.addWidget(title_label)

        # Add another spacer to balance the layout
        header_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        main_layout.addLayout(header_layout)

        # Set the main layout
        self.setLayout(main_layout)
