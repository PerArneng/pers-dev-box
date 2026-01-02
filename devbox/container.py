from dependency_injector import containers, providers

from devbox.change_engine import ChangeEngine
from devbox.state_changers.claude_code import ClaudeCode
from devbox.state_changers.create_or_replace_file import CreateOrReplaceFile
from devbox.state_changers.home_brew import HomeBrew
from devbox.utils.devbox_log import DevBoxLog, DevBoxLogImpl


class Container(containers.DeclarativeContainer):
    """Main dependency injection container for DevBox."""

    # Logging - Singleton (one logger instance for the entire application)
    log: providers.Provider[DevBoxLog] = providers.Singleton(DevBoxLogImpl)

    # State Changer Factory - accepts (path, contents) at call time
    create_or_replace_file_factory = providers.Factory(
        CreateOrReplaceFile,
        log=log,
    )

    # HomeBrew Factory - accepts (package_name) at call time
    homebrew_factory = providers.Factory(
        HomeBrew,
        log=log,
    )

    # ClaudeCode Factory - installs claude-code via Homebrew
    claude_code_factory = providers.Factory(
        ClaudeCode,
        log=log,
    )

    # ChangeEngine - Singleton (one engine for the application)
    change_engine = providers.Singleton(
        ChangeEngine,
        log=log,
    )
