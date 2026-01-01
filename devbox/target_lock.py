from dataclasses import dataclass

from devbox.target import Target


@dataclass
class TargetLock:
    """Represents a lock on a target."""

    target: Target
    timeout_s: int
