from PySide6.QtCore import QTimer, Signal
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton

from app.core.clipboard import ClipboardMatch


class ClipboardBanner(QFrame):
    open_requested = Signal(str)   # tool_id
    dismissed = Signal(str)        # content hash
    never_show = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("ClipboardBanner")
        self.setVisible(False)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 10, 16, 10)
        layout.setSpacing(12)

        self.icon = QLabel("📋")
        self.icon.setObjectName("ClipboardIcon")
        layout.addWidget(self.icon)

        self.text = QLabel("")
        self.text.setObjectName("ClipboardText")
        layout.addWidget(self.text)

        layout.addStretch()

        self.open_btn = QPushButton("Open Tool")
        self.open_btn.setObjectName("PrimaryButton")
        self.open_btn.clicked.connect(self._on_open)
        layout.addWidget(self.open_btn)

        self.dismiss_btn = QPushButton("Dismiss")
        self.dismiss_btn.clicked.connect(self._on_dismiss)
        layout.addWidget(self.dismiss_btn)

        self.never_btn = QPushButton("Never Show")
        self.never_btn.clicked.connect(self._on_never)
        layout.addWidget(self.never_btn)

        self._tool_id: str | None = None
        self._content_hash: str | None = None

        self._hide_timer = QTimer(self)
        self._hide_timer.setSingleShot(True)
        self._hide_timer.timeout.connect(self._on_dismiss)

    def show_match(self, match: ClipboardMatch, content_hash: str) -> None:
        self._tool_id = match.tool_id
        self._content_hash = content_hash
        self.icon.setText(match.icon)
        self.text.setText(f"Detected <b>{match.label}</b> in clipboard")
        self.open_btn.setVisible(match.tool_id is not None)
        self.setVisible(True)
        self._hide_timer.start(15000)

    def _on_open(self) -> None:
        if self._tool_id:
            self.open_requested.emit(self._tool_id)
        self._on_dismiss()

    def _on_dismiss(self) -> None:
        if self._content_hash:
            self.dismissed.emit(self._content_hash)
        self.setVisible(False)
        self._hide_timer.stop()

    def _on_never(self) -> None:
        self.never_show.emit()
        self.setVisible(False)
        self._hide_timer.stop()