from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import Header, Footer

from Config import Config
from ui.common.bindings import screen_common_bindings
from ui.components import HostPicker
from ui.components.HostCompare import HostCompare


class CompareScreen(Screen):
    """Compare screen of the OIC Helper app."""
    BINDINGS = screen_common_bindings + [
        Binding("c", "compare", "Compare"),
        Binding("l", "show_list", "Show host list") #TODO: Fix bug that initially shows both bindings
    ]

    def __init__(self, name=None, cid=None, classes=None):
        super().__init__(name, cid, classes)
        self.config = Config()
        self.config.load_from_file('data/config.json')
        self.current_widget_id = 'host_picker'

    def check_action(self, action: str, parameters: tuple[object, ...]) -> bool | None:
        """Check if an action may run."""
        if action == "compare" and self.current_widget_id == "#host_compare":
            return False
        if action == "show_list" and self.current_widget_id == "#host_picker":
            return False

        return True

    def compose(self) -> ComposeResult:
        yield Header()
        yield HostPicker(id="host_picker", hosts=[host for host in self.config.hosts.values()])
        yield Footer()

    def action_compare(self) -> None:
        """Action to compare the selected hosts."""
        self.log("Comparing selected hosts...")
        host_picker = self.query_one("#host_picker", HostPicker)
        selected_hosts = host_picker.get_selected_hosts()
        self.log(f"Selected hosts: {selected_hosts}")
        self.remove_children('#host_picker')
        self.mount(HostCompare(id="host_compare", host1=selected_hosts[0], host2=selected_hosts[1]))
        self.current_widget_id = "#host_compare"
        self.refresh_bindings()

    def action_show_list(self) -> None:
        """Action to show the host list."""
        self.log("Showing host list...")
        self.remove_children('#host_compare')
        self.mount(HostPicker(id="host_picker", hosts=[host for host in self.config.hosts.values()]))
        self.current_widget_id = "#host_picker"
        self.refresh_bindings()

    #def on_mount(self):
    #    self.action_compare()
