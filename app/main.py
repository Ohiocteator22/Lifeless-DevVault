import sys
import os

# ----------------------------------------------------------------------
# Windows: give the process its own AppUserModelID BEFORE anything else.
# This is what makes the taskbar show OUR icon instead of python.exe's.
# Must run before QApplication is created.
# ----------------------------------------------------------------------
if sys.platform == "win32":
    import ctypes
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            "DevVault.Desktop.1"
        )
    except Exception:
        pass

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from app.core import theme
from app.core.resources import app_icon_path
from app.core.settings import settings
from app.tools import register_all_tools
from app.ui.main_window import MainWindow


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("DevVault")
    app.setOrganizationName("DevVault")
    # Also set the desktop file name — Qt uses this to match the AppUserModelID
    app.setDesktopFileName("DevVault")

    # Set app-wide icon
    icon_path = app_icon_path()
    if icon_path:
        app.setWindowIcon(QIcon(icon_path))

    register_all_tools()
    theme.apply_theme(app, settings.theme)

    window = MainWindow()
    window.showFullScreen()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())