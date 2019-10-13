from typing import Set, Dict, Any


modes = set()


class ScreenMode:
    def __init__(self, name: str, template_file: str, value_positions):
        self.name = name
        self.template_file = template_file
        self.value_positions = value_positions

        modes.add(self)  # add the mode into the list of all modes

    def fill_template(self, **values):
        # Check that all open positions are given by args (may give more values than needed)
        ...

    def display(self):
        ...


class ScreenController:
    def __init__(self, screen_modes: Set[ScreenMode]) -> None:
        assert len(screen_modes) > 0  # must be at least one screen mode
        self.modes = screen_modes
        self.current_mode = screen_modes[0]  # initialize screen to first mode

    def set_mode(self, mode_name: str) -> ScreenMode:
        self.current_mode = next(filter(lambda m: m.name == mode_name, self.modes))
        return self.current_mode

    def display_data(self, data: Dict[str, Any]) -> None:
        self.current_mode.display(data)


# Create some basic modes that might be used
ScreenMode("debug", ..., ...)
ScreenMode("accel", ..., ...)
ScreenMode("enduro", ..., ...)
