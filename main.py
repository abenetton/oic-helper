from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QListWidget, QStackedWidget, QWidget
import sys
from ui.screens.screen_list import top_level_screens

class OICHelper(QMainWindow):
    """Main application window for the OIC Helper Tool."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("OIC Helper Tool")

        # Main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Navigation list
        self.nav_list = QListWidget()
        self.layout.addWidget(self.nav_list)

        # Screen container
        self.screen_container = QStackedWidget()
        self.layout.addWidget(self.screen_container)

        # Populate screens
        self.screens = {}
        self.populate_screens()

        # Connect navigation signals
        self.nav_list.currentRowChanged.connect(self.switch_screen)

    def populate_screens(self):
        """Populate the navigation list and screen container with screens."""
        for key, value in top_level_screens.items():
            screen = value.screen()
            self.screens[key] = screen
            self.screen_container.addWidget(screen)
            self.nav_list.addItem(value.label)

    def switch_screen(self, index):
        """Switch to the selected screen."""
        if index < 0 or index >= len(self.screens):
            return
        self.screen_container.setCurrentIndex(index)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OICHelper()
    window.show()
    sys.exit(app.exec())
