from dataclasses import dataclass

from devbox.change_status import ChangeStatus


@dataclass
class ChangeResult:
    """Represents the result of a state change operation."""

    status: ChangeStatus
    message: str

    def __repr__(self) -> str:
        """Return a nice string representation of the result."""
        return f"[{self.status.value}] {self.message}"
