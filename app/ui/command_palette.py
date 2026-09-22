from PySide6.QtCore import QEvent, Qt, Signal
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
)

from app.core.registry import registry
from app.core.tool import Tool


class CommandPalette(QDialog):
    tool_chosen = Signal(object)  # emits Tool

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("CommandPalette")
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setModal(True)
        self.setFixedSize(560, 380)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.input = QLineEdit()
        self.input.setObjectName("PaletteInput")
        self.input.setPlaceholderText("Search tools…   ↑↓ navigate · Enter open · Esc close")
        self.input.textChanged.connect(self._refresh)
        self.input.returnPressed.connect(self._activate_current)
        self.input.installEventFilter(self)
        layout.addWidget(self.input)

        self.list = QListWidget()
        self.list.setObjectName("PaletteList")
        self.list.itemActivated.connect(self._activate_item)
        self.list.itemClicked.connect(self._activate_item)
        layout.addWidget(self.list, 1)

        hint = QLabel("Tip: press Ctrl+K anywhere in DevVault to open this palette.")
        hint.setObjectName("PaletteHint")
        layout.addWidget(hint)

        self._refresh("")
        self.input.setFocus()

    # ---- data ----

    def _refresh(self, query: str) -> None:
        self.list.clear()
        results = registry.search(query) if query else registry.all()
        for tool in results:
            item = QListWidgetItem(
                f"{tool.meta.icon}   {tool.meta.name}     ·  {tool.meta.category}"
            )
            item.setData(Qt.UserRole, tool.meta.id)
            self.list.addItem(item)
        if self.list.count():
            self.list.setCurrentRow(0)

    # ---- activation ----

    def _activate_current(self) -> None:
        item = self.list.currentItem()
        if item is not None:
            self._activate_item(item)

    def _activate_item(self, item: QListWidgetItem) -> None:
        tool_id = item.data(Qt.UserRole)
        tool: Tool | None = registry.get(tool_id)
        if tool is not None:
            self.tool_chosen.emit(tool)
        self.accept()

    # ---- keys ----

    def eventFilter(self, obj, event) -> bool:
        if obj is self.input and event.type() == QEvent.KeyPress:
            key = event.key()
            if key == Qt.Key_Down and self.list.count():
                self.list.setFocus()
                self.list.setCurrentRow(min(1, self.list.count() - 1))
                return True
            if key == Qt.Key_Up and self.list.count():
                self.list.setFocus()
                self.list.setCurrentRow(self.list.count() - 1)
                return True
        return super().eventFilter(obj, event)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Escape:
            self.reject()
            return
        super().keyPressEvent(event)