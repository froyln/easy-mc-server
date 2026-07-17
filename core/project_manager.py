"""Ties together server type installers, MCDReforged and launch script generation."""
from __future__ import annotations

import stat
from dataclasses import dataclass
from pathlib import Path

from . import launch_scripts, mcdreforged_setup
from .server_types import get_installer
from .system_check import is_windows
from .types import LogCallback, ProgressCallback


@dataclass
class ServerRequest:
    destination: Path
    server_type_id: str
    mc_version: str
    use_mcdreforged: bool
    min_ram_mb: str = "1024"
    max_ram_mb: str = "2048"
    loader_version: str | None = None
    installer_version: str | None = None


def create_server(request: ServerRequest, log: LogCallback, on_progress: ProgressCallback | None = None) -> Path:
    installer = get_installer(request.server_type_id)

    if request.use_mcdreforged:
        if not mcdreforged_setup.is_mcdreforged_installed():
            mcdreforged_setup.install_mcdreforged(log)
        server_dir = mcdreforged_setup.init_mcdreforged(request.destination, log)
    else:
        server_dir = request.destination
        server_dir.mkdir(parents=True, exist_ok=True)

    result = installer.install(
        server_dir,
        request.mc_version,
        log,
        on_progress=on_progress,
        loader_version=request.loader_version,
        installer_version=request.installer_version,
    )

    is_forge = request.server_type_id == "forge"
    if is_forge:
        _finish_forge(request, server_dir, log)
    else:
        command = launch_scripts.build_java_command(result.jar_name, request.min_ram_mb, request.max_ram_mb)
        if request.use_mcdreforged:
            mcdreforged_setup.set_start_command(request.destination, command, log)
            launch_scripts.write_mcdreforged_launch_scripts(request.destination)
        else:
            launch_scripts.write_java_launch_scripts(server_dir, result.jar_name, request.min_ram_mb, request.max_ram_mb)

    log("Server setup complete.")
    return request.destination


def _finish_forge(request: ServerRequest, server_dir: Path, log: LogCallback) -> None:
    jvm_args_path = server_dir / "user_jvm_args.txt"
    jvm_args_path.write_text(f"-Xms{request.min_ram_mb}M -Xmx{request.max_ram_mb}M\n", encoding="utf-8")

    if request.use_mcdreforged:
        run_script = "run.bat" if (server_dir / "run.bat").exists() else "./run.sh"
        mcdreforged_setup.set_start_command(request.destination, run_script, log)
        launch_scripts.write_mcdreforged_launch_scripts(request.destination)
    else:
        command = "run.bat" if is_windows() else "run.sh"
        bat_path = server_dir / "start.bat"
        bat_path.write_text(f"{command}\r\npause\r\n", encoding="utf-8")
        sh_path = server_dir / "start.sh"
        sh_path.write_text(f"#!/bin/sh\n{command}\n", encoding="utf-8")
        if not is_windows():
            sh_path.chmod(sh_path.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
