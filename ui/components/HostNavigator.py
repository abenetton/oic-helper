from textual.reactive import reactive
from textual.reactive import reactive
from textual.widgets import Tree

from Config import Config


class HostNavigator(Tree):

    host_id = reactive("Ajeje")

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
            self.set_loading(True)
            for package in sorted(self.config.packages):
                self.root.add(package)
            self.set_loading(False)
        else:
            self.root.add("No packages available")

    # def compose(self) -> ComposeResult:
    #     """Compose the UI elements for the HostNavigator."""
    #     tree: Tree[str] = Tree("Dune")
    #     tree.root.expand()
    #     characters = tree.root.add("Characters", expand=True)
    #     characters.add_leaf("Paul")
    #     characters.add_leaf("Jessica")
    #     characters.add_leaf("Chani")
    #     yield tree
