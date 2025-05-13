from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget
from .base_screen import BaseScreen

class CompareScreen(BaseScreen):
    def __init__(self, back_callback):
        super().__init__("Compare Feature", back_callback)
