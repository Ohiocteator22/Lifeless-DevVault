from PySide6.QtCore import QUrl, Signal
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton


class UpdateBanner(QFrame):
    skip_requested = Signal(str)    # version to skip
    dismissed = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("UpdateBanner")
        self.setVisible(False)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 10, 16, 10)
        layout.setSpacing(12)

        self.icon = QLabel("🚀")
        self.icon.setObjectName("ClipboardIcon")
        layout.addWidget(self.icon)

        self.text = QLabel("")
        self.text.setObjectName("ClipboardText")
        layout.addWidget(self.text)

        layout.addStretch()

        self.view_btn = QPushButton("View Release")
        self.view_btn.setObjectName("PrimaryButton")
        self.view_btn.clicked.connect(self._on_view)
        layout.addWidget(self.view_btn)

        self.skip_btn = QPushButton("Skip This Version")
        self.skip_btn.clicked.connect(self._on_skip)
        layout.addWidget(self.skip_btn)

        self.dismiss_btn = QPushButton("Later")
        self.dismiss_btn.clicked.connect(self._on_dismiss)
        layout.addWidget(self.dismiss_btn)

        self._version: str = ""
        self._url: str = ""

    def show_update(self, version: str, url: str, title: str = "") -> None:
        self._version = version
        self._url = url
        label = f"DevVault <b>v{version}</b> is available"
        self.text.setText(label)
        self.setVisible(True)

    def _on_view(self) -> None:
        if self._url:
            QDesktopServices.openUrl(QUrl(self._url))
        self.setVisible(False)
        self.dismissed.emit()

    def _on_skip(self) -> None:
        self.skip_requested.emit(self._version)
        self.setVisible(False)

    def _on_dismiss(self) -> None:
        self.setVisible(False)
        self.dismissed.emit()