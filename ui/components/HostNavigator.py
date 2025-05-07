from textual.binding import Binding
from textual.reactive import reactive
from textual.widgets import Tree

from Config import Config
from oic_tools import OICHost


class HostNavigator(Tree):
    BINDINGS = [
        Binding("a", "show_all", "Show all packages")
    ]

    load_all_packages = reactive(False)
    priority_packages_sort = reactive(True)
    hosts: reactive[dict[str, OICHost]] = reactive({})

    def __init__(self, config: Config) -> None:
        super().__init__("Tree root")
        self.show_root = False
        self.root.add_leaf("No packages loaded")
        self.config = config
        self.hosts = config.hosts

    def watch_hosts(self, hosts: dict[str, OICHost]) -> None:
        """Watch for changes to the hosts property and update the tree."""
        self.log(f"Hosts changed to: {hosts}")
        self.root.remove_children()
        self.root.expand()

        # Add all hosts from config to the tree
        if hosts:
            for host in hosts.values():
                host_node = self.root.add(host.label)
                # Add packages under each host
                for package_id in host.get_sorted_package_ids(priority_packages_sort=self.priority_packages_sort):
                    package = host.packages.get(package_id)
                    if package:
                        host_node.add(f"{package.name} ({package.integration_num})")
                    else:
                        host_node.add_leaf(f"Unknown package: {package_id}")
        else:
            self.root.add_leaf("No hosts available")

    def action_show_all(self) -> None:
        """Show all packages."""
        self.load_all_packages = not self.load_all_packages
        self.log(f"Showing all packages toggled, new value is: {self.load_all_packages}")
        self.root.add("Loading all packages...")
