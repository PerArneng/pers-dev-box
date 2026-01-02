![DevBox Logo](docs/devbox_logo.png)

# DevBox

A Python framework for managing and orchestrating file system state changes with dependency injection, logging, and change tracking.

## Features

- **Dependency Injection**: Central container for wiring dependencies using `dependency-injector`
- **State Management**: Abstract state changer pattern for implementing reversible operations
- **Change Engine**: Orchestrate multiple state changes in a coordinated manner
- **Change Results**: Track success, failure, and warnings with `ChangeResult` and `ChangeStatus`
- **Target Locking**: Track changes with checksums and descriptions
- **Source-Based Logging**: Colored logging with traceable source prefixes (`[ClassName]: message`)
- **Extensible**: Easy to implement custom state changers

## Components

### StateChanger ABC
Abstract base class for implementing state change operations:
- `get_name()`: Returns the name of the state changer
- `get_locks()`: Returns list of target locks
- `change()`: Applies the state change, returns `ChangeResult`
- `undo()`: Reverts the state change, returns `ChangeResult`
- `is_changed()`: Checks if the state has been changed

### ChangeEngine
Manages and executes multiple state changers:
- `add_state_changer(state_changer)`: Add a state changer to the engine
- `apply_changes()`: Execute all registered state changers

### ChangeResult & ChangeStatus
Operations return a `ChangeResult` with status and message:
- `ChangeStatus.SUCCESS`: Operation completed successfully
- `ChangeStatus.FAILED`: Operation failed
- `ChangeStatus.WARN`: Operation completed with warnings

### Built-in State Changers

#### CreateOrReplaceFile
Creates or replaces file contents with specified text.

#### HomeBrew
Installs Homebrew packages via `brew install`.

### Logging

DevBox includes a colored logging system with source-based tracing:

```
YYYY-MM-DD HH:MM LEVEL [Source]: message
```

Example output:
```
2026-01-02 12:41 INFO [ChangeEngine(changers=2)]: Starting to apply changes
2026-01-02 12:41 INFO [CreateOrReplaceFile(file1.txt)]: Writing content to file...
2026-01-02 12:41 INFO [ChangeEngine(changers=2)]: Result: [SUCCESS] Created/replaced file: file1.txt
```

Levels are color-coded:
- **INFO**: Green
- **WARN**: Yellow
- **ERROR**: Red

## Usage

```python
from pathlib import Path
from devbox import Container

def main():
    # Create the DI container
    container = Container()

    # Get logger from container (singleton)
    log = container.log()
    log.info("DevBox starting up")

    # Get change engine from container (singleton)
    engine = container.change_engine()

    # Create state changers using factories (log auto-injected)
    engine.add_state_changer(
        container.create_or_replace_file_factory(
            path=Path("config.txt"),
            contents="my configuration",
        )
    )

    engine.add_state_changer(
        container.homebrew_factory(
            package_name="jq",
        )
    )

    # Apply all changes
    engine.apply_changes()

    log.info("DevBox finished")

if __name__ == "__main__":
    main()
```

## Installation

```bash
# Clone the repository
git clone https://github.com/PerArneng/pers-dev-box.git
cd pers-dev-box

# Install dependencies with uv
uv sync
```

## Running

```bash
uv run python main.py
```

## License

See LICENSE file for details.
