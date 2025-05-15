from models.explore_model import ExploreModel
from oic_tools.OICHost import OICHost
from oic_tools.OICPackage import OICPackage


class ExploreController:
    def __init__(self, model: ExploreModel, view):
        self.model = model
        self.view = view
        self.host_id = ""
        self.show_only_priority = True

    def populate_host_list(self):
        hosts = self.model.fetch_hosts()
        self.view.display_host_list(hosts)

    def populate_package_tree(self, host_id: str):
        # Fetch packages for the given host
        self.host_id = host_id
        host = self.model.config.hosts[host_id] if host_id in self.model.config.hosts else None
        if not host:
            raise ValueError(f"Host with ID {host_id} not found in config.")
        
        ids = host.get_sorted_package_ids(priority_packages_only=self.show_only_priority)
        packages = [host.packages[package_id] for package_id in ids]

        # Pass data to the view
        self.view.display_package_tree(packages)

    def is_package_prioritary(self, package_id: str) -> bool:
        return package_id in self.model.config.hosts[self.host_id].priority_package_ids

