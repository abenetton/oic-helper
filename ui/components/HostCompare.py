from typing import Tuple

from textual import events, on
from textual.app import ComposeResult
from textual.containers import Container
from textual.reactive import reactive
from textual.widgets import Label, OptionList, Placeholder
from textual.widgets._option_list import Option

from oic_tools import OICHost


class HostCompare(Container):

    def __init__(self, id, hosts: list[OICHost]):
        super().__init__(id=id)
        self.hosts = hosts

    def compose(self) -> ComposeResult:
        """Compose the HostCompare widget."""
        yield Placeholder("Host compare")