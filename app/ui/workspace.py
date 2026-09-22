from PySide6.QtCore import QTimer, Signal
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from app.core.registry import registry
from app.core.settings import settings
from app.core.tool import Tool
from app.ui.tool_card import ToolCard


class Workspace(QWidget):
    tool_opened = Signal(object)  # emits Tool

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._category = "All"
        self._filter = ""

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.stack = QStackedWidget()
        layout.addWidget(self.stack)

        self.stack.addWidget(self._build_grid_page())
        self.stack.addWidget(self._build_tool_page())

        self._rebuild_grid()

    # ---- page construction ----

    def _build_grid_page(self) -> QWidget:
        page = QWidget()
        outer = QVBoxLayout(page)
        outer.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        outer.addWidget(scroll)

        self.grid_host = QWidget()
        self.grid = QGridLayout(self.grid_host)
        self.grid.setContentsMargins(24, 24, 24, 24)
        self.grid.setSpacing(16)
        scroll.setWidget(self.grid_host)

        return page

    def _build_tool_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        header = QFrame()
        header.setObjectName("ToolHeader")
        h = QHBoxLayout(header)
        h.setContentsMargins(16, 12, 16, 12)

        self.back_btn = QPushButton("←  Back")
        self.back_btn.setObjectName("BackButton")
        self.back_btn.clicked.connect(self.show_grid)
        h.addWidget(self.back_btn)

        self.tool_title = QLabel("")
        self.tool_title.setObjectName("ToolTitle")
        h.addWidget(self.tool_title)
        h.addStretch()

        layout.addWidget(header)

        self.tool_container = QWidget()
        self.tool_container_layout = QVBoxLayout(self.tool_container)
        self.tool_container_layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.tool_container, 1)

        return page

    # ---- grid logic ----

    def _visible_tools(self) -> list[Tool]:
        tools = registry.all()

        if self._category == "Favorites":
            favs = set(settings.favorites)
            tools = [t for t in tools if t.meta.id in favs]
        elif self._category != "All":
            tools = [t for t in tools if t.meta.category == self._category]

        if self._filter:
            q = self._filter.lower()
            tools = [
                t for t in tools
                if q in t.meta.name.lower()
                or q in t.meta.description.lower()
                or any(q in k.lower() for k in t.meta.keywords)
            ]

        return tools

    def _rebuild_grid(self) -> None:
        while self.grid.count():
            item = self.grid.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()

        tools = self._visible_tools()

        if not tools:
            msg = (
                "No favorites yet — click ☆ on any tool to add it here."
                if self._category == "Favorites"
                else "No tools match."
            )
            empty = QLabel(msg)
            empty.setObjectName("EmptyLabel")
            self.grid.addWidget(empty, 0, 0)
            return

        cols = 3
        for i, tool in enumerate(tools):
            card = ToolCard(tool)
            card.clicked.connect(self.open_tool)
            card.favorite_toggled.connect(self._on_favorite_toggled)
            self.grid.addWidget(card, i // cols, i % cols)

        self.grid.setRowStretch(self.grid.rowCount(), 1)

    # ---- public API ----

    def set_category(self, category: str) -> None:
        self._category = category
        self.show_grid()

    def set_filter(self, text: str) -> None:
        self._filter = text.strip()
        if self.stack.currentIndex() == 0:
            self._rebuild_grid()

    def show_grid(self) -> None:
        self.stack.setCurrentIndex(0)
        self._rebuild_grid()

    def open_tool(self, tool: Tool) -> None:
        while self.tool_container_layout.count():
            item = self.tool_container_layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()

        widget = tool.create_widget()
        self.tool_container_layout.addWidget(widget)

        self.tool_title.setText(f"{tool.meta.icon}   {tool.meta.name}")
        self.stack.setCurrentIndex(1)
        self.tool_opened.emit(tool)

    # ---- slots ----

    def _on_favorite_toggled(self, _tool: Tool, _is_fav: bool) -> None:
        # Only need to redraw if we're viewing the Favorites list;
        # the star on the card already updated itself in place.
        if self._category == "Favorites":
            QTimer.singleShot(0, self._rebuild_grid)