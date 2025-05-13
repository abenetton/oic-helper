from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget
import sys
from ui.screens.explore_screen import ExploreScreen
from ui.screens.compare_screen import CompareScreen
from functools import partial

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OIC Helper Tool")

        # Create buttons for "Explore" and "Compare"
        explore_button = QPushButton("Explore")
        compare_button = QPushButton("Compare")

        # Connect buttons to their respective methods
        explore_button.clicked.connect(partial(self.open_screen, "explore"))
        compare_button.clicked.connect(partial(self.open_screen, "compare"))

        # Layout to hold the buttons
        layout = QVBoxLayout()
        layout.addWidget(explore_button)
        layout.addWidget(compare_button)

        # Central widget
        self.main_menu_widget = QWidget()
        self.main_menu_widget.setLayout(layout)
        self.setCentralWidget(self.main_menu_widget)

    def open_screen(self, screen_type):
        if screen_type == "explore":
            self.setCentralWidget(ExploreScreen(self.return_to_main))
        elif screen_type == "compare":
            self.setCentralWidget(CompareScreen(self.return_to_main))

    def return_to_main(self):
        self.setCentralWidget(self.main_menu_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())