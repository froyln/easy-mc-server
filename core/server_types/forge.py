"""Forge server installer, using the official MinecraftForge promotions feed."""
from __future__ import annotations

from pathlib import Path

from ..downloader import download_file, get_json
from ..process_runner import run_streaming
from ..system_check import find_java_executable
from ..types import LogCallback, ProgressCallback
from .base import BaseServerInstaller, InstallResult

PROMOTIONS_URL = "https://files.minecraftforge.net/net/minecraftforge/forge/promotions_slim.json"


class ForgeServerInstaller(BaseServerInstaller):
    id = "forge"
    display_name = "Forge"
    requires_loader_selection = False

    def _promotions(self, log: LogCallback) -> dict:
        log("Fetching Forge promotions feed...")
        return get_json(PROMOTIONS_URL)["promos"]

    def list_versions(self, log: LogCallback) -> list[str]:
        promos = self._promotions(log)
        versions = sorted(
            {key.replace("-recommended", "").replace("-latest", "") for key in promos},
            key=_version_sort_key,
            reverse=True,
        )
        return versions

    def install(
        self,
        path: Path,
        version: str,
        log: LogCallback,
        on_progress: ProgressCallback | None = None,
        **kwargs,
    ) -> InstallResult:
        promos = self._promotions(log)
        forge_build = promos.get(f"{version}-recommended") or promos.get(f"{version}-latest")
        if forge_build is None:
            raise ValueError(f"No Forge build found for Minecraft {version}.")

        full_version = f"{version}-{forge_build}"
        log(f"Downloading Forge installer {full_version}...")
        download_url = (
            f"https://maven.minecraftforge.net/net/minecraftforge/forge/"
            f"{full_version}/forge-{full_version}-installer.jar"
        )
        installer_path = path / "forge-installer.jar"
        download_file(download_url, installer_path, on_progress)
        log("Forge installer downloaded successfully.")

        java_bin = find_java_executable() or "java"
        log("Running Forge installer (this can take a while)...")
        run_streaming([java_bin, "-jar", "forge-installer.jar", "--installServer"], path, log)

        self.accept_eula(path, log)
        installer_path.unlink(missing_ok=True)

        run_script = "run.bat" if (path / "run.bat").exists() else "run.sh"
        return InstallResult(
            jar_name="",
            notes=f"Forge generated its own launch script: {run_script}",
        )


def _version_sort_key(version: str) -> tuple:
    return tuple(int(part) if part.isdigit() else 0 for part in version.split("."))
