from textual.reactive import reactive
from textual.widgets import Placeholder
from Config import Config

class HostNavigator(Placeholder):

    host_id = reactive("Ajeje")

    def __init__(self, id, config: Config) -> None:
        super().__init__(label="Host navigator", id=id)
        self.config = config

    def watch_host_id(self, host_id: str) -> None:
        """Watch for changes to the host_id property."""
        self.log(f"Host ID changed to: {host_id}")
        self.border_title = f"Host Navigator - {host_id}"
        # Here you can add logic to update the UI or perform actions based on the new host_id
        # For example, you might want to fetch data related to the new host_id
