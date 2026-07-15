"""System dependency checks: Java presence and version."""
from __future__ import annotations

import platform
import re
import shutil
import subprocess
from dataclasses import dataclass


@dataclass
class JavaStatus:
    installed: bool
    version: int | None
    raw_output: str
    path: str | None


def find_java_executable() -> str | None:
    return shutil.which("java")


def check_java(min_version: int = 21) -> JavaStatus:
    java_path = find_java_executable()
    if java_path is None:
        return JavaStatus(installed=False, version=None, raw_output="", path=None)

    try:
        result = subprocess.run(
            [java_path, "-version"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        raw_output = (result.stdout or "") + (result.stderr or "")
    except (subprocess.SubprocessError, OSError) as exc:
        return JavaStatus(installed=False, version=None, raw_output=str(exc), path=java_path)

    version = _parse_java_major_version(raw_output)
    return JavaStatus(installed=True, version=version, raw_output=raw_output, path=java_path)


def _parse_java_major_version(raw_output: str) -> int | None:
    match = re.search(r'version "?(\d+)(?:\.(\d+))?', raw_output)
    if not match:
        return None
    major = int(match.group(1))
    if major == 1 and match.group(2):
        return int(match.group(2))
    return major


def is_windows() -> bool:
    return platform.system() == "Windows"


def is_macos() -> bool:
    return platform.system() == "Darwin"


def is_linux() -> bool:
    return platform.system() == "Linux"
