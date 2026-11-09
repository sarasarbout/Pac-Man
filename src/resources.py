"""Locate read-only resources in development and PyInstaller bundles."""

from pathlib import Path
import os
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    RESOURCE_ROOT = Path(getattr(sys, "_MEIPASS"))
else:
    RESOURCE_ROOT = PROJECT_ROOT


def resource_path(*parts: str) -> Path:
    """Return the path to a bundled resource or a development resource."""
    return RESOURCE_ROOT.joinpath(*parts)


def user_data_path(filename: str) -> Path:
    """Return a writable per-user path for persistent game data."""
    path = Path(filename)
    if path.is_absolute():
        return path

    if sys.platform == "win32":
        base = Path(
            os.environ.get(
                "APPDATA",
                Path.home() / "AppData" / "Roaming",
            )
        )
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        base = Path(
            os.environ.get(
                "XDG_DATA_HOME",
                Path.home() / ".local" / "share",
            )
        )

    data_dir = base / "Pacman Ghosts"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir / path
