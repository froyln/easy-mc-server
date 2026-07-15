"""PaperMC server installer, using the official PaperMC v2 API."""
from __future__ import annotations

from pathlib import Path

from ..downloader import download_file, get_json
from .base import BaseServerInstaller, InstallResult, LogCallback, ProgressCallback

PROJECT_URL = "https://api.papermc.io/v2/projects/paper"


class PaperServerInstaller(BaseServerInstaller):
    id = "paper"
    display_name = "Paper"
    requires_loader_selection = False

    def list_versions(self, log: LogCallback) -> list[str]:
        log("Fetching Paper version list...")
        data = get_json(PROJECT_URL)
        return list(reversed(data["versions"]))

    def install(
        self,
        path: Path,
        version: str,
        log: LogCallback,
        on_progress: ProgressCallback | None = None,
        **kwargs,
    ) -> InstallResult:
        log(f"Fetching Paper build list for {version}...")
        builds_data = get_json(f"{PROJECT_URL}/versions/{version}")
        builds = builds_data["builds"]
        if not builds:
            raise ValueError(f"No Paper builds available for {version}.")
        latest_build = builds[-1]

        build_info = get_json(f"{PROJECT_URL}/versions/{version}/builds/{latest_build}")
        jar_name = build_info["downloads"]["application"]["name"]

        log(f"Downloading Paper build {latest_build}...")
        download_url = f"{PROJECT_URL}/versions/{version}/builds/{latest_build}/downloads/{jar_name}"
        download_file(download_url, path / "paper-server.jar", on_progress)
        log("Paper server downloaded successfully.")

        self.accept_eula(path, log)
        return InstallResult(jar_name="paper-server.jar")
