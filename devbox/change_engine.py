from devbox.change_status import ChangeStatus
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

    def __repr__(self) -> str:
        """Return a string representation of this engine."""
        return f"ChangeEngine(changers={len(self.state_changers)})"

    def add_state_changer(self, state_changer: StateChanger) -> None:
        """Add a state changer to the engine.

        Args:
            state_changer: The state changer to add.
        """
        self.log.info_from(self, f"Adding state changer: {state_changer}")
        self.log.info_from(self, f"Total state changers: {len(self.state_changers) + 1}")
        self.state_changers.append(state_changer)

    def apply_changes(self, verbose: bool = False) -> None:
        """Run through all state changers and execute their change methods.

        Args:
            verbose: If True, log full command output (stdout/stderr).
        """
        self.log.info_from(self, f"Starting to apply changes")
        self.log.info_from(self, f"Total state changers to process: {len(self.state_changers)}")

        success_count = 0
        failed_count = 0
        skipped_count = 0

        for i, state_changer in enumerate(self.state_changers, 1):
            self.log.info_from(self, f"Processing state changer {i}/{len(self.state_changers)}: {state_changer}")

            if not state_changer.is_changed():
                self.log.info_from(self, f"Executing change for: {state_changer}")
                result = state_changer.change(verbose)
                self._log_result(state_changer, result)

                if result.status == ChangeStatus.SUCCESS:
                    success_count += 1
                elif result.status == ChangeStatus.FAILED:
                    failed_count += 1
            else:
                self.log.info_from(self, f"Skipping (already applied): {state_changer}")
                skipped_count += 1

        self.log.info_from(self, f"Finished applying changes")
        self.log.info_from(self, f"Summary: {success_count} succeeded, {failed_count} failed, {skipped_count} skipped")

    def _log_result(self, state_changer: StateChanger, result) -> None:
        """Log the result of a change operation based on its status.

        Args:
            state_changer: The state changer that produced the result.
            result: The ChangeResult to log.
        """
        if result.status == ChangeStatus.SUCCESS:
            self.log.info_from(self, f"Result: {result}")
        elif result.status == ChangeStatus.WARN:
            self.log.warn_from(self, f"Result: {result}")
        elif result.status == ChangeStatus.FAILED:
            self.log.error_from(self, f"Result: {result}")
