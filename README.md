![DevBox Logo](docs/devbox_logo.png)

# DevBox

A Python framework for managing and orchestrating file system state changes with built-in logging and change tracking.

## Features

- **State Management**: Abstract state changer pattern for implementing reversible operations
- **Change Engine**: Orchestrate multiple state changes in a coordinated manner
- **Target Locking**: Track changes with checksums and descriptions
- **Colored Logging**: Built-in logging with colored output for INFO, WARN, and ERROR levels
- **Extensible**: Easy to implement custom state changers

## Components

### StateChanger ABC
Abstract base class for implementing state change operations:
- `get_name()`: Returns the name of the state changer
- `get_locks()`: Returns list of target locks
- `change()`: Applies the state change
- `undo()`: Reverts the state change
- `is_changed()`: Checks if the state has been changed

### ChangeEngine
Manages and executes multiple state changers:
- `add_state_changer(state_changer)`: Add a state changer to the engine
- `apply_changes()`: Execute all registered state changers

### Built-in State Changers

#### CreateOrReplaceFile
Creates or replaces file contents with specified text.

### Logging

DevBox includes a colored logging system with the following format:
```
YYYY-MM-DD HH:MM LEVEL message
```

Levels are color-coded:
- **INFO**: Green
- **WARN**: Yellow
- **ERROR**: Red

## Usage

```python
from pathlib import Path
from devbox import ChangeEngine
from devbox.state_changers import CreateOrReplaceFile
from devbox.utils import DevBoxLogImpl

# Initialize logger
log = DevBoxLogImpl()
log.info("Starting DevBox")

# Create and configure change engine
engine = ChangeEngine()
engine.add_state_changer(CreateOrReplaceFile(Path("file1.txt"), "content 1"))
engine.add_state_changer(CreateOrReplaceFile(Path("file2.txt"), "content 2"))

# Apply all changes
engine.apply_changes()

log.info("Changes applied successfully")
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
python main.py
```

## License

See LICENSE file for details.
