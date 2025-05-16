from typing import List, Tuple

from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QTreeWidget, QTreeWidgetItem

from controllers.compare_controller import CompareController
from models.compare_model import CompareModel
from oic_tools import OICHost, OICIntegration
from .base_view import BaseView


class CompareView(BaseView):
    def __init__(self, back_callback):
        super().__init__("Compare Feature", back_callback)

        compare_layout = QVBoxLayout()
        self.layout().addLayout(compare_layout)

        host_selector_layout = QHBoxLayout()
        compare_layout.addLayout(host_selector_layout)
        host_selector_layout.addWidget(QLabel("Host 1:"))
        # Add a dropdown or list for host selection
        self.host1_dropdown = QComboBox()
        host_selector_layout.addWidget(self.host1_dropdown)
        host_selector_layout.addWidget(QLabel("Host 2:"))
        self.host2_dropdown = QComboBox()
        host_selector_layout.addWidget(self.host2_dropdown)
        self.compare_button = QPushButton("Compare")
        self.compare_button.clicked.connect(self.compare_host_action)
        host_selector_layout.addWidget(self.compare_button)
        self.generate_report = QPushButton("Generate report")
        self.generate_report.clicked.connect(self.generate_report_action)
        self.generate_report.setDisabled(True)
        host_selector_layout.addWidget(self.generate_report)

        host_selector_layout.setStretch(0, 1)
        host_selector_layout.setStretch(1, 2)
        host_selector_layout.setStretch(2, 1)
        host_selector_layout.setStretch(3, 2)
        host_selector_layout.setStretch(4, 1)

        # Tree widget to display packages and integrations
        self.package_tree = QTreeWidget()
        self.package_tree.setHeaderLabels(["Integration", "Host1", "Host2", "Note"])
        compare_layout.addWidget(self.package_tree)

        self.package_tree.setColumnWidth(0, self.package_tree.width() * 5 // 12)  # First column takes 1/2
        self.package_tree.setColumnWidth(1, self.package_tree.width() * 3 // 12)  # First column takes 1/2
        self.package_tree.setColumnWidth(2, self.package_tree.width() * 3 // 12)  # First column takes 1/2
        self.package_tree.setColumnWidth(3, self.package_tree.width() * 1 // 12)  # Second column takes 1/4

        # Initialize model and controller
        self.model = CompareModel()  # TODO: Move this to the controller
        self.controller = CompareController(self.model, self)

        self.host1_dropdown.currentIndexChanged.connect(self.on_host1_changed)


    def update_host_list(self, is_host1: bool, host_list: list[OICHost]):

        host_dropdown: QComboBox = self.host1_dropdown if is_host1 else self.host2_dropdown

        # Clear existing items in the dropdowns
        host_dropdown.clear()

        # Load all hosts from the model
        for host in host_list:
            host_dropdown.addItem(host.label, host)

        # Set the default selection to the first host
        if host_dropdown.count() > 0:
            host_dropdown.setCurrentIndex(0)

    def on_host1_changed(self, index):
        # Disable the single selected host item in the second dropdown
        self.controller.update_host2(self.host1_dropdown.itemData(index))

    def set_selected_host(self, is_host1: bool, host: OICHost):
        if is_host1:
            self.host1_dropdown.setCurrentText(host.label)
        else:
            self.host2_dropdown.setCurrentText(host.label)

    def compare_host_action(self):
        host1: OICHost = self.host1_dropdown.currentData()
        host2: OICHost = self.host2_dropdown.currentData()
        self.generate_report.setDisabled(False)
        if host1 and host2:
            self.controller.compare_hosts(host1, host2)
        else:
            # Handle the case where one of the hosts is not selected. Should never happen
            raise ValueError("Both hosts must be selected for comparison.")

    def update_package_tree(self, package_list: List[Tuple[str, List[OICIntegration.OICCompare]]]):
        self.package_tree.clear()

        for package_name, integrations in package_list:
            package_item = QTreeWidgetItem([
                package_name
            ])
            self.package_tree.addTopLevelItem(package_item)
            package_item.setExpanded(True)

            for integration in integrations:
                integration_item = QTreeWidgetItem([
                    integration.name,
                    f"{integration.host1_version[0]} - {integration.host1_version[1]}",
                    f"{integration.host2_version[0]} - {integration.host2_version[1]}" if integration.host2_version else "N/A",
                    integration.result.value
                ])
                package_item.addChild(integration_item)

    def generate_report_action(self):
        self.generate_report.setDisabled(True)
        self.controller.generate_report()
        self.generate_report.setDisabled(False)