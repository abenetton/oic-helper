from typing import Tuple, List

from textual.app import ComposeResult
from textual.containers import ScrollableContainer
from textual.reactive import reactive
from textual.widgets import Label

from oic_tools import OICHost, OICIntegration


class HostCompare(ScrollableContainer):
    filtered_compare_results: reactive[List[Tuple[str, List[OICIntegration.OICCompare]]]] = reactive([])

    def filter_compare_results(self) -> List[Tuple[str, List[OICIntegration.OICCompare]]]:
        res: List[Tuple[str, List[OICIntegration.OICCompare]]] = []

        for elem in self.compare_results:
            tmp: List[OICIntegration.OICCompare] = [x for x in elem[1] if
                                                    x.result != OICIntegration.OICCompare.CompareResultEnum.EQUAL]
            if tmp:
                res.append((elem[0], tmp))

        return res

    def __init__(self, id, hosts1: OICHost, hosts2: OICHost):
        super().__init__(id=id)
        self.hosts1 = hosts1
        self.hosts2 = hosts2
        self.compare_results: List[Tuple[str, List[OICIntegration.OICCompare]]] = hosts1.compare(hosts2)
        self.filtered_compare_results = self.filter_compare_results()

    def compose(self) -> ComposeResult:
        """Compose the HostCompare widget."""
        for package, result in self.filtered_compare_results:
            if result:
                Label(f"Package: {package}")
                for compare in result:
                    yield Label(f"{compare.result} - {compare.name}")
            else:
                yield Label(f"No integrations found in package {package}")
