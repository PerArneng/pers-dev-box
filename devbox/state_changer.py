from __future__ import annotations

import re
from abc import ABC, abstractmethod

from devbox.change_result import ChangeResult
from devbox.target_lock import TargetLock


def _camel_to_snake(name: str) -> str:
    """Convert CamelCase to snake_case.

    Args:
        name: A CamelCase string (e.g., 'HomeBrew', 'CreateOrReplaceFile')

    Returns:
        The snake_case equivalent (e.g., 'home_brew', 'create_or_replace_file')
    """
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


class StateChanger(ABC):
    """Abstract base class for state changers."""

    _parent: StateChanger | None = None

    @property
    def parent(self) -> StateChanger | None:
        """Get the parent state changer.

        Returns:
            The parent StateChanger, or None if this is a root changer.
        """
        return self._parent

    @parent.setter
    def parent(self, value: StateChanger | None) -> None:
        """Set the parent state changer.

        Args:
            value: The parent StateChanger, or None.
        """
        self._parent = value

    def get_name(self) -> str:
        """Return the snake_case name of this state changer.

        Returns:
            str: The snake_case name derived from the class name.
        """
        return _camel_to_snake(self.__class__.__name__)

    def get_path(self) -> str:
        """Return the full hierarchical path of this state changer.

        Returns:
            str: The dot-separated path from root to this changer.
                 Example: 'claude_code.home_brew'
        """
        if self._parent is not None:
            return f"{self._parent.get_path()}.{self.get_name()}"
        return self.get_name()

    def __repr__(self) -> str:
        """Return the hierarchical path representation.

        Returns:
            str: The full path (e.g., 'claude_code.home_brew')
        """
        return self.get_path()

    @abstractmethod
    def get_locks(self) -> list[TargetLock]:
        """Return the target locks for this state changer.

        Returns:
            list[TargetLock]: The list of target locks.
        """
        pass

    @abstractmethod
    def change(self, verbose: bool = False) -> ChangeResult:
        """Apply the state change.

        Args:
            verbose: If True, log full command output (stdout/stderr).

        Returns:
            ChangeResult: The result of the change operation.
        """
        pass

    @abstractmethod
    def rollback(self, verbose: bool = False) -> ChangeResult:
        """Rollback the state change.

        Args:
            verbose: If True, log full command output (stdout/stderr).

        Returns:
            ChangeResult: The result of the rollback operation.
        """
        pass

    @abstractmethod
    def is_changed(self) -> bool:
        """Check if the state has been changed.

        Returns:
            bool: True if the state has been changed, False otherwise.
        """
        pass

    @abstractmethod
    def description(self) -> str:
        """Return a human-readable description of what this state changer does.

        Returns:
            str: A description of the state change operation.
        """
        pass
