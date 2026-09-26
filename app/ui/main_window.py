from PySide6.QtCore import QEvent, Qt, QTimer
from PySide6.QtGui import QIcon, QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLineEdit,
    QMainWindow,
    QStackedWidget,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from app.core import theme
from app.core.clipboard import fingerprint
from app.core.registry import registry
from app.core.resources import app_icon_path
from app.core.settings import settings
from app.core.updater import UpdateChecker
from app.ui.clipboard_banner import ClipboardBanner
from app.ui.palette_page import PalettePage
from app.ui.sidebar import Sidebar
from app.ui.update_banner import UpdateBanner
from app.ui.workspace import Workspace


PALETTE_WIDTH = 640
PALETTE_HEIGHT = 420


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("DevVault")

        # Window icon (taskbar, alt-tab thumbnail)
        _icon_path = app_icon_path()
        if _icon_path:
            self.setWindowIcon(QIcon(_icon_path))

        # Borderless window — always either fullscreen or small centered.
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setMinimumSize(400, 300)

        # Top-level stack: normal view (0) and palette view (1)
        self.central_stack = QStackedWidget()
        self.setCentralWidget(self.central_stack)

        # --- page 0: normal layout ---
        self.normal_page = self._build_normal_page()
        self.central_stack.addWidget(self.normal_page)

        # --- page 1: palette ---
        self.palette_page = PalettePage()
        self.palette_page.tool_chosen.connect(self._on_palette_tool_chosen)
        self.palette_page.cancelled.connect(self._exit_palette_mode)
        self.central_stack.addWidget(self.palette_page)

        self._palette_mode = False
        self._last_clipboard_hash: str | None = None
        self._update_thread: UpdateChecker | None = None

        # Shortcuts
        QShortcut(
            QKeySequence("Ctrl+K"), self, activated=self._enter_palette_mode
        )

        # Kick off the update check after the window is drawn.
        QTimer.singleShot(2500, self._check_for_updates)

    # ---------------- normal page ----------------

    def _build_normal_page(self) -> QWidget:
        page = QWidget()
        root = QHBoxLayout(page)
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
        self.top_bar = self._build_top_bar()
        right_layout.addWidget(self.top_bar)

        # Update banner (hidden by default)
        self.update_banner = UpdateBanner()
        self.update_banner.skip_requested.connect(self._on_update_skip)
        self.update_banner.dismissed.connect(self._on_update_dismissed)
        right_layout.addWidget(self.update_banner)

        # Clipboard banner (hidden by default)
        self.clipboard_banner = ClipboardBanner()
        self.clipboard_banner.open_requested.connect(self._open_tool_by_id)
        self.clipboard_banner.dismissed.connect(self._on_clipboard_dismissed)
        self.clipboard_banner.never_show.connect(self._on_clipboard_never)
        right_layout.addWidget(self.clipboard_banner)

        # Workspace
        self.workspace = Workspace()
        right_layout.addWidget(self.workspace, 1)

        root.addWidget(right, 1)

        # Wiring
        self.sidebar.category_selected.connect(self._on_category)
        self.workspace.tool_opened.connect(self._on_tool_opened)

        return page

    def _build_top_bar(self) -> QFrame:
        bar = QFrame()
        bar.setObjectName("TopBar")
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(16, 12, 16, 12)

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search tools…   (or press Ctrl+K)")
        self.search.setObjectName("SearchBar")
        layout.addWidget(self.search, 1)

        palette_btn = QToolButton()
        palette_btn.setObjectName("IconButton")
        palette_btn.setText("⌘")
        palette_btn.setToolTip("Command palette (Ctrl+K)")
        palette_btn.clicked.connect(self._enter_palette_mode)
        layout.addWidget(palette_btn)

        self.theme_btn = QToolButton()
        self.theme_btn.setObjectName("IconButton")
        self.theme_btn.setText("🌙" if settings.theme == "dark" else "☀️")
        self.theme_btn.clicked.connect(self._toggle_theme)
        layout.addWidget(self.theme_btn)

        # Window controls (frameless window needs its own buttons)
        min_btn = QToolButton()
        min_btn.setObjectName("IconButton")
        min_btn.setText("—")
        min_btn.setToolTip("Minimize")
        min_btn.clicked.connect(self.showMinimized)
        layout.addWidget(min_btn)

        close_btn = QToolButton()
        close_btn.setObjectName("IconButton")
        close_btn.setText("✕")
        close_btn.setToolTip("Close")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)

        self.search.textChanged.connect(self._on_search)

        return bar

    # ---------------- palette mode ----------------

    def _enter_palette_mode(self) -> None:
        if self._palette_mode:
            return
        self._palette_mode = True

        self.central_stack.setCurrentIndex(1)
        self.palette_page.activate()

        self.setWindowState(Qt.WindowNoState)
        screen = QApplication.primaryScreen().availableGeometry()
        w, h = PALETTE_WIDTH, PALETTE_HEIGHT
        x = screen.x() + (screen.width() - w) // 2
        y = screen.y() + (screen.height() - h) // 3
        self.setGeometry(x, y, w, h)
        self.raise_()
        self.activateWindow()

    def _exit_palette_mode(self) -> None:
        if not self._palette_mode:
            return
        self._palette_mode = False

        self.central_stack.setCurrentIndex(0)
        self.setWindowState(Qt.WindowFullScreen)
        self.showFullScreen()

    def _on_palette_tool_chosen(self, tool) -> None:
        self._exit_palette_mode()
        self.workspace.open_tool(tool)

    # ---------------- search / theme ----------------

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

    # ---------------- clipboard ----------------

    def changeEvent(self, event) -> None:
        super().changeEvent(event)
        if (
            event.type() == QEvent.ActivationChange
            and self.isActiveWindow()
            and settings.clipboard_enabled
            and not self._palette_mode
        ):
            self._check_clipboard()

    def _check_clipboard(self) -> None:
        text = QApplication.clipboard().text()
        if not text:
            return

        import hashlib

        h = hashlib.sha256(
            text.encode("utf-8", errors="replace")
        ).hexdigest()[:16]

        if h == self._last_clipboard_hash:
            return
        if h in settings.clipboard_dismissed:
            return

        match = fingerprint(text)
        if not match:
            return

        self._last_clipboard_hash = h
        self.clipboard_banner.show_match(match, h)

    def _on_clipboard_dismissed(self, content_hash: str) -> None:
        dismissed = settings.clipboard_dismissed
        if content_hash not in dismissed:
            dismissed.append(content_hash)
        settings.clipboard_dismissed = dismissed

    def _on_clipboard_never(self) -> None:
        settings.clipboard_enabled = False
        self.clipboard_banner.setVisible(False)

    def _open_tool_by_id(self, tool_id: str) -> None:
        tool = registry.get(tool_id)
        if tool is None:
            return
        text = QApplication.clipboard().text()
        self.workspace.open_tool(tool, prefill=text)

    # ---------------- updates ----------------

    def _check_for_updates(self) -> None:
        if not settings.update_check_enabled:
            return
        # Avoid stacking checks
        if self._update_thread is not None and self._update_thread.isRunning():
            return

        self._update_thread = UpdateChecker(self)
        self._update_thread.result.connect(self._on_update_result)
        self._update_thread.finished.connect(self._on_update_thread_finished)
        self._update_thread.start()

    def _on_update_result(self, data) -> None:
        if not data:
            return

        version = data.get("version", "")
        url = data.get("url", "")
        title = data.get("title", "")

        if not version or not url:
            return

        # Respect "Skip This Version"
        if settings.skipped_version == version:
            return

        self.update_banner.show_update(version, url, title)

    def _on_update_thread_finished(self) -> None:
        # Drop our reference so the thread can be GC'd
        self._update_thread = None

    def _on_update_skip(self, version: str) -> None:
        settings.skipped_version = version

    def _on_update_dismissed(self) -> None:
        # "Later" — no persistence, banner just hides
        pass

    # ---------------- keys ----------------

    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key_Escape and self._palette_mode:
            self._exit_palette_mode()
            return
        super().keyPressEvent(event)

    def closeEvent(self, event) -> None:
        # Let the checker thread finish cleanly if it's still running.
        if self._update_thread is not None and self._update_thread.isRunning():
            self._update_thread.quit()
            self._update_thread.wait(1500)
        QApplication.quit()
        super().closeEvent(event)