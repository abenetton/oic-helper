from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox

from controllers.compare_controller import CompareController
from models.compare_model import CompareModel
from oic_tools import OICHost
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
        # self.compare_button.clicked.connect(self.compare_host_action)
        host_selector_layout.addWidget(self.compare_button)

        host_selector_layout.setStretch(0, 1)
        host_selector_layout.setStretch(1, 2)
        host_selector_layout.setStretch(2, 1)
        host_selector_layout.setStretch(3, 2)
        host_selector_layout.setStretch(4, 1)

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