import logging
from abc import ABC, abstractmethod
from datetime import datetime


class DevBoxLog(ABC):
    """Abstract base class for DevBox logging."""

    @abstractmethod
    def info(self, message: str) -> None:
        """Log an info message.

        Args:
            message: The message to log.
        """
        pass

    @abstractmethod
    def warn(self, message: str) -> None:
        """Log a warning message.

        Args:
            message: The message to log.
        """
        pass

    @abstractmethod
    def error(self, message: str) -> None:
        """Log an error message.

        Args:
            message: The message to log.
        """
        pass


class DevBoxLogImpl(DevBoxLog):
    """Implementation of DevBoxLog using Python's standard logging library."""

    # ANSI color codes
    INFO_COLOR = "\033[32m"  # Green
    WARN_COLOR = "\033[33m"  # Yellow
    ERROR_COLOR = "\033[31m"  # Red
    RESET_COLOR = "\033[0m"  # Reset

    def __init__(self) -> None:
        """Initialize the DevBoxLogImpl."""
        self.logger = logging.getLogger("devbox")
        self.logger.setLevel(logging.DEBUG)

        # Remove existing handlers to avoid duplicates
        self.logger.handlers.clear()

        # Create console handler
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)

        # We'll format manually in our methods
        self.logger.addHandler(handler)
        self.logger.propagate = False

    def _log(self, level: str, message: str, color: str) -> None:
        """Internal method to log a message with formatting.

        Args:
            level: The log level (INFO, WARN, ERROR).
            message: The message to log.
            color: The ANSI color code for the level.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        colored_level = f"{color}{level}{self.RESET_COLOR}"
        formatted_message = f"{timestamp} {colored_level} {message}"
        print(formatted_message)

    def info(self, message: str) -> None:
        """Log an info message.

        Args:
            message: The message to log.
        """
        self._log("INFO", message, self.INFO_COLOR)

    def warn(self, message: str) -> None:
        """Log a warning message.

        Args:
            message: The message to log.
        """
        self._log("WARN", message, self.WARN_COLOR)

    def error(self, message: str) -> None:
        """Log an error message.

        Args:
            message: The message to log.
        """
        self._log("ERROR", message, self.ERROR_COLOR)
