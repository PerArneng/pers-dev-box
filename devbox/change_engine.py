from devbox.state_changer import StateChanger
from devbox.utils.devbox_log import DevBoxLog


class ChangeEngine:
    """Engine for managing and executing state changers."""

    def __init__(self, log: DevBoxLog) -> None:
        """Initialize the ChangeEngine.

        Args:
            log: The logger instance for logging operations.
        """
        self.log = log
        self.state_changers: list[StateChanger] = []

    def add_state_changer(self, state_changer: StateChanger) -> None:
        """Add a state changer to the engine.

        Args:
            state_changer: The state changer to add.
        """
        self.log.info(f"Adding state changer: {state_changer.get_name()}")
        self.state_changers.append(state_changer)

    def apply_changes(self) -> None:
        """Run through all state changers and execute their change methods."""
        self.log.info(f"Applying {len(self.state_changers)} state changes")
        for state_changer in self.state_changers:
            if not state_changer.is_changed():
                self.log.info(f"Executing: {state_changer.get_name()}")
                state_changer.change()
            else:
                self.log.info(f"Skipping (already applied): {state_changer.get_name()}")
