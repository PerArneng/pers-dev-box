from devbox.change_result import ChangeResult
from devbox.state_changer import StateChanger
from devbox.state_changers.home_brew import HomeBrew
from devbox.target_lock import TargetLock
from devbox.utils.devbox_log import DevBoxLog


class ClaudeCode(StateChanger):
    """State changer that installs Claude Code via Homebrew."""

    PACKAGE_NAME = "claude-code"

    def __init__(
        self,
        log: DevBoxLog,
        parent: StateChanger | None = None,
    ) -> None:
        """Initialize the ClaudeCode state changer.

        Args:
            log: The logger instance for logging operations.
            parent: Optional parent StateChanger for hierarchy.
        """
        self.log = log
        self.parent = parent
        self._homebrew = HomeBrew(self.PACKAGE_NAME, log, parent=self)

    def get_locks(self) -> list[TargetLock]:
        """Return the target locks for this state changer.

        Returns:
            list[TargetLock]: The list of target locks.
        """
        return self._homebrew.get_locks()

    def change(self) -> ChangeResult:
        """Apply the state change by installing Claude Code via Homebrew.

        Returns:
            ChangeResult: The result of the change operation.
        """
        self.log.info_from(self, "Installing Claude Code")
        return self._homebrew.change()

    def rollback(self) -> ChangeResult:
        """Rollback the state change by uninstalling Claude Code.

        Returns:
            ChangeResult: The result of the rollback operation.
        """
        self.log.info_from(self, "Uninstalling Claude Code")
        return self._homebrew.rollback()

    def is_changed(self) -> bool:
        """Check if Claude Code is already installed.

        Returns:
            bool: True if Claude Code is installed, False otherwise.
        """
        return self._homebrew.is_changed()

    def description(self) -> str:
        """Return a human-readable description of what this state changer does.

        Returns:
            str: A description of the state change operation.
        """
        return "Installs Claude Code CLI via Homebrew"
