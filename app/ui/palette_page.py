from PySide6.QtCore import QEvent, Qt, Signal
from PySide6.QtWidgets import (
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.core.registry import registry


class PalettePage(QWidget):
    tool_chosen = Signal(object)
    cancelled = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("PalettePage")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.input = QLineEdit()
        self.input.setObjectName("PaletteInput")
        self.input.setPlaceholderText(
            "Search tools…    ↑↓ navigate · Enter open · Esc close"
        )
        self.input.textChanged.connect(self._refresh)
        self.input.returnPressed.connect(self._activate_current)
        self.input.installEventFilter(self)
        layout.addWidget(self.input)

        self.list = QListWidget()
        self.list.setObjectName("PaletteList")
        self.list.itemActivated.connect(self._activate_item)
        self.list.itemClicked.connect(self._activate_item)
        self.list.installEventFilter(self)
        layout.addWidget(self.list, 1)

        hint = QLabel("Tip: press Ctrl+K anywhere to summon this palette.")
        hint.setObjectName("PaletteHint")
        layout.addWidget(hint)

        self._refresh("")

    def activate(self) -> None:
        self.input.clear()
        self._refresh("")
        self.input.setFocus()

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

    def _activate_current(self) -> None:
        item = self.list.currentItem()
        if item:
            self._activate_item(item)

    def _activate_item(self, item: QListWidgetItem) -> None:
        tool_id = item.data(Qt.UserRole)
        tool = registry.get(tool_id)
        if tool is not None:
            self.tool_chosen.emit(tool)

    def eventFilter(self, obj, event) -> bool:
        if event.type() != QEvent.KeyPress:
            return super().eventFilter(obj, event)
        key = event.key()

        if obj is self.input:
            if key == Qt.Key_Escape:
                self.cancelled.emit()
                return True
            if key == Qt.Key_Down and self.list.count():
                self.list.setFocus()
                self.list.setCurrentRow(min(1, self.list.count() - 1))
                return True
            if key == Qt.Key_Up and self.list.count():
                self.list.setFocus()
                self.list.setCurrentRow(self.list.count() - 1)
                return True

        if obj is self.list:
            if key == Qt.Key_Escape:
                self.cancelled.emit()
                return True
            if key in (Qt.Key_Return, Qt.Key_Enter):
                self._activate_current()
                return True
            if key == Qt.Key_Backspace:
                self.input.setFocus()
                self.input.backspace()
                return True
            if key in (Qt.Key_Up,) and self.list.currentRow() == 0:
                self.input.setFocus()
                return True

        return super().eventFilter(obj, event)