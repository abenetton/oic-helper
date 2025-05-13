from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget
from oic_tools import OICHost

class HostPicker(QWidget):
    """Host Picker component for selecting hosts."""

    def __init__(self, hosts: list[OICHost], parent=None):
        super().__init__(parent)
        self.hosts = hosts

        # Main layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Labels for selected hosts
        self.label_host_1 = QLabel("Host 1: -")
        self.label_host_2 = QLabel("Host 2: -")
        self.layout.addWidget(self.label_host_1)
        self.layout.addWidget(self.label_host_2)

        # List widgets for host selection
        self.list_host_1 = QListWidget()
        self.list_host_2 = QListWidget()
        self.layout.addWidget(self.list_host_1)
        self.layout.addWidget(self.list_host_2)

        # Populate the lists
        self.populate_host_lists()

        # Connect signals
        self.list_host_1.currentRowChanged.connect(self.update_host_1)
        self.list_host_2.currentRowChanged.connect(self.update_host_2)

    def populate_host_lists(self):
        """Populate the host selection lists."""
        for host in self.hosts:
            self.list_host_1.addItem(f"{host.label} ({host.id})")
            self.list_host_2.addItem(f"{host.label} ({host.id})")

    def update_host_1(self, index):
        """Update the label for Host 1."""
        if index >= 0:
            self.label_host_1.setText(f"Host 1: {self.list_host_1.item(index).text()}")

    def update_host_2(self, index):
        """Update the label for Host 2."""
        if index >= 0:
            self.label_host_2.setText(f"Host 2: {self.list_host_2.item(index).text()}")
