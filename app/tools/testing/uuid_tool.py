import uuid as uuid_mod

from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from app.core.tool import Tool, ToolMeta


class UuidWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(12)

        controls = QHBoxLayout()
        controls.addWidget(QLabel("Count:"))
        self.count = QSpinBox()
        self.count.setRange(1, 1000)
        self.count.setValue(5)
        controls.addWidget(self.count)

        self.gen_btn = QPushButton("Generate")
        self.gen_btn.setObjectName("PrimaryButton")
        self.gen_btn.clicked.connect(self._generate)
        controls.addWidget(self.gen_btn)

        self.copy_btn = QPushButton("Copy All")
        self.copy_btn.clicked.connect(self._copy)
        controls.addWidget(self.copy_btn)

        controls.addStretch()
        layout.addLayout(controls)

        self.output = QPlainTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output, 1)

        self._generate()

    def _generate(self) -> None:
        n = self.count.value()
        lines = [str(uuid_mod.uuid4()) for _ in range(n)]
        self.output.setPlainText("\n".join(lines))

    def _copy(self) -> None:
        QApplication.clipboard().setText(self.output.toPlainText())


class UuidTool(Tool):
    meta = ToolMeta(
        id="testing.uuid",
        name="UUID Generator",
        category="Testing",
        icon="🧪",
        description="Generate v4 UUIDs in bulk.",
        keywords=("uuid", "guid", "generate", "random", "id"),
    )

    def create_widget(self, parent=None):
        return UuidWidget(parent)