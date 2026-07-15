"""Run external processes (java installers) while streaming their output live."""
from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Callable

LogCallback = Callable[[str], None]


class ProcessError(RuntimeError):
    pass


def run_streaming(args: list[str], cwd: Path, log: LogCallback) -> int:
    log(f"$ {' '.join(args)}")
    try:
        process = subprocess.Popen(
            args,
            cwd=str(cwd),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
    except OSError as exc:
        raise ProcessError(f"Failed to start process: {exc}") from exc

    assert process.stdout is not None
    for line in process.stdout:
        log(line.rstrip())

    return_code = process.wait()
    if return_code != 0:
        raise ProcessError(f"Process exited with code {return_code}")
    return return_code
