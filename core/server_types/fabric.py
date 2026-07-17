"""Fabric server installer, using the official FabricMC meta API."""
from __future__ import annotations

from pathlib import Path

from ..downloader import download_file, get_json
from ..types import LogCallback, ProgressCallback
from .base import BaseServerInstaller, InstallResult

API_GAME = "https://meta.fabricmc.net/v2/versions/game"
API_LOADER = "https://meta.fabricmc.net/v2/versions/loader"
API_INSTALLER = "https://meta.fabricmc.net/v2/versions/installer"


class FabricServerInstaller(BaseServerInstaller):
    id = "fabric"
    display_name = "Fabric"
    requires_loader_selection = True

    def list_versions(self, log: LogCallback) -> list[str]:
        log("Fetching Fabric game version list...")
        return [v["version"] for v in get_json(API_GAME) if v["stable"]]

    def list_loader_versions(self, log: LogCallback) -> list[str]:
        log("Fetching Fabric loader version list...")
        return [v["version"] for v in get_json(API_LOADER) if v["stable"]]

    def list_installer_versions(self, log: LogCallback) -> list[str]:
        log("Fetching Fabric installer version list...")
        return [v["version"] for v in get_json(API_INSTALLER) if v["stable"]]

    def install(
        self,
        path: Path,
        version: str,
        log: LogCallback,
        on_progress: ProgressCallback | None = None,
        loader_version: str | None = None,
        installer_version: str | None = None,
        **kwargs,
    ) -> InstallResult:
        if not loader_version:
            loader_version = self.list_loader_versions(log)[0]
        if not installer_version:
            installer_version = self.list_installer_versions(log)[0]

        log(f"Downloading Fabric server jar (mc {version}, loader {loader_version}, installer {installer_version})...")
        download_url = (
            f"https://meta.fabricmc.net/v2/versions/loader/{version}/{loader_version}"
            f"/{installer_version}/server/jar"
        )
        download_file(download_url, path / "fabric-server.jar", on_progress)
        log("Fabric server downloaded successfully.")

        self.accept_eula(path, log)
        return InstallResult(jar_name="fabric-server.jar")
