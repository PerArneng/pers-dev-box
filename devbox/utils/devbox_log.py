import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any


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
    def info_from(self, source: Any, message: str) -> None:
        """Log an info message with source.

        Args:
            source: The source object where the log originates.
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
    def warn_from(self, source: Any, message: str) -> None:
        """Log a warning message with source.

        Args:
            source: The source object where the log originates.
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

    @abstractmethod
    def error_from(self, source: Any, message: str) -> None:
        """Log an error message with source.

        Args:
            source: The source object where the log originates.
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

    def _format_with_source(self, source: Any, message: str) -> str:
        """Format a message with source prefix.

        Args:
            source: The source object where the log originates.
            message: The message to log.

        Returns:
            str: The formatted message with source prefix.
        """
        return f"[{source}]: {message}"

    def info(self, message: str) -> None:
        """Log an info message.

        Args:
            message: The message to log.
        """
        self._log("INFO", message, self.INFO_COLOR)

    def info_from(self, source: Any, message: str) -> None:
        """Log an info message with source.

        Args:
            source: The source object where the log originates.
            message: The message to log.
        """
        self.info(self._format_with_source(source, message))

    def warn(self, message: str) -> None:
        """Log a warning message.

        Args:
            message: The message to log.
        """
        self._log("WARN", message, self.WARN_COLOR)

    def warn_from(self, source: Any, message: str) -> None:
        """Log a warning message with source.

        Args:
            source: The source object where the log originates.
            message: The message to log.
        """
        self.warn(self._format_with_source(source, message))

    def error(self, message: str) -> None:
        """Log an error message.

        Args:
            message: The message to log.
        """
        self._log("ERROR", message, self.ERROR_COLOR)

    def error_from(self, source: Any, message: str) -> None:
        """Log an error message with source.

        Args:
            source: The source object where the log originates.
            message: The message to log.
        """
        self.error(self._format_with_source(source, message))
