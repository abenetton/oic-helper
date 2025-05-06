from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Placeholder, Footer

from ui.common.bindings import screen_common_bindings


class ExploreScreen(Screen):
    """Explore screen of the OIC Helper app."""
    BINDINGS = screen_common_bindings

    def compose(self) -> ComposeResult:
        yield Header()
        yield Placeholder("Explore screen")
        yield Footer()
