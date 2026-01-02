from enum import Enum


class ChangeStatus(Enum):
    """Enum representing the status of a state change operation."""

    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    WARN = "WARN"

    def __repr__(self) -> str:
        """Return a nice string representation of the status."""
        return self.value
