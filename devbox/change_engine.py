from devbox.state_changer import StateChanger


class ChangeEngine:
    """Engine for managing and executing state changers."""

    def __init__(self) -> None:
        """Initialize the ChangeEngine."""
        self.state_changers: list[StateChanger] = []

    def add_state_changer(self, state_changer: StateChanger) -> None:
        """Add a state changer to the engine.

        Args:
            state_changer: The state changer to add.
        """
        self.state_changers.append(state_changer)

    def apply_changes(self) -> None:
        """Run through all state changers and execute their change methods."""
        for state_changer in self.state_changers:
            state_changer.change()
