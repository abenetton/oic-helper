from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from Config import Config
from ui.components.HostNavigator import HostNavigator

class ExploreScreen(QWidget):
    """Explore screen of the OIC Helper app."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = Config()
        self.config.load_from_file('data/config.json')

        # Main layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Add header
        header = QLabel("Explore Screen")
        self.layout.addWidget(header)

        # Add HostNavigator
        self.host_navigator = HostNavigator(config=self.config)
        self.layout.addWidget(self.host_navigator)
