from textual.app import ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import Footer, Header, OptionList, ContentSwitcher
from textual import on
from textual.reactive import reactive

from ui.common.bindings import screen_common_bindings
from ui.components import HostPicker, HostNavigator
from Config import Config


class ExploreScreen(Screen):
    """Explore screen of the OIC Helper app."""
    BINDINGS = [
        Binding("escape", "go_back", "Go Back")
    ]

    def __init__(self, name=None, cid=None, classes=None):
        super().__init__(name, cid, classes)
        self.config = Config()
        self.config.load_from_file('data/config.json')

    def compose(self) -> ComposeResult:
        yield Header()
        with ContentSwitcher(initial="host_picker"):
            yield HostPicker(id="host_picker", config=self.config)
            yield HostNavigator(id="host_navigator", config=self.config)  # Valore predefinito
        yield Footer()

    @on(HostPicker.OptionSelected)
    def handle_option_selected(self, event: HostPicker.OptionSelected) -> None:
        """Handle option selection."""
        self.query_one(ContentSwitcher).current = "host_navigator"
        self.query_one(HostNavigator).host_id = event.option.id
        event.stop()

    def action_go_back(self) -> None:
        """Go back to the previous screen."""
        if self.query_one(ContentSwitcher).current == "host_picker":
            self.app.pop_screen()
        else:
            self.query_one(ContentSwitcher).current = "host_picker"
            self.query_one(HostPicker).focus()
