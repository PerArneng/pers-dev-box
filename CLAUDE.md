# CLAUDE.md

## Project Overview

DevBox is a Python framework for managing and orchestrating file system state changes with dependency injection, logging, and change tracking.

## Architecture

### Dependency Injection

The project uses `dependency-injector` for DI. All dependencies are wired through `devbox/container.py`:

- **Singleton providers**: `DevBoxLogImpl`, `ChangeEngine`
- **Factory providers**: `CreateOrReplaceFile` (accepts runtime params `path`, `contents`)

Classes depend on ABC interfaces, not implementations:
- `DevBoxLog` ABC for logging
- `StateChanger` ABC for state change operations

### Key Components

| Component | Type | Location |
|-----------|------|----------|
| `Container` | DI Container | `devbox/container.py` |
| `StateChanger` | ABC | `devbox/state_changer.py` |
| `ChangeEngine` | Orchestrator | `devbox/change_engine.py` |
| `DevBoxLog` | ABC | `devbox/utils/devbox_log.py` |
| `DevBoxLogImpl` | Implementation | `devbox/utils/devbox_log.py` |
| `CreateOrReplaceFile` | StateChanger impl | `devbox/state_changers/create_or_replace_file.py` |

### Module Structure

```
devbox/
├── __init__.py          # Exports: ChangeEngine, Container, StateChanger
├── container.py         # Central DI container
├── change_engine.py     # Orchestrates state changers
├── state_changer.py     # StateChanger ABC
├── target.py            # Target dataclass
├── target_lock.py       # TargetLock dataclass
├── state_changers/      # StateChanger implementations
│   └── create_or_replace_file.py
└── utils/
    └── devbox_log.py    # DevBoxLog ABC + DevBoxLogImpl
```

## Conventions

### Adding New State Changers

1. Create a new file in `devbox/state_changers/`
2. Implement the `StateChanger` ABC (methods: `get_name`, `get_locks`, `change`, `undo`, `is_changed`)
3. Accept `log: DevBoxLog` as a constructor parameter
4. Add a factory provider in `devbox/container.py`
5. Export from `devbox/state_changers/__init__.py`

### Logging

Use the injected `DevBoxLog` instance for logging:
- `self.log.info("message")` - Green INFO
- `self.log.warn("message")` - Yellow WARN
- `self.log.error("message")` - Red ERROR

Format: `YYYY-MM-DD HH:MM LEVEL message`

### Testing

Override providers for testing:
```python
from unittest.mock import Mock
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
3. Creates state changers via factory
4. Calls `engine.apply_changes()`
