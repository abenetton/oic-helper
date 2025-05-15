from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QListWidget, QPushButton, QTreeWidget, QMenu

from controllers.explore_controller import ExploreController
from models.explore_model import ExploreModel
from .base_view import BaseView


class ExploreView(BaseView):
    def __init__(self, back_callback):
        super().__init__("Explore Feature", back_callback)

        explore_layout = QHBoxLayout()
        self.layout().addLayout(explore_layout)

        selector_layout = QVBoxLayout()
        explore_layout.addLayout(selector_layout)

        self.host_list = QListWidget()
        selector_layout.addWidget(self.host_list)

        # Add a confirm button below the host list
        self.confirm_button = QPushButton("Confirm Host Selection")
        self.confirm_button.clicked.connect(self.confirm_selection_action)
        selector_layout.addWidget(self.confirm_button)

        # Connect signals
        self.host_list.itemSelectionChanged.connect(self.update_confirm_button_state)

        # Tree widget to display packages and integrations
        self.package_tree = QTreeWidget()
        self.package_tree.setHeaderLabels(["Priority", "Integration", "Count", "Version", "Status"])
        explore_layout.addWidget(self.package_tree)

        # Set the column widths for the package tree
        self.package_tree.setColumnWidth(0, self.package_tree.width() * 1 // 12)  # First column takes 1/2
        self.package_tree.setColumnWidth(1, self.package_tree.width() * 6 // 12)  # First column takes 1/2
        self.package_tree.setColumnWidth(2, self.package_tree.width() * 1 // 12)  # First column takes 1/2
        self.package_tree.setColumnWidth(3, self.package_tree.width() * 2 // 12)  # Second column takes 1/4
        self.package_tree.setColumnWidth(4, self.package_tree.width() * 1 // 12)  # Third column takes 1/4
        
        # Control buttons for the package tree
        control_layout = QVBoxLayout()
        explore_layout.addLayout(control_layout)
        control_layout.addWidget(QLabel("View controls"))
        self.show_all_button = QPushButton("Show all")
        self.show_all_button.setDisabled(True)
        self.show_all_button.clicked.connect(self.show_all_action)
        control_layout.addWidget(self.show_all_button)
        control_layout.addWidget(QLabel("Package controls"))
        self.priority_button = QPushButton("Mark as priority")
        self.priority_button.setDisabled(True)
        control_layout.addWidget(self.priority_button)
        control_layout.addWidget(QLabel("Integration controls"))
        self.priority_button = QPushButton("Enable integration")
        self.priority_button.setDisabled(True)
        control_layout.addWidget(self.priority_button)

        # Enable custom context menu for the package tree
        self.package_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.package_tree.customContextMenuRequested.connect(self.show_context_menu)

        # Adjust the stretch factors for the layout
        explore_layout.setStretch(0, 1)  # Host list takes 1/4 of the space
        explore_layout.setStretch(1, 4)  # Package tree takes 3/4 of the space
        explore_layout.setStretch(2, 1)

        # Initialize model and controller
        self.model = ExploreModel()
        self.controller = ExploreController(self.model, self)

        # Populate the host list
        self.controller.populate_host_list()

        # Initially disable the confirm button
        self.confirm_button.setEnabled(False)

    def confirm_selection_action(self):
        selected_items = self.host_list.selectedItems()
        if selected_items:
            selected_host_id = selected_items[0].data(Qt.UserRole)
            print(f"Selected host: {selected_host_id}")
            self.controller.populate_package_tree(selected_host_id)
            self.package_tree.setFocus()  # Focus on the package tree after confirming

            # Enable context buttons
            self.show_all_button.setDisabled(False)
        else:
            print("No host selected.")

    def show_all_action(self):
        pass

    def update_confirm_button_state(self):
        self.confirm_button.setEnabled(bool(self.host_list.selectedItems()))

    def show_context_menu(self, position):
        # Get the item at the clicked position
        item = self.package_tree.itemAt(position)
        if item:
            # Create the context menu
            menu = QMenu()

            version_id = item.data(2, Qt.UserRole)
            if version_id:
                # enable_integration_action = menu.addAction("Enable integration")
                # enable_integration_action.triggered.connect(self.enable_integration)
                # action = menu.exec_(self.package_tree.viewport().mapToGlobal(position))
                return
            
            integration_id = item.data(1, Qt.UserRole)
            if integration_id:
                return

            package_id = item.data(0, Qt.UserRole)
            if package_id:
                is_priority = self.controller.is_package_prioritary(package_id)
                # Add actions to the menu
                mark_priority_action = menu.addAction(["Mark as priority", "Remove from priority"][is_priority])
                mark_priority_action.triggered.connect(self.mark_as_priority)
                # Execute the menu and get the selected action
                action = menu.exec_(self.package_tree.viewport().mapToGlobal(position))
                return

    def mark_as_priority(self, event):
        # Logic to mark the item as priority
        print(f"Marking  as priority")

    def enable_integration(self, event):
        # Logic to enable the integration
        print(f"Enabling integration for ")
