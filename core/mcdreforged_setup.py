"""Helpers to install and initialize MCDReforged around a Minecraft server."""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

from .types import LogCallback

MCDR_PLACEHOLDER = "start_command: echo Hello world from MCDReforged"


def is_mcdreforged_installed() -> bool:
    return shutil.which("mcdreforged") is not None


def install_mcdreforged(log: LogCallback) -> None:
    log("Installing MCDReforged via pip...")
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "mcdreforged"],
        check=True,
    )
    log("MCDReforged installed successfully.")


def init_mcdreforged(root_path: Path, log: LogCallback) -> Path:
    root_path.mkdir(parents=True, exist_ok=True)
    log(f"Initializing MCDReforged in {root_path}...")
    subprocess.run(
        [sys.executable, "-m", "mcdreforged", "init"],
        cwd=str(root_path),
        check=True,
    )
    log("MCDReforged initialized.")
    return root_path / "server"


def set_start_command(root_path: Path, start_command: str, log: LogCallback) -> None:
    config_path = root_path / "config.yml"
    content = config_path.read_text(encoding="utf-8")
    if MCDR_PLACEHOLDER in content:
        content = content.replace(MCDR_PLACEHOLDER, f"start_command: {start_command}")
        config_path.write_text(content, encoding="utf-8")
        log("MCDReforged start command configured.")
    else:
        log("Could not find the default start_command placeholder in config.yml; please set it manually.")
