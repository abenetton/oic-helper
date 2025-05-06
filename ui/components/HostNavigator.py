from textual.widgets import Placeholder
from Config import Config

class HostNavigator(Placeholder):
    def __init__(self, config: Config, host_id: str) -> None:
        super().__init__("Host navigator " + host_id)
        self.config = config
        self.host_id = host_id