"""Streaming HTTP downloads with progress callbacks and JSON helpers."""
from __future__ import annotations

from pathlib import Path
from typing import Callable, Optional

import requests

ProgressCallback = Optional[Callable[[int, int], None]]

USER_AGENT = "easy-mc-server/2.0"
DEFAULT_HEADERS = {"User-Agent": USER_AGENT}
CHUNK_SIZE = 1024 * 256


class DownloadError(RuntimeError):
    pass


def get_json(url: str, timeout: int = 15) -> dict | list:
    try:
        response = requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        raise DownloadError(f"Failed to fetch {url}: {exc}") from exc


def download_file(url: str, destination: Path, on_progress: ProgressCallback = None) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        with requests.get(url, headers=DEFAULT_HEADERS, stream=True, timeout=30) as response:
            response.raise_for_status()
            total = int(response.headers.get("Content-Length", 0))
            downloaded = 0
            with open(destination, "wb") as f:
                for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                    if not chunk:
                        continue
                    f.write(chunk)
                    downloaded += len(chunk)
                    if on_progress is not None:
                        on_progress(downloaded, total)
    except requests.RequestException as exc:
        raise DownloadError(f"Failed to download {url}: {exc}") from exc

    return destination
