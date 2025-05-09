from typing import Tuple

from textual import events, on
from textual.app import ComposeResult
from textual.containers import Container
from textual.reactive import reactive
from textual.widgets import Label, OptionList
from textual.widgets._option_list import Option

from oic_tools import OICHost


class HostPicker(Container):
    host_list: reactive[list[OICHost]] = reactive([])

    def __init__(self, id, hosts: list[OICHost]):
        super().__init__(id=id)
        self.hosts = hosts
        self.selected_index_1 = 0

    def compose(self) -> ComposeResult:
        """Compose the HostPicker widget."""
        yield Label("Host 1", classes="box")
        yield Label("-", id="host_id_1", classes="box")
        yield Label("Host 2", classes="box")
        yield Label("-", id="host_id_2", classes="box")
        yield OptionList(id="host_list_1", classes="host_list")
        yield OptionList(id="host_list_2", classes="host_list")

    def watch_host_list(self, host_list: list[OICHost]) -> None:
        """Watch for changes in the host list and update the option lists."""
        self.host_list = host_list
        # update both host lists
        host_list_1 = self.query_one("#host_list_1", OptionList)
        host_list_2 = self.query_one("#host_list_2", OptionList)
        host_list_1.clear_options()
        host_list_2.clear_options()
        for host in host_list:
            host_list_1.add_option(Option(f"{host.label} ({host.id})", id=host.id))
            host_list_2.add_option(Option(f"{host.label} ({host.id})", id=host.id))

        # set the selected host
        host_list_1.highlighted = 0
        host_list_2.highlighted = 1

    @on(OptionList.OptionHighlighted)
    def highlight_changed(self, event: OptionList.OptionHighlighted) -> None:
        """Handle option highlight change."""
        if event.option_list.id == "host_list_1":
            self.query_one("#host_id_1", Label).update(event.option_id)
            # update the second host list and disable the option selected in the first
            host_2_list = self.query_one("#host_list_2", OptionList)
            host_2_list.enable_option_at_index(self.selected_index_1)
            self.selected_index_1 = event.option_index
            host_2_list.disable_option_at_index(self.selected_index_1)
        elif event.option_list.id == "host_list_2":
            self.query_one("#host_id_2", Label).update(event.option_id)

    def on_mount(self, event: events.Mount) -> None:
        self.watch_host_list(self.hosts)

    def get_selected_hosts(self) -> (OICHost, OICHost):
        """Get the selected hosts from the host lists."""
        host_list_1 = self.query_one("#host_list_1", OptionList)
        host_list_2 = self.query_one("#host_list_2", OptionList)
        selected_host_1: OICHost = self.hosts[host_list_1.highlighted]
        selected_host_2: OICHost = self.hosts[host_list_2.highlighted]
        return selected_host_1, selected_host_2
