from models.explore_model import ExploreModel


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

    def load_integrations_for_package(self, package_id: str):
        # Fetch integrations for the given package
        host = self.model.config.hosts[self.host_id]
        package = host.packages[package_id]
        if not package.integrations_loaded:
            package.get_all_integrations()
            # Reload the package tree to show the integrations
            self.populate_package_tree(self.host_id) # TODO: This is a workaround, find a better way to update the tree without reloading
            self.view.expand_tree_package(package_id)