from PySide6.QtWidgets import QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem
from Config import Config
from oic_tools import OICHost, OICPackage

class HostNavigator(QWidget):
    """Host Navigator component for exploring hosts and packages."""

    def __init__(self, config: Config, parent=None):
        super().__init__(parent)
        self.config = config
        self.hosts = config.hosts

        # Main layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Tree widget
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Host/Package"])
        self.layout.addWidget(self.tree)

        # Load hosts into the tree
        self.reload_hosts()

    def reload_hosts(self):
        """Reload the hosts and their packages into the tree."""
        self.tree.clear()

        if self.hosts:
            for host in self.hosts.values():
                host_item = QTreeWidgetItem([host.label])
                self.tree.addTopLevelItem(host_item)

                # Add packages under each host
                for package_id in host.get_sorted_package_ids():
                    package_item = QTreeWidgetItem([package_id])
                    host_item.addChild(package_item)
