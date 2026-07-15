"""Generate start.bat / start.sh launch scripts for a configured server."""
from __future__ import annotations

import stat
from pathlib import Path

from .system_check import is_windows


def build_java_command(jar_name: str, min_ram_mb: str, max_ram_mb: str) -> str:
    return f"java -Xms{min_ram_mb}M -Xmx{max_ram_mb}M -jar {jar_name} nogui"


def write_java_launch_scripts(path: Path, jar_name: str, min_ram_mb: str, max_ram_mb: str) -> Path:
    command = build_java_command(jar_name, min_ram_mb, max_ram_mb)
    return _write_scripts(path, command)


def write_mcdreforged_launch_scripts(path: Path) -> Path:
    return _write_scripts(path, "python -m mcdreforged")


def write_forge_launch_scripts(path: Path) -> Path:
    script_name = "run.bat" if is_windows() else "run.sh"
    return _write_scripts(path, script_name)


def _write_scripts(path: Path, command: str) -> Path:
    bat_path = path / "start.bat"
    bat_path.write_text(f"{command}\r\npause\r\n", encoding="utf-8")

    sh_path = path / "start.sh"
    sh_path.write_text(f"#!/bin/sh\n{command}\n", encoding="utf-8")
    if not is_windows():
        current_mode = sh_path.stat().st_mode
        sh_path.chmod(current_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)

    return bat_path if is_windows() else sh_path
