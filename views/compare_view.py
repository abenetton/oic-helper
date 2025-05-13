from .base_view import BaseView
from PySide6.QtWidgets import QVBoxLayout, QLabel
from controllers.compare_controller import CompareController
from models.compare_model import CompareModel

class CompareView(BaseView):
    def __init__(self, back_callback):
        super().__init__("Compare Feature", back_callback)
        layout = QVBoxLayout()
        label = QLabel("Compare View Content")
        layout.addWidget(label)
        self.setLayout(layout)

        # Initialize model and controller
        self.model = CompareModel()
        self.controller = CompareController(self.model, self)
