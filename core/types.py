"""Shared type aliases used across the core package."""
from __future__ import annotations

from typing import Callable, Optional

LogCallback = Callable[[str], None]
ProgressCallback = Optional[Callable[[int, int], None]]
