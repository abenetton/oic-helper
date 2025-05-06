from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Header, OptionList
from textual import on

from ui.common.bindings import screen_common_bindings
from ui.components import HostPicker
from Config import Config


class ExploreScreen(Screen):
    """Explore screen of the OIC Helper app."""
    BINDINGS = screen_common_bindings

    def __init__(self, name = None, id = None, classes = None):
        super().__init__(name, id, classes)
        self.config = Config()
        self.config.load_from_file('data/config.json')


    def compose(self) -> ComposeResult:
        yield Header()
        yield HostPicker(self.config)
        yield Footer()

    # Generate event handler for option list
    @on(OptionList.OptionSelected)
    def handle_option_selected(self, event: OptionList.OptionSelected) -> None:
        """Handle option selection."""

        if event.option.id not in self.config.hosts:
            self.log(f"Invalid option selected: {event.option.id}")
            return

        
