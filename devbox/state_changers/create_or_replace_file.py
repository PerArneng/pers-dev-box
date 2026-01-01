import hashlib
from pathlib import Path

from devbox.state_changer import StateChanger
from devbox.target import Target
from devbox.target_lock import TargetLock


class CreateOrReplaceFile(StateChanger):
    """State changer that creates or replaces a file with placeholder content."""

    def __init__(self, path: Path, contents: str) -> None:
        """Initialize the CreateOrReplaceFile state changer.

        Args:
            path: The path to the file to create or replace.
            contents: The contents to write to the file.
        """
        self.path = path
        self.contents = contents

    def get_name(self) -> str:
        """Return the name of this state changer.

        Returns:
            str: The name of the state changer.
        """
        return f"CreateOrReplaceFile({self.path})"

    def get_locks(self) -> list[TargetLock]:
        """Return the target locks for this state changer.

        Returns:
            list[TargetLock]: The list of target locks.
        """
        full_path = str(self.path.resolve())
        checksum = hashlib.sha256(full_path.encode()).hexdigest()
        description = f"Full path to the file {full_path}"

        target = Target(
            name=full_path,
            checksum=checksum,
            description=description,
        )

        target_lock = TargetLock(
            target=target,
            timeout_s=30,
        )

        return [target_lock]

    def change(self) -> None:
        """Apply the state change by creating or replacing the file."""
        self.path.write_text(self.contents)

    def undo(self) -> None:
        """Undo the state change."""
        pass

    def is_changed(self) -> bool:
        """Check if the file exists and contains the expected contents.

        Returns:
            bool: True if the file exists and contains the expected contents, False otherwise.
        """
        if not self.path.exists():
            return False
        return self.path.read_text() == self.contents
