![DevBox Logo](docs/devbox_logo.png)

# DevBox

A CLI tool and Python framework for provisioning developer workstations. DevBox manages the installation and configuration of development tools with reversible state changes, dependency injection, and detailed logging.

## Purpose

DevBox automates the setup of a consistent development environment by:
- Installing essential CLI tools via Homebrew (Claude Code, K9s, etc.)
- Managing configuration files
- Providing rollback capability for all changes
- Tracking what's installed and what needs updating

## Quick Start

```bash
# Clone and install
git clone https://github.com/PerArneng/pers-dev-box.git
cd pers-dev-box
uv sync

# List available tools
uv run python main.py list

# Install tools
uv run python main.py apply claude_code,k9s

# Uninstall tools
uv run python main.py rollback k9s
```

## CLI Commands

### List available changes
```bash
uv run python main.py list
```
Output:
```
Available changes:
  claude_code     - Installs Claude Code CLI via Homebrew
  k9s             - Installs K9s Kubernetes CLI via Homebrew
```

### Apply changes
```bash
# Apply single change
uv run python main.py apply claude_code

# Apply multiple changes (comma-separated)
uv run python main.py apply claude_code,k9s

# Apply with verbose output (shows full command stdout/stderr)
uv run python main.py apply claude_code --verbose
uv run python main.py apply k9s -v
```

### Rollback changes
```bash
# Rollback single change
uv run python main.py rollback k9s

# Rollback multiple changes
uv run python main.py rollback claude_code,k9s

# Rollback with verbose output
uv run python main.py rollback k9s --verbose
```

## Available Tools

| Name | Description |
|------|-------------|
| `claude_code` | Installs Claude Code CLI via Homebrew |
| `k9s` | Installs K9s Kubernetes CLI via Homebrew |

## Features

- **CLI Interface**: Simple commands to list, apply, and rollback changes
- **Reversible Operations**: Every change can be rolled back
- **Verbose Mode**: Full command output for debugging
- **Idempotent**: Skip already-applied changes automatically
- **Dependency Injection**: Clean architecture using `dependency-injector`
- **Colored Logging**: Traceable output with source prefixes
- **Extensible**: Easy to add new state changers

## Architecture

### StateChanger ABC
Abstract base class for implementing state change operations:
- `get_locks()`: Returns list of target locks
- `change(verbose)`: Applies the state change, returns `ChangeResult`
- `rollback(verbose)`: Reverts the state change, returns `ChangeResult`
- `is_changed()`: Checks if already applied
- `description()`: Human-readable description

### Built-in State Changers

| Changer | Description |
|---------|-------------|
| `ClaudeCode` | Installs Claude Code CLI via Homebrew |
| `K9s` | Installs K9s Kubernetes CLI via Homebrew |
| `HomeBrew` | Generic Homebrew package installer |
| `CreateOrReplaceFile` | Creates or replaces file contents |

### ChangeResult & ChangeStatus
Operations return a `ChangeResult` with status and message:
- `ChangeStatus.SUCCESS`: Operation completed successfully
- `ChangeStatus.FAILED`: Operation failed
- `ChangeStatus.WARN`: Operation completed with warnings

### Logging

DevBox includes colored logging with source-based tracing:

```
2026-01-02 12:41 INFO [claude_code]: Installing Claude Code
2026-01-02 12:41 INFO [claude_code.home_brew]: Running: brew install claude-code
2026-01-02 12:41 INFO [claude_code.home_brew]: Installation completed successfully
```

Levels are color-coded:
- **INFO**: Green
- **WARN**: Yellow
- **ERROR**: Red

## Programmatic Usage

DevBox can also be used as a library:

```python
from pathlib import Path
from devbox import Container

container = Container()
log = container.log()
engine = container.change_engine()

# Use factories for custom state changers
engine.add_state_changer(
    container.create_or_replace_file_factory(
        path=Path("config.txt"),
        contents="my configuration",
    )
)

engine.add_state_changer(
    container.homebrew_factory(package_name="jq")
)

engine.apply_changes(verbose=True)
```

## License

See LICENSE file for details.
