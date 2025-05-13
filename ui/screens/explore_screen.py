from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget
from .base_screen import BaseScreen

class ExploreScreen(BaseScreen):
    def __init__(self, back_callback):
        super().__init__("Explore Feature", back_callback)
