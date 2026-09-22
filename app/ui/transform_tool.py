from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QSplitter,
    QVBoxLayout,
    QWidget,
)


MONO = QFont("Consolas")
MONO.setStyleHint(QFont.Monospace)
MONO.setPointSize(10)


class TransformTool(QWidget):
    """Base widget for any tool that maps input text -> output text."""

    input_label = "Input"
    output_label = "Output"
    input_placeholder = ""
    output_placeholder = ""
    transform_label = "Transform"
    live = False

    def transform(self, text: str) -> str:
        raise NotImplementedError

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(12)

        splitter = QSplitter(Qt.Horizontal)

        # Left: input
        left = QWidget()
        ll = QVBoxLayout(left)
        ll.setContentsMargins(0, 0, 0, 0)
        ll.setSpacing(6)
        ll.addWidget(QLabel(self.input_label))
        self.input = QPlainTextEdit()
        self.input.setPlaceholderText(self.input_placeholder)
        self.input.setFont(MONO)
        ll.addWidget(self.input, 1)
        splitter.addWidget(left)

        # Right: output
        right = QWidget()
        rl = QVBoxLayout(right)
        rl.setContentsMargins(0, 0, 0, 0)
        rl.setSpacing(6)
        rl.addWidget(QLabel(self.output_label))
        self.output = QPlainTextEdit()
        self.output.setPlaceholderText(self.output_placeholder)
        self.output.setFont(MONO)
        self.output.setReadOnly(True)
        rl.addWidget(self.output, 1)
        splitter.addWidget(right)

        splitter.setSizes([500, 500])
        layout.addWidget(splitter, 1)

        # Bottom controls
        controls = QHBoxLayout()
        self.run_btn = QPushButton(self.transform_label)
        self.run_btn.setObjectName("PrimaryButton")
        self.run_btn.clicked.connect(self.run)
        controls.addWidget(self.run_btn)

        self.copy_btn = QPushButton("Copy Output")
        self.copy_btn.clicked.connect(self.copy_output)
        controls.addWidget(self.copy_btn)

        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_all)
        controls.addWidget(self.clear_btn)

        controls.addStretch()
        self.status = QLabel("")
        self.status.setObjectName("StatusLabel")
        controls.addWidget(self.status)

        layout.addLayout(controls)

        if self.live:
            self.input.textChanged.connect(self.run)

    def run(self) -> None:
        text = self.input.toPlainText()
        try:
            result = self.transform(text)
            self.output.setPlainText(result)
            self.set_status("")
        except Exception as exc:
            self.output.setPlainText("")
            self.set_status(f"⚠ {exc}", error=True)

    def copy_output(self) -> None:
        QApplication.clipboard().setText(self.output.toPlainText())
        self.set_status("Copied ✓")

    def clear_all(self) -> None:
        self.input.clear()
        self.output.clear()
        self.set_status("")

    def set_status(self, msg: str, error: bool = False) -> None:
        self.status.setText(msg)
        self.status.setProperty("error", error)
        self.status.style().unpolish(self.status)
        self.status.style().polish(self.status)