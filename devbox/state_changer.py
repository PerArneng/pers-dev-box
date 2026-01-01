from abc import ABC, abstractmethod

from devbox.target_lock import TargetLock


class StateChanger(ABC):
    """Abstract base class for state changers."""

    @abstractmethod
    def get_name(self) -> str:
        """Return the name of this state changer.

        Returns:
            str: The name of the state changer.
        """
        pass

    @abstractmethod
    def get_locks(self) -> list[TargetLock]:
        """Return the target locks for this state changer.

        Returns:
            list[TargetLock]: The list of target locks.
        """
        pass

    @abstractmethod
    def change(self) -> None:
        """Apply the state change."""
        pass

    @abstractmethod
    def undo(self) -> None:
        """Undo the state change."""
        pass

    @abstractmethod
    def is_changed(self) -> bool:
        """Check if the state has been changed.

        Returns:
            bool: True if the state has been changed, False otherwise.
        """
        pass
