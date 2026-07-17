"""Official Mojang vanilla server installer."""
from __future__ import annotations

from pathlib import Path

from ..downloader import download_file, get_json
from ..types import LogCallback, ProgressCallback
from .base import BaseServerInstaller, InstallResult

VERSION_MANIFEST_URL = "https://launchermeta.mojang.com/mc/game/version_manifest.json"


class VanillaServerInstaller(BaseServerInstaller):
    id = "vanilla"
    display_name = "Vanilla"
    requires_loader_selection = False

    def list_versions(self, log: LogCallback) -> list[str]:
        log("Fetching Vanilla version list from Mojang...")
        manifest = get_json(VERSION_MANIFEST_URL)
        return [v["id"] for v in manifest["versions"] if v["type"] == "release"]

    def install(
        self,
        path: Path,
        version: str,
        log: LogCallback,
        on_progress: ProgressCallback | None = None,
        **kwargs,
    ) -> InstallResult:
        log(f"Resolving Vanilla server download for {version}...")
        manifest = get_json(VERSION_MANIFEST_URL)
        version_entry = next((v for v in manifest["versions"] if v["id"] == version), None)
        if version_entry is None:
            raise ValueError(f"Minecraft version {version} not found.")

        version_data = get_json(version_entry["url"])
        download_url = version_data["downloads"]["server"]["url"]

        log("Downloading server.jar...")
        download_file(download_url, path / "server.jar", on_progress)
        log("Vanilla server downloaded successfully.")

        self.accept_eula(path, log)
        return InstallResult(jar_name="server.jar")
