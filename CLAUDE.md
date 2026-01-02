# CLAUDE.md

## Project Overview

DevBox is a Python framework for managing and orchestrating file system state changes with dependency injection, logging, and change tracking.

## Architecture

### Dependency Injection

The project uses `dependency-injector` for DI. All dependencies are wired through `devbox/container.py`:

- **Singleton providers**: `DevBoxLogImpl`, `ChangeEngine`
- **Factory providers**:
  - `create_or_replace_file_factory` (accepts `path`, `contents`, optional `parent`)
  - `homebrew_factory` (accepts `package_name`, optional `parent`)
  - `claude_code_factory` (accepts optional `parent`)

Classes depend on ABC interfaces, not implementations:
- `DevBoxLog` ABC for logging
- `StateChanger` ABC for state change operations

### Key Components

| Component | Type | Location |
|-----------|------|----------|
| `Container` | DI Container | `devbox/container.py` |
| `StateChanger` | ABC | `devbox/state_changer.py` |
| `ChangeEngine` | Orchestrator | `devbox/change_engine.py` |
| `ChangeStatus` | Enum | `devbox/change_status.py` |
| `ChangeResult` | Dataclass | `devbox/change_result.py` |
| `DevBoxLog` | ABC | `devbox/utils/devbox_log.py` |
| `DevBoxLogImpl` | Implementation | `devbox/utils/devbox_log.py` |
| `CreateOrReplaceFile` | StateChanger impl | `devbox/state_changers/create_or_replace_file.py` |
| `HomeBrew` | StateChanger impl | `devbox/state_changers/home_brew.py` |
| `ClaudeCode` | StateChanger impl | `devbox/state_changers/claude_code.py` |

### Module Structure

```
devbox/
├── __init__.py          # Exports: ChangeEngine, Container, StateChanger
├── container.py         # Central DI container
├── change_engine.py     # Orchestrates state changers
├── change_result.py     # ChangeResult dataclass
├── change_status.py     # ChangeStatus enum (SUCCESS, FAILED, WARN)
├── state_changer.py     # StateChanger ABC
├── target.py            # Target dataclass
├── target_lock.py       # TargetLock dataclass
├── state_changers/      # StateChanger implementations
│   ├── claude_code.py
│   ├── create_or_replace_file.py
│   └── home_brew.py
└── utils/
    └── devbox_log.py    # DevBoxLog ABC + DevBoxLogImpl
```

## Conventions

### Adding New State Changers

1. Create a new file in `devbox/state_changers/`
2. Implement the `StateChanger` ABC:
   - `get_locks()` - Return list of TargetLock
   - `change()` - Apply change, return `ChangeResult`
   - `rollback()` - Revert change, return `ChangeResult`
   - `is_changed()` - Check if already applied
3. Accept `log: DevBoxLog` and optional `parent: StateChanger | None = None` as constructor parameters
4. Set `self.parent = parent` in constructor
5. Add a factory provider in `devbox/container.py`
6. Export from `devbox/state_changers/__init__.py`

### Parent Hierarchy

StateChangers support optional parent-child relationships for hierarchical logging:

```python
# Standalone changer
home_brew = HomeBrew("git", log)
repr(home_brew)  # "home_brew"

# Child changer with parent
class ClaudeCode(StateChanger):
    def __init__(self, log: DevBoxLog, parent: StateChanger | None = None):
        self.log = log
        self.parent = parent
        # Pass self as parent to create hierarchy
        self._homebrew = HomeBrew(self.PACKAGE_NAME, log, parent=self)

claude_code = ClaudeCode(log)
repr(claude_code)            # "claude_code"
repr(claude_code._homebrew)  # "claude_code.home_brew"
```

### `__repr__` Convention

StateChangers inherit `__repr__` from the ABC, which returns the hierarchical path in snake_case:

- `get_name()` - Returns snake_case class name (e.g., `home_brew`)
- `get_path()` - Returns full dot-separated path (e.g., `claude_code.home_brew`)
- `__repr__()` - Returns `get_path()`

Do NOT override `__repr__` or `get_name()` in implementations.

### ChangeResult

The `change()` and `rollback()` methods return a `ChangeResult`:

```python
from devbox.change_result import ChangeResult
from devbox.change_status import ChangeStatus

# Success
return ChangeResult(ChangeStatus.SUCCESS, "Operation completed")

# Failure
return ChangeResult(ChangeStatus.FAILED, "Error message")

# Warning
return ChangeResult(ChangeStatus.WARN, "Warning message")
```

### Logging

Use the injected `DevBoxLog` instance for logging. Always use source-based logging with `self`:

```python
# Source-based logging (preferred) - includes hierarchical path in output
self.log.info_from(self, "message")   # [claude_code.home_brew]: message
self.log.warn_from(self, "message")   # [claude_code.home_brew]: message
self.log.error_from(self, "message")  # [claude_code.home_brew]: message

# Simple logging (for general messages)
self.log.info("message")
self.log.warn("message")
self.log.error("message")
```

Format: `YYYY-MM-DD HH:MM LEVEL [source_path]: message`

Colors:
- **INFO**: Green
- **WARN**: Yellow
- **ERROR**: Red

### Testing

Override providers for testing:
```python
from unittest.mock import Mock
from dependency_injector import providers
from devbox import Container

container = Container()
mock_log = Mock()
container.log.override(providers.Object(mock_log))
```

## Commands

```bash
# Run the application
uv run python main.py

# Add dependencies
uv add <package>
```

## Entry Point

`main.py` bootstraps the application:
1. Creates `Container` instance
2. Gets logger and engine from container
3. Creates state changers via factory (log auto-injected)
4. Calls `engine.apply_changes()`
