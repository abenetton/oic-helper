from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, OptionList
from textual.widgets.option_list import Option

from ui.screens.screen_list import top_level_screens  # Importa top_level_screens


class OICHelper(App):
    TITLE = "OIC Helper Tool"
    #BINDINGS = [("c", "open_config", "Open config")]
    CSS_PATH = "oic_helper.tcss"

    # Popola SCREENS utilizzando top_level_screens
    SCREENS = {key: value.screen for key, value in top_level_screens.items()}

    def compose(self) -> ComposeResult:
        yield Header()
        yield OptionList(
            *[Option(value.label, id=value.identifier) for value in top_level_screens.values()]
        )
        yield Footer()

    # Generate event handler for option list
    @on(OptionList.OptionSelected)
    def handle_option_selected(self, event: OptionList.OptionSelected) -> None:
        """Handle option selection."""

        if event.option.id not in top_level_screens:
            self.log(f"Invalid option selected: {event.option.id}")
            return

        app.push_screen(event.option.id)

    def on_mount(self) -> None:
        """Called when the app is mounted."""
        # self.push_screen("compare") # TODO: Remove after testing


if __name__ == "__main__":
    app = OICHelper()
    app.run()
