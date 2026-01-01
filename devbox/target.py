from dataclasses import dataclass


@dataclass
class Target:
    """Represents a target."""

    name: str
    checksum: str
    description: str
