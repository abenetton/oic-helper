from textual.reactive import reactive
from textual.widgets import Tree

from Config import Config
from oic_tools.OICClient import OICClient
from oic_tools.OICPackage import OICPackage


class HostNavigator(Tree):
    host_id = reactive("Ajeje")
    load_all_packages = reactive(True)

    def __init__(self, id, config: Config) -> None:
        super().__init__(id=id, label="Ajeje")
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
            packages: list[OICPackage] = []

            if self.load_all_packages:
                oic_client = OICClient(host)
                packages_tmp = oic_client.get_all_packages()

                # Split packages into two lists, one for those with name in config and one for those not
                packages_in_config = [pkg for pkg in packages_tmp if pkg.pid in self.config.packages]
                packages_not_in_config = [pkg for pkg in packages_tmp if pkg.pid not in self.config.packages]

                # Join the two lists keeping the packages in config first and sorting individual lists by name
                packages = sorted(packages_in_config, key=lambda x: x.name) + sorted(packages_not_in_config,
                                                                                     key=lambda x: x.name)
            else:
                packages = [OICPackage(package, package, 0) for package in sorted(self.config.packages)]

            for package in packages:
                self.root.add(f"{package.name} ({package.integration_num})")
        else:
            self.root.add("No packages available")

        self.parent.set_loading(False)  # TODO: NOT WORKING
