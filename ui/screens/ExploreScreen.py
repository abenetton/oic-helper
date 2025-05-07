from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Header

from Config import Config
from ui.common.bindings import screen_common_bindings
from ui.components import HostNavigator


class ExploreScreen(Screen):
    """Explore screen of the OIC Helper app."""
    BINDINGS = screen_common_bindings

    def __init__(self, name=None, cid=None, classes=None):
        super().__init__(name, cid, classes)
        self.config = Config()
        self.config.load_from_file('data/config.json')

    def compose(self) -> ComposeResult:
        yield Header()
        yield HostNavigator(config=self.config)
        yield Footer()
