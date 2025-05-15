from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTreeWidgetItem, QListWidgetItem

from models.explore_model import ExploreModel
from oic_tools.OICHost import OICHost
from oic_tools.OICPackage import OICPackage
from oic_tools.OICIntegration import OICIntegration
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QListWidget, QPushButton, QTreeWidget, QTreeWidgetItem, QListWidgetItem
from PySide6.QtCore import Qt


class ExploreController:
    def __init__(self, model: ExploreModel, view):
        self.model = model
        self.view = view
        self.host_id = ""

    def populate_host_list(self):
        hosts = self.model.fetch_hosts()
        self.view.host_list.clear()
        for host in hosts.values():
            item = QListWidgetItem(host.label)
            item.setData(Qt.UserRole, host.id)
            self.view.host_list.addItem(item)

    def populate_package_tree(self, host_id: str):
         # Fetch packages for the given host
        self.host_id = host_id
        host = self.model.config.hosts[host_id] if host_id in self.model.config.hosts else None
        if not host:
            raise ValueError(f"Host with ID {host_id} not found in config.")
        
        ids = host.get_sorted_package_ids(priority_packages_only=True)
        packages = [host.packages[package_id] for package_id in ids]

        self.view.package_tree.clear()
        for package in packages:
            integrations = package.get_all_integrations().values()
            package_item = QTreeWidgetItem([("", "X")[self.is_package_prioritary(package.id)], package.name, str(package.integration_num)])
            package_item.setData(0, Qt.UserRole, package.id)
            self.view.package_tree.addTopLevelItem(package_item)
            for integration in integrations:
                integration_item = QTreeWidgetItem(["", integration.name, str(len(integration.versions))])
                integration_item.setData(0, Qt.UserRole, package.id)
                integration_item.setData(1, Qt.UserRole, integration.id)
                package_item.addChild(integration_item)
                for version in integration.versions:
                    version_item = QTreeWidgetItem(["", "", "", version[0], version[1]])
                    version_item.setData(0, Qt.UserRole, package.id)
                    version_item.setData(1, Qt.UserRole, integration.id)
                    version_item.setData(2, Qt.UserRole, version[0])
                    integration_item.addChild(version_item)

    def is_package_prioritary(self, package_id: str) -> bool:
        return package_id in self.model.config.hosts[self.host_id].priority_package_ids

