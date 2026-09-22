from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLineEdit,
    QMainWindow,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from app.core import theme
from app.core.registry import registry
from app.core.settings import settings
from app.ui.command_palette import CommandPalette
from app.ui.sidebar import Sidebar
from app.ui.workspace import Workspace


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("DevVault")
        self.resize(1100, 720)

        central = QWidget()
        self.setCentralWidget(central)

        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self.sidebar = Sidebar()
        self.sidebar.set_categories(registry.categories())
        root.addWidget(self.sidebar)

        right = QWidget()
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        # Top bar
        top_bar = QFrame()
        top_bar.setObjectName("TopBar")
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(16, 12, 16, 12)

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search tools…   (or press Ctrl+K)")
        self.search.setObjectName("SearchBar")
        top_layout.addWidget(self.search, 1)

        self.palette_btn = QToolButton()
        self.palette_btn.setObjectName("IconButton")
        self.palette_btn.setText("⌘")
        self.palette_btn.setToolTip("Command palette (Ctrl+K)")
        self.palette_btn.clicked.connect(self._open_command_palette)
        top_layout.addWidget(self.palette_btn)

        self.theme_btn = QToolButton()
        self.theme_btn.setObjectName("IconButton")
        self.theme_btn.setText("🌙" if settings.theme == "dark" else "☀️")
        self.theme_btn.clicked.connect(self._toggle_theme)
        top_layout.addWidget(self.theme_btn)

        right_layout.addWidget(top_bar)

        self.workspace = Workspace()
        right_layout.addWidget(self.workspace, 1)

        root.addWidget(right, 1)

        # Wiring
        self.sidebar.category_selected.connect(self._on_category)
        self.search.textChanged.connect(self._on_search)
        self.workspace.tool_opened.connect(self._on_tool_opened)

        # Ctrl+K anywhere
        QShortcut(QKeySequence("Ctrl+K"), self, activated=self._open_command_palette)

    # ---- slots ----

    def _on_category(self, category: str) -> None:
        self.search.clear()
        self.workspace.set_category(category)

    def _on_search(self, text: str) -> None:
        if self.workspace.stack.currentIndex() != 0 and text:
            self.workspace.show_grid()
        self.workspace.set_filter(text)

    def _on_tool_opened(self, _tool) -> None:
        self.search.clear()

    def _toggle_theme(self) -> None:
        new_theme = "light" if settings.theme == "dark" else "dark"
        settings.theme = new_theme
        app = QApplication.instance()
        if app is not None:
            theme.apply_theme(app, new_theme)
        self.theme_btn.setText("🌙" if new_theme == "dark" else "☀️")

    # ---- command palette ----

    def _open_command_palette(self) -> None:
        palette = CommandPalette(self)
        palette.tool_chosen.connect(self.workspace.open_tool)

        # Center it near the top of the main window, Spotlight-style.
        self.adjustSize()  # ensure we have a fresh geometry
        geo = self.geometry()
        x = geo.x() + (geo.width() - palette.width()) // 2
        y = geo.y() + (geo.height() - palette.height()) // 3
        palette.move(x, y)

        palette.exec()