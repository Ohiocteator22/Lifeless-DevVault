import sys

from PySide6.QtWidgets import QApplication

from app.core import theme
from app.core.settings import settings
from app.tools import register_all_tools
from app.ui.main_window import MainWindow


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("DevVault")
    app.setOrganizationName("DevVault")

    register_all_tools()
    theme.apply_theme(app, settings.theme)

    window = MainWindow()
    window.showFullScreen()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())