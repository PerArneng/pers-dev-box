from devbox.change_result import ChangeResult
from devbox.state_changer import StateChanger
from devbox.state_changers.home_brew import HomeBrew
from devbox.target_lock import TargetLock
from devbox.utils.devbox_log import DevBoxLog


class K9s(StateChanger):
    """State changer that installs K9s via Homebrew."""

    PACKAGE_NAME = "k9s"

    def __init__(
        self,
        log: DevBoxLog,
        parent: StateChanger | None = None,
    ) -> None:
        """Initialize the K9s state changer.

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

    def change(self, verbose: bool = False) -> ChangeResult:
        """Apply the state change by installing K9S via Homebrew.

        Args:
            verbose: If True, log full command output (stdout/stderr).

        Returns:
            ChangeResult: The result of the change operation.
        """
        self.log.info_from(self, "Installing K9S")
        return self._homebrew.change(verbose)

    def rollback(self, verbose: bool = False) -> ChangeResult:
        """Rollback the state change by uninstalling K9S.

        Args:
            verbose: If True, log full command output (stdout/stderr).

        Returns:
            ChangeResult: The result of the rollback operation.
        """
        self.log.info_from(self, "Uninstalling K9S")
        return self._homebrew.rollback(verbose)

    def is_changed(self) -> bool:
        """Check if K9S is already installed.

        Returns:
            bool: True if K9S is installed, False otherwise.
        """
        return self._homebrew.is_changed()

    def description(self) -> str:
        """Return a human-readable description of what this state changer does.

        Returns:
            str: A description of the state change operation.
        """
        return "Installs K9S Kubernetes CLI via Homebrew"
