from PySide6.QtWidgets import QVBoxLayout, QLabel, QListWidget
from .base_view import BaseView
from controllers.explore_controller import ExploreController
from models.explore_model import ExploreModel

class ExploreView(BaseView):
    def __init__(self, back_callback):
        super().__init__("Explore Feature", back_callback)

        # Use the layout from BaseView instead of creating a new one
        self.host_list = QListWidget()
        self.layout().addWidget(self.host_list)

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
