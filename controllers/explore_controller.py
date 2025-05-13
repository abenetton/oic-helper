from typing import List
from models.explore_model import ExploreModel
from oic_tools.OICHost import OICHost
from oic_tools.OICPackage import OICPackage
from oic_tools.OICIntegration import OICIntegration

class ExploreController:
    def __init__(self, model: ExploreModel, view):
        self.model = model
        self.view = view

    def handle_action(self):
        # Example action handler
        print("Action handled in ExploreController")

    def get_hosts(self) -> List[OICHost]:
        return self.model.fetch_hosts()

    def get_packages_for_host(self, host_label: str) -> List[OICPackage]:
        # Fetch packages for the given host
        host = self.model.config.hosts[host_label] if host_label in self.model.config.hosts else None
        if host:
            ids = host.get_sorted_package_ids(priority_packages_only=True)
            return [host.packages[package_id] for package_id in ids]
        return []

    def get_integrations_for_package(self, package_name: str) -> List[OICIntegration]:
        # Fetch integrations for the given package
        package = next((pkg for pkg in self.model.data if pkg.name == package_name), None)
        if package:
            return package.get_integrations()  # Assuming OICPackage has a method to fetch integrations
        return []
