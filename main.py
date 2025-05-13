from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget, QStackedWidget
import sys
from ui.screens.explore_screen import ExploreScreen
from ui.screens.compare_screen import CompareScreen

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OIC Helper Tool")
        self.resize(800, 600)

        # Create the stacked widget
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Create the main menu widget
        self.main_menu_widget = QWidget()
        layout = QVBoxLayout()
        explore_button = QPushButton("Explore")
        compare_button = QPushButton("Compare")
        explore_button.clicked.connect(lambda: self.open_screen("explore"))
        compare_button.clicked.connect(lambda: self.open_screen("compare"))
        layout.addWidget(explore_button)
        layout.addWidget(compare_button)
        self.main_menu_widget.setLayout(layout)

        # Add widgets to the stack
        self.stack.addWidget(self.main_menu_widget)
        self.explore_screen = ExploreScreen(self.return_to_main)
        self.compare_screen = CompareScreen(self.return_to_main)
        self.stack.addWidget(self.explore_screen)
        self.stack.addWidget(self.compare_screen)

    def open_screen(self, screen_type):
        if screen_type == "explore":
            self.stack.setCurrentWidget(self.explore_screen)
        elif screen_type == "compare":
            self.stack.setCurrentWidget(self.compare_screen)

    def return_to_main(self):
        self.stack.setCurrentWidget(self.main_menu_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())