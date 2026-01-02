import hashlib
import subprocess

from devbox.change_result import ChangeResult
from devbox.change_status import ChangeStatus
from devbox.state_changer import StateChanger
from devbox.target import Target
from devbox.target_lock import TargetLock
from devbox.utils.devbox_log import DevBoxLog


class HomeBrew(StateChanger):
    """State changer that installs a Homebrew package."""

    def __init__(
        self,
        package_name: str,
        log: DevBoxLog,
        parent: StateChanger | None = None,
    ) -> None:
        """Initialize the HomeBrew state changer.

        Args:
            package_name: The name of the Homebrew package to install.
            log: The logger instance for logging operations.
            parent: Optional parent StateChanger for hierarchy.
        """
        self.package_name = package_name
        self.log = log
        self.parent = parent

    def get_locks(self) -> list[TargetLock]:
        """Return the target locks for this state changer.

        Returns:
            list[TargetLock]: The list of target locks.
        """
        checksum = hashlib.sha256(self.package_name.encode()).hexdigest()
        description = f"Homebrew package installation for {self.package_name}"

        target = Target(
            name=self.package_name,
            checksum=checksum,
            description=description,
        )

        target_lock = TargetLock(
            target=target,
            timeout_s=300,  # 5 minutes timeout for package installation
        )

        return [target_lock]

    def change(self) -> ChangeResult:
        """Apply the state change by installing the Homebrew package.

        Returns:
            ChangeResult: The result of the change operation.
        """
        self.log.info_from(self, f"Starting Homebrew package installation")
        self.log.info_from(self, f"Package name: {self.package_name}")
        self.log.info_from(self, f"Running: brew install {self.package_name}")

        result = subprocess.run(
            ["brew", "install", self.package_name],
            capture_output=True,
            text=True,
        )

        self.log.info_from(self, f"Command exit code: {result.returncode}")

        if result.returncode != 0:
            self.log.error_from(self, f"Installation failed with exit code: {result.returncode}")
            self.log.error_from(self, f"stderr: {result.stderr.strip()}")
            if result.stdout.strip():
                self.log.error_from(self, f"stdout: {result.stdout.strip()}")
            return ChangeResult(
                ChangeStatus.FAILED,
                f"Failed to install {self.package_name}: {result.stderr}",
            )

        self.log.info_from(self, f"Installation completed successfully")
        if result.stdout.strip():
            self.log.info_from(self, f"Output: {result.stdout.strip()[:200]}...")

        return ChangeResult(
            ChangeStatus.SUCCESS,
            f"Successfully installed Homebrew package: {self.package_name}",
        )

    def rollback(self) -> ChangeResult:
        """Rollback the state change by uninstalling the Homebrew package.

        Returns:
            ChangeResult: The result of the rollback operation.
        """
        self.log.info_from(self, f"Starting Homebrew package uninstallation")
        self.log.info_from(self, f"Package name: {self.package_name}")
        self.log.info_from(self, f"Running: brew uninstall {self.package_name}")

        result = subprocess.run(
            ["brew", "uninstall", self.package_name],
            capture_output=True,
            text=True,
        )

        self.log.info_from(self, f"Command exit code: {result.returncode}")

        if result.returncode != 0:
            self.log.error_from(self, f"Uninstallation failed with exit code: {result.returncode}")
            self.log.error_from(self, f"stderr: {result.stderr.strip()}")
            return ChangeResult(
                ChangeStatus.FAILED,
                f"Failed to uninstall {self.package_name}: {result.stderr}",
            )

        self.log.info_from(self, f"Uninstallation completed successfully")
        return ChangeResult(
            ChangeStatus.SUCCESS,
            f"Successfully uninstalled Homebrew package: {self.package_name}",
        )

    def is_changed(self) -> bool:
        """Check if the Homebrew package is already installed.

        Returns:
            bool: True if the package is installed, False otherwise.
        """
        self.log.info_from(self, f"Checking if package is installed: {self.package_name}")
        self.log.info_from(self, f"Running: brew list {self.package_name}")

        result = subprocess.run(
            ["brew", "list", self.package_name],
            capture_output=True,
            text=True,
        )

        is_installed = result.returncode == 0
        if is_installed:
            self.log.info_from(self, f"Package is already installed: {self.package_name}")
        else:
            self.log.info_from(self, f"Package is not installed: {self.package_name}")

        return is_installed

    def description(self) -> str:
        """Return a human-readable description of what this state changer does.

        Returns:
            str: A description of the state change operation.
        """
        return f"Installs the '{self.package_name}' package via Homebrew"
