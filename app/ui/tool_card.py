from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QToolButton,
    QVBoxLayout,
)

from app.core.settings import settings
from app.core.tool import Tool


class ToolCard(QFrame):
    clicked = Signal(object)                # emits Tool
    favorite_toggled = Signal(object, bool)  # emits (Tool, is_favorite)

    def __init__(self, tool: Tool, parent=None) -> None:
        super().__init__(parent)
        self.tool = tool
        self.setObjectName("ToolCard")
        self.setCursor(Qt.PointingHandCursor)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 12, 16)
        layout.setSpacing(6)

        # Top row: icon + star
        top = QHBoxLayout()
        top.setContentsMargins(0, 0, 0, 0)

        icon = QLabel(tool.meta.icon)
        icon.setObjectName("CardIcon")
        top.addWidget(icon)
        top.addStretch()

        self.star = QToolButton()
        self.star.setObjectName("StarButton")
        self.star.setCursor(Qt.PointingHandCursor)
        self.star.setCheckable(True)
        self.star.setToolTip("Toggle favorite")
        self._sync_star(settings.is_favorite(tool.meta.id))
        self.star.clicked.connect(self._on_star_clicked)
        top.addWidget(self.star)

        layout.addLayout(top)

        name = QLabel(tool.meta.name)
        name.setObjectName("CardName")
        layout.addWidget(name)

        desc = QLabel(tool.meta.description)
        desc.setObjectName("CardDesc")
        desc.setWordWrap(True)
        layout.addWidget(desc)

        layout.addStretch()

    def _sync_star(self, is_fav: bool) -> None:
        self.star.setChecked(is_fav)
        self.star.setText("★" if is_fav else "☆")

    def _on_star_clicked(self) -> None:
        new_state = settings.toggle_favorite(self.tool.meta.id)
        self._sync_star(new_state)
        self.favorite_toggled.emit(self.tool, new_state)

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.tool)
        super().mousePressEvent(event)