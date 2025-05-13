from PySide6.QtWidgets import QVBoxLayout, QLabel, QListWidget, QPushButton, QTreeWidget, QTreeWidgetItem, QListWidgetItem
from .base_view import BaseView
from controllers.explore_controller import ExploreController
from models.explore_model import ExploreModel
from oic_tools.OICPackage import OICPackage
from oic_tools.OICIntegration import OICIntegration
from PySide6.QtCore import Qt

class ExploreView(BaseView):
    def __init__(self, back_callback):
        super().__init__("Explore Feature", back_callback)

        # Use the layout from BaseView
        self.host_list = QListWidget()
        self.layout().addWidget(self.host_list)

        # Tree widget to display packages and integrations
        self.package_tree = QTreeWidget()
        self.package_tree.setHeaderLabels(["Package", "Integration"])
        self.layout().addWidget(self.package_tree)

        # Add a confirm button below the host list
        self.confirm_button = QPushButton("Confirm Host Selection")
        self.confirm_button.clicked.connect(self.confirm_selection)
        self.layout().addWidget(self.confirm_button)

        # Connect signals
        self.host_list.itemSelectionChanged.connect(self.update_confirm_button_state)

        # Initialize model and controller
        self.model = ExploreModel()
        self.controller = ExploreController(self.model, self)

        # Populate the host list
        self.populate_host_list()

        # Initially disable the confirm button
        self.confirm_button.setEnabled(False)

    def populate_host_list(self):
        hosts = self.controller.get_hosts()
        self.host_list.clear()
        for host in hosts.values():
            item = QListWidgetItem(host.label)
            item.setData(Qt.UserRole, host.id)
            self.host_list.addItem(item)

    def confirm_selection(self):
        selected_items = self.host_list.selectedItems()
        if selected_items:
            selected_host_id = selected_items[0].data(Qt.UserRole)
            print(f"Selected host: {selected_host_id}")
            self.populate_package_tree(selected_host_id)
            self.package_tree.setFocus()  # Focus on the package tree after confirming
        else:
            print("No host selected.")

    def populate_package_tree(self, host_label):
        packages = self.controller.get_packages_for_host(host_label)
        self.package_tree.clear()
        for package in packages:
            package_item = QTreeWidgetItem([package.name])
            self.package_tree.addTopLevelItem(package_item)
            integrations = self.controller.get_integrations_for_package(package.name)
            for integration in integrations:
                integration_item = QTreeWidgetItem([integration.name])
                package_item.addChild(integration_item)

    def update_confirm_button_state(self):
        self.confirm_button.setEnabled(bool(self.host_list.selectedItems()))
