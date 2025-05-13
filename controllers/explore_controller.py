from typing import List
from models.explore_model import ExploreModel
from oic_tools.OICHost import OICHost
from oic_tools.OICPackage import OICPackage
from oic_tools.OICIntegration import OICIntegration

class ExploreController:
    def __init__(self, model: ExploreModel, view):
        self.model = model
        self.view = view
        self.host_id = ""

    def handle_action(self):
        # Example action handler
        print("Action handled in ExploreController")

    def get_hosts(self) -> List[OICHost]:
        return self.model.fetch_hosts()

    def get_packages_for_host(self, host_id: str) -> List[OICPackage]:
        # Fetch packages for the given host
        self.host_id = host_id
        host = self.model.config.hosts[host_id] if host_id in self.model.config.hosts else None
        if host:
            ids = host.get_sorted_package_ids(priority_packages_only=True)
            return [host.packages[package_id] for package_id in ids]
        return []

    def get_integrations_for_package(self, package_name: str) -> List[OICIntegration]:
        # Fetch integrations for the given package
        package = self.model.config.hosts[self.host_id].packages[package_name] if package_name in self.model.config.hosts[self.host_id].packages else None
        if package:
            return package.get_all_integrations().values()
        return []
