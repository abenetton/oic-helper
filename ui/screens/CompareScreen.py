from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from Config import Config
from ui.components.HostPicker import HostPicker
from ui.components.HostCompare import HostCompare

class CompareScreen(QWidget):
    """Compare screen of the OIC Helper app."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = Config()
        self.config.load_from_file('data/config.json')
        self.current_widget = None

        # Main layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Initial widget
        self.show_host_list()

    def show_host_list(self):
        """Show the host list."""
        if self.current_widget:
            self.layout.removeWidget(self.current_widget)
            self.current_widget.deleteLater()

        self.current_widget = HostPicker(hosts=[host for host in self.config.hosts.values()])
        self.layout.addWidget(self.current_widget)

        # Add a button to switch to compare view
        compare_button = QPushButton("Compare Hosts")
        compare_button.clicked.connect(self.compare_hosts)
        self.layout.addWidget(compare_button)

    def compare_hosts(self):
        """Compare the selected hosts."""
        if isinstance(self.current_widget, HostPicker):
            selected_hosts = self.current_widget.get_selected_hosts()
            if len(selected_hosts) == 2:
                self.layout.removeWidget(self.current_widget)
                self.current_widget.deleteLater()

                self.current_widget = HostCompare(host1=selected_hosts[0], host2=selected_hosts[1])
                self.layout.addWidget(self.current_widget)
