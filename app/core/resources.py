import os
import sys


def resource_path(relative: str) -> str:
    """
    Return the absolute path to a bundled resource.

    Works both:
      - from source:   <project_root>/<relative>
      - from PyInstaller onedir: <exe_dir>/_internal/<relative>
      - from PyInstaller onefile: <extract_tmp>/<relative>
    """
    base = getattr(sys, "_MEIPASS", None)
    if base:
        return os.path.join(base, relative)
    # Dev fallback: project root is two levels up from app/core/
    project_root = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )
    return os.path.join(project_root, relative)


def app_icon_path() -> str | None:
    """Return the path to app_icon.ico if it exists, else None."""
    candidate = resource_path(os.path.join("assets", "app_icon.ico"))
    return candidate if os.path.isfile(candidate) else None