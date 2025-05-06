from textual.binding import Binding

screen_common_bindings: list[Binding] = [
    Binding("escape", "app.pop_screen", "Go Back")
]