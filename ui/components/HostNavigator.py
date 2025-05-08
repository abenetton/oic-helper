from textual import on
from textual.binding import Binding
from textual.reactive import reactive
from textual.widgets import Tree

from Config import Config
from oic_tools import OICHost, OICIntegration, OICPackage


class HostNavigator(Tree):
    BINDINGS = [
        Binding("a", "show_all", "Show all packages"),
        Binding("a", "hide_non_priority", "Show only priority packages"),
        Binding("p", "mark_priority", "Mark as priority"),
        Binding("p", "mark_not_priority", "Mark as non-priority"),
    ]

    load_all_packages = reactive(False)
    hosts: reactive[dict[str, OICHost]] = reactive({})

    def __init__(self, config: Config) -> None:
        super().__init__("Tree root")
        self.show_root = False
        self.root.add_leaf("No packages loaded")
        self.config = config
        self.hosts = config.hosts

    def check_action(self, action: str, parameters: tuple[object, ...]) -> bool | None:
        """Check if an action may run."""
        if action == "show_all" and self.load_all_packages == True:
            return False
        if action == "hide_non_priority" and self.load_all_packages == False:
            return False
        if action == "mark_priority" and self.cursor_node and type(self.cursor_node.data) == OICPackage and self.cursor_node.data.id in self.cursor_node.parent.data.priority_package_ids:
            return False
        if action == "mark_not_priority" and self.cursor_node and type(self.cursor_node.data) == OICPackage and self.cursor_node.data.id not in self.cursor_node.parent.data.priority_package_ids:
            return False
        if action in ["mark_priority", "mark_not_priority"] and self.cursor_node and type(self.cursor_node.data) != OICPackage:
            return None

        return True

    @on(Tree.NodeHighlighted)
    def tree_node_highlighted(self):
        self.refresh_bindings()

    def reload_hosts(self) -> None:
        self.log(f"Hosts changed to: {self.hosts}")
        self.root.remove_children()
        self.root.expand()

        # Add all hosts from config to the tree
        if self.hosts:
            for host in self.hosts.values():
                host_node = self.root.add(label=host.label, data=host)
                # Add packages under each host
                for package_id in host.get_sorted_package_ids(priority_packages_only=not self.load_all_packages):
                    package = host.packages.get(package_id)
                    if package:
                        host_node.add(
                            label=f"{("", "*")[package.id in host.priority_package_ids]} {package.name} ({package.integration_num})",
                            data=package)
                    else:
                        host_node.add_leaf(f"Unknown package: {package_id}")
        else:
            self.root.add_leaf("No hosts available")

    @on(Tree.NodeExpanded)
    def tree_node_expanded(self, event: Tree.NodeExpanded) -> None:
        self.log(f"Node expanded: {event.node.data}")
        if not event.node.children and event.node.data:
            # Load all integrations for the package
            integrations: dict[str, OICIntegration] = event.node.data.get_all_integrations()

            # Regenerate label with integration count
            event.node.label = f"{("", "*")[event.node.data.id in event.node.parent.data.priority_package_ids]} {event.node.data.name} ({event.node.data.integration_num})"

            # Add integrations to the tree
            for integration in integrations.values():
                version = integration.versions[0] if integration.versions else ""
                label = f"{integration.name} - ({version[0]}) - {version[1]}"

                if len(integration.versions) == 1:
                    event.node.add_leaf(label=label, data=integration)
                else:
                    integration_node = event.node.add(label=label, data=integration)
                    for version, status in integration.versions:
                        integration_node.add_leaf(label=f"{version} - {status}", data=integration)

    def action_show_all(self) -> None:
        """Show all packages."""
        self.log("Showing all packages")
        for host in self.hosts.values():
            if not host.packages_loaded:
                host.load_all_packages()
        self.load_all_packages = True
        self.refresh_bindings()

    def action_hide_non_priority(self) -> None:
        """Hide non priority packages."""
        self.log("Hiding non-priority packages")
        self.load_all_packages = False
        self.refresh_bindings()

    def action_mark_priority(self):
        """Mark the selected package as priority."""
        if self.cursor_node and type(self.cursor_node.data) == OICPackage:
            host = self.cursor_node.parent.data
            package = self.cursor_node.data
            host.priority_package_ids.append(package.id)
            host.priority_package_ids.sort()
            self.cursor_node.set_label(f"{("", "*")[package.id in host.priority_package_ids]} {package.name} ({package.integration_num})",)

    def action_mark_not_priority(self):
        """Mark the selected package as non-priority."""
        self.log("Marking package as non-priority")
        if self.cursor_node and type(self.cursor_node.data) == OICPackage:
            self.log(f"Marking package {self.cursor_node.data.name} as non-priority")
            host = self.cursor_node.parent.data
            package = self.cursor_node.data
            host.priority_package_ids.remove(package.id)
            host.priority_package_ids.sort()
            self.cursor_node.set_label(f"{("", "*")[package.id in host.priority_package_ids]} {package.name} ({package.integration_num})",)

    def on_mount(self):
        """Called when the app is mounted."""
        self.watch(self, "hosts", self.reload_hosts)
        self.watch(self, "load_all_packages", self.reload_hosts)
