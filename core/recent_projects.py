"""Persists the list of recently created servers between sessions."""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

CONFIG_DIR = Path.home() / ".easy-mc-server"
RECENT_FILE = CONFIG_DIR / "recent_projects.json"
MAX_ENTRIES = 10


@dataclass
class RecentProject:
    name: str
    path: str
    server_type: str
    mc_version: str
    used_mcdreforged: bool


def load_recent() -> list[RecentProject]:
    if not RECENT_FILE.exists():
        return []
    try:
        raw = json.loads(RECENT_FILE.read_text(encoding="utf-8"))
        return [RecentProject(**entry) for entry in raw]
    except (json.JSONDecodeError, TypeError, ValueError):
        return []


def add_recent(project: RecentProject) -> None:
    entries = [p for p in load_recent() if p.path != project.path]
    entries.insert(0, project)
    entries = entries[:MAX_ENTRIES]

    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    RECENT_FILE.write_text(
        json.dumps([asdict(p) for p in entries], indent=2),
        encoding="utf-8",
    )
