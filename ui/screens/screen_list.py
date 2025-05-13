from ui.screens.CompareScreen import CompareScreen
from ui.screens.ExploreScreen import ExploreScreen


class ScreenElement:
    """Class to represent a screen element."""

    def __init__(self, identifier: str, label: str, screen: type):
        self.identifier = identifier
        self.label = label
        self.screen = screen

    def __repr__(self):
        return f"ScreenElement(label={self.label}, screen={self.screen.__name__})"


top_level_screens: dict[str, ScreenElement] = {
    "explore": ScreenElement("explore", "Explore", ExploreScreen),
    "compare": ScreenElement("compare", "Compare", CompareScreen),
}