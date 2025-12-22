import sys
from pathlib import Path


def base_path() -> Path:
    """
    Returns correct base path for both:
    - normal python run
    - PyInstaller packaged app
    """
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parents[2]


def resource_path(relative_path: str) -> str:
    return str(base_path() / relative_path)
