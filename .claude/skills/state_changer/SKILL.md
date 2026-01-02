---
name: state_changer
description: How to create a StateChanger. useful for when creating a StateChanger
---

# Creating a New StateChanger

This guide explains how to implement a new `StateChanger` for the DevBox framework.

## File Location

Create your StateChanger in: `devbox/state_changers/<name>.py`

Use snake_case for the filename (e.g., `home_brew.py`, `create_or_replace_file.py`).

## Required Imports

```python
import hashlib  # For generating checksums

from devbox.change_result import ChangeResult
from devbox.change_status import ChangeStatus
from devbox.state_changer import StateChanger
from devbox.target import Target
from devbox.target_lock import TargetLock
from devbox.utils.devbox_log import DevBoxLog
```

## Class Template

```python
class MyStateChanger(StateChanger):
    """Brief description of what this state changer does."""

    def __init__(self, my_param: str, log: DevBoxLog) -> None:
        """Initialize the state changer.

        Args:
            my_param: Description of parameter.
            log: The logger instance for logging operations.
        """
        self.my_param = my_param
        self.log = log

    def __repr__(self) -> str:
        """Return a string representation for traceable logging."""
        return f"MyStateChanger({self.my_param})"

    def get_name(self) -> str:
        """Return the name of this state changer."""
        return f"MyStateChanger({self.my_param})"

    def get_locks(self) -> list[TargetLock]:
        """Return the target locks for this state changer."""
        checksum = hashlib.sha256(self.my_param.encode()).hexdigest()
        description = f"Description of what is being locked: {self.my_param}"

        target = Target(
            name=self.my_param,
            checksum=checksum,
            description=description,
        )

        target_lock = TargetLock(
            target=target,
            timeout_s=30,  # Adjust based on expected operation time
        )

        return [target_lock]

    def change(self) -> ChangeResult:
        """Apply the state change."""
        self.log.info_from(self, f"Starting operation for: {self.my_param}")

        try:
            # Perform the actual change here
            self.log.info_from(self, f"Operation completed successfully")
            return ChangeResult(
                ChangeStatus.SUCCESS,
                f"Successfully completed: {self.my_param}",
            )
        except Exception as e:
            self.log.error_from(self, f"Operation failed: {e}")
            return ChangeResult(
                ChangeStatus.FAILED,
                f"Failed: {self.my_param}: {e}",
            )

    def undo(self) -> ChangeResult:
        """Undo the state change."""
        self.log.info_from(self, f"Undoing operation for: {self.my_param}")

        # Implement undo logic or return WARN if not implemented
        return ChangeResult(
            ChangeStatus.WARN,
            f"Undo not implemented for: {self.my_param}",
        )

    def is_changed(self) -> bool:
        """Check if the state has already been changed."""
        self.log.info_from(self, f"Checking state for: {self.my_param}")

        # Return True if already in desired state, False otherwise
        is_applied = False  # Replace with actual check

        if is_applied:
            self.log.info_from(self, f"Already applied: {self.my_param}")
        else:
            self.log.info_from(self, f"Not yet applied: {self.my_param}")

        return is_applied
```

## Required Steps After Creating the Class

### 1. Export from `devbox/state_changers/__init__.py`

```python
from devbox.state_changers.my_state_changer import MyStateChanger

__all__ = ["CreateOrReplaceFile", "HomeBrew", "MyStateChanger"]
```

### 2. Add Factory to `devbox/container.py`

```python
from devbox.state_changers.my_state_changer import MyStateChanger

# In the Container class:
my_state_changer_factory = providers.Factory(
    MyStateChanger,
    log=log,
)
```

## Key Conventions

### Logging
- Always use source-based logging: `self.log.info_from(self, "message")`
- Log at the start and end of operations
- Log errors with `self.log.error_from(self, "message")`
- Log warnings with `self.log.warn_from(self, "message")`

### `__repr__`
- MUST implement `__repr__` for traceable logging
- Format: `ClassName(key_identifier)`
- Used by source-based logging to show `[ClassName(id)]: message`

### ChangeResult
- Always return `ChangeResult` from `change()` and `undo()`
- Use appropriate status:
  - `ChangeStatus.SUCCESS` - Operation completed successfully
  - `ChangeStatus.FAILED` - Operation failed
  - `ChangeStatus.WARN` - Operation has warnings (e.g., undo not implemented)

### Checksums
- Generate checksum from the unique identifier using SHA256
- Checksum should be deterministic for the same input

### Timeouts
- Set `timeout_s` in `TargetLock` based on expected operation duration
- File operations: 30 seconds
- Package installations: 300 seconds (5 minutes)
- Network operations: adjust accordingly

## Example: Checking External State

For state changers that interact with external systems (like HomeBrew), use subprocess:

```python
import subprocess

def is_changed(self) -> bool:
    result = subprocess.run(
        ["some-command", "check", self.my_param],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0
```

## Example: File System Operations

For file operations, use pathlib:

```python
from pathlib import Path

def is_changed(self) -> bool:
    if not self.path.exists():
        return False
    return self.path.read_text() == self.expected_content
```
