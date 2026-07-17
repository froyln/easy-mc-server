"""Common interface every server type (Vanilla, Fabric, Forge, Paper...) implements."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

from ..types import LogCallback, ProgressCallback


@dataclass
class InstallResult:
    """Outcome of a server installation, used to build the launch command."""
    jar_name: str
    notes: str = ""


class BaseServerInstaller(ABC):
    """Base class for every supported Minecraft server type."""

    id: str = "base"
    display_name: str = "Base"
    requires_loader_selection: bool = False

    @abstractmethod
    def list_versions(self, log: LogCallback) -> list[str]:
        """Return available Minecraft versions, newest first."""
        raise NotImplementedError

    @abstractmethod
    def install(
        self,
        path: Path,
        version: str,
        log: LogCallback,
        on_progress: ProgressCallback | None = None,
        **kwargs,
    ) -> InstallResult:
        """Download and set up the server jar inside `path`."""
        raise NotImplementedError

    def accept_eula(self, path: Path, log: LogCallback) -> None:
        eula_path = path / "eula.txt"
        eula_path.write_text("eula=true\n", encoding="utf-8")
        log("EULA accepted automatically.")
