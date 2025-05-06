
from textual.widgets import OptionList
from textual.widgets.option_list import Option
from Config import Config

class HostPicker(OptionList):
    def __init__(self, config: Config) -> None:
        super().__init__()
        self.add_options([Option(value.label, id=key) for key, value in config.hosts.items()])