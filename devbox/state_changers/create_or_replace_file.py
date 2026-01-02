import hashlib
from pathlib import Path

from devbox.change_result import ChangeResult
from devbox.change_status import ChangeStatus
from devbox.state_changer import StateChanger
from devbox.target import Target
from devbox.target_lock import TargetLock
from devbox.utils.devbox_log import DevBoxLog


class CreateOrReplaceFile(StateChanger):
    """State changer that creates or replaces a file with placeholder content."""

    def __init__(self, path: Path, contents: str, log: DevBoxLog) -> None:
        """Initialize the CreateOrReplaceFile state changer.

        Args:
            path: The path to the file to create or replace.
            contents: The contents to write to the file.
            log: The logger instance for logging operations.
        """
        self.path = path
        self.contents = contents
        self.log = log

    def __repr__(self) -> str:
        """Return a string representation of this state changer."""
        return f"CreateOrReplaceFile({self.path})"

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

    def change(self) -> ChangeResult:
        """Apply the state change by creating or replacing the file.

        Returns:
            ChangeResult: The result of the change operation.
        """
        self.log.info_from(self, f"Starting file operation for: {self.path}")
        self.log.info_from(self, f"Target path: {self.path.resolve()}")
        self.log.info_from(self, f"Content length: {len(self.contents)} characters")

        try:
            file_exists = self.path.exists()
            if file_exists:
                self.log.info_from(self, f"File exists, will be replaced")
            else:
                self.log.info_from(self, f"File does not exist, will be created")

            self.log.info_from(self, f"Writing content to file...")
            self.path.write_text(self.contents)
            self.log.info_from(self, f"File write completed successfully")

            return ChangeResult(
                ChangeStatus.SUCCESS,
                f"Created/replaced file: {self.path}",
            )
        except PermissionError as e:
            self.log.error_from(self, f"Permission denied writing to: {self.path}")
            return ChangeResult(
                ChangeStatus.FAILED,
                f"Permission denied: {self.path}: {e}",
            )
        except Exception as e:
            self.log.error_from(self, f"Unexpected error: {e}")
            return ChangeResult(
                ChangeStatus.FAILED,
                f"Failed to create/replace file {self.path}: {e}",
            )

    def undo(self) -> ChangeResult:
        """Undo the state change.

        Returns:
            ChangeResult: The result of the undo operation.
        """
        self.log.warn_from(self, f"Undo requested for: {self.path}")
        self.log.warn_from(self, f"Undo operation is not implemented")
        return ChangeResult(
            ChangeStatus.WARN,
            f"Undo not implemented for: {self.path}",
        )

    def is_changed(self) -> bool:
        """Check if the file exists and contains the expected contents.

        Returns:
            bool: True if the file exists and contains the expected contents, False otherwise.
        """
        if not self.path.exists():
            self.log.info_from(self, f"File does not exist: {self.path}")
            return False
        matches = self.path.read_text() == self.contents
        if matches:
            self.log.info_from(self, f"File already has expected content: {self.path}")
        else:
            self.log.info_from(self, f"File exists but content differs: {self.path}")
        return matches
