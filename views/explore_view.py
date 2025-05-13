from PySide6.QtWidgets import QVBoxLayout, QLabel, QListWidget, QPushButton
from .base_view import BaseView
from controllers.explore_controller import ExploreController
from models.explore_model import ExploreModel

class ExploreView(BaseView):
    def __init__(self, back_callback):
        super().__init__("Explore Feature", back_callback)

        # Use the layout from BaseView instead of creating a new one
        self.host_list = QListWidget()
        self.layout().addWidget(self.host_list)

        # Add a confirm button below the list
        self.confirm_button = QPushButton("Confirm Selection")
        self.confirm_button.clicked.connect(self.confirm_selection)
        self.layout().addWidget(self.confirm_button)

        # Connect the list widget's selection change signal to enable/disable the confirm button
        self.host_list.itemSelectionChanged.connect(self.update_confirm_button_state)

        # Initially disable the confirm button
        self.confirm_button.setEnabled(False)

        # Initialize model and controller
        self.model = ExploreModel()
        self.controller = ExploreController(self.model, self)

        # Populate the list with hosts after initializing the controller
        self.populate_host_list()

    def populate_host_list(self):
        hosts = self.controller.get_hosts()
        self.host_list.clear()
        for host in hosts:
            self.host_list.addItem(f"{host.label} ({host.id})")

    def confirm_selection(self):
        selected_items = self.host_list.selectedItems()
        if selected_items:
            selected_host = selected_items[0].text()
            print(f"Selected host: {selected_host}")
        else:
            print("No host selected.")

    def update_confirm_button_state(self):
        # Enable the confirm button only if an item is selected
        self.confirm_button.setEnabled(bool(self.host_list.selectedItems()))
