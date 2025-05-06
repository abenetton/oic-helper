from textual.binding import Binding
from textual.reactive import reactive
from textual.widgets import Tree

from Config import Config
from oic_tools.OICClient import OICClient
from oic_tools.OICPackage import OICPackage


class HostNavigator(Tree):
    BINDINGS = [
        Binding("a", "show_all", "Show all packages")
    ]

    host_id = reactive("Ajeje")
    load_all_packages = reactive(False)

    def __init__(self, id, config: Config) -> None:
        super().__init__(id=id, label="Ajeje")
        self.packages = None
        self.package_ids = None
        self.config = config

    def watch_host_id(self, host_id: str) -> None:
        """Watch for changes to the host_id property."""
        self.log(f"Host ID changed to: {host_id}")
        self.border_title = f"Host Navigator - {host_id}"

        # Fetch host data
        host = self.config.hosts.get(host_id)
        self.root.remove_children()
        self.root.set_label(host.label if host else "Unknown Host")
        self.root.expand()

        # Add all packages from config to the tree
        if host:

            if self.load_all_packages:
                oic_client = OICClient(host)
                self.packages = {package.pid: package for package in oic_client.get_all_packages()}
                package_ids = [pkg.pid for pkg in self.packages]

                # Split packages into two lists, one for those with name in config and one for those not
                packages_in_config = [pkg for pkg in package_ids if pkg in self.config.packages]
                packages_not_in_config = [pkg for pkg in package_ids if pkg not in self.config.packages]

                # Join the two lists keeping the packages in config first and sorting individual lists by name
                self.package_ids = sorted(packages_in_config, key=lambda x: x) + sorted(packages_not_in_config,
                                                                                        key=lambda x: x)
            else:
                self.packages = {package: OICPackage(package, package, 0) for package in self.config.packages}
                self.package_ids = sorted(self.config.packages, key=lambda x: x)

            for package_id in self.package_ids:
                self.root.add(f"{self.packages.get(package_id).name} ({self.packages.get(package_id).integration_num})")
        else:
            self.root.add("No packages available")

        self.parent.set_loading(False)  # TODO: NOT WORKING

    def action_show_all(self) -> None:
        """Show all packages."""
        self.log("Showing all packages toggled")
        self.load_all_packages = not self.load_all_packages
