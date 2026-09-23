import os
import shutil
import subprocess
import tempfile

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from app.core.tool import Tool, ToolMeta


class SubprocessObfuscatorWidget(QWidget):
    """
    Generic obfuscator widget.

    Subclasses set:
      - input_ext, output_ext, input_label, output_label,
        input_placeholder, run_label
      - presets: list of preset names, or None

    Subclasses implement:
      - build_command(in_path, out_path, preset) -> list[str]
      - tool_check() -> str | None
    """

    input_ext = ".txt"
    output_ext = ".txt"
    presets: list[str] | None = None
    input_label = "Source"
    output_label = "Obfuscated Output"
    input_placeholder = ""
    run_label = "Obfuscate"

    def build_command(
        self, in_path: str, out_path: str, preset: str | None
    ) -> list[str]:
        raise NotImplementedError

    def tool_check(self) -> str | None:
        return None

    @staticmethod
    def resolve_exe(*names: str) -> str | None:
        for name in names:
            found = shutil.which(name)
            if found:
                return found
        return None

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(12)

        controls = QHBoxLayout()

        if self.presets:
            controls.addWidget(QLabel("Preset:"))
            self.preset = QComboBox()
            self.preset.addItems(self.presets)
            controls.addWidget(self.preset)
        else:
            self.preset = None

        self.run_btn = QPushButton(self.run_label)
        self.run_btn.setObjectName("PrimaryButton")
        self.run_btn.clicked.connect(self._run)
        controls.addWidget(self.run_btn)

        self.copy_btn = QPushButton("Copy Output")
        self.copy_btn.clicked.connect(self._copy)
        controls.addWidget(self.copy_btn)

        controls.addStretch()
        self.status = QLabel("")
        self.status.setObjectName("StatusLabel")
        controls.addWidget(self.status)
        layout.addLayout(controls)

        splitter = QSplitter(Qt.Horizontal)

        left = QWidget()
        ll = QVBoxLayout(left)
        ll.setContentsMargins(0, 0, 0, 0)
        ll.addWidget(QLabel(self.input_label))
        self.input = QPlainTextEdit()
        self.input.setPlaceholderText(self.input_placeholder)
        mono = QFont("Consolas")
        mono.setStyleHint(QFont.Monospace)
        mono.setPointSize(10)
        self.input.setFont(mono)
        ll.addWidget(self.input)
        splitter.addWidget(left)

        right = QWidget()
        rl = QVBoxLayout(right)
        rl.setContentsMargins(0, 0, 0, 0)
        rl.addWidget(QLabel(self.output_label))
        self.output = QPlainTextEdit()
        self.output.setReadOnly(True)
        self.output.setFont(mono)
        rl.addWidget(self.output)
        splitter.addWidget(right)

        splitter.setSizes([500, 500])
        layout.addWidget(splitter, 1)

        self._check_availability()

    def _check_availability(self) -> None:
        err = self.tool_check()
        if err:
            self.set_status(err, error=True)
        else:
            self.set_status("✓ Ready")

    def _run(self) -> None:
        source = self.input.toPlainText()
        if not source.strip():
            self.set_status("Nothing to obfuscate.", error=True)
            return

        err = self.tool_check()
        if err:
            self.set_status(err, error=True)
            return

        preset = self.preset.currentText() if self.preset else None

        with tempfile.TemporaryDirectory() as tmp:
            in_path = os.path.join(tmp, f"input{self.input_ext}")
            out_path = os.path.join(tmp, f"output{self.output_ext}")

            with open(in_path, "w", encoding="utf-8") as f:
                f.write(source)

            cmd = self.build_command(in_path, out_path, preset)

            try:
                proc = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",     # <-- force UTF-8
                    errors="replace",      # <-- never crash on bad bytes
                    timeout=120,
                    cwd=tmp,
                    shell=False,
                )
            except subprocess.TimeoutExpired:
                self.set_status("⚠ Timed out (120s).", error=True)
                return
            except FileNotFoundError:
                self.set_status(
                    f"⚠ Tool not found: {cmd[0]}\n"
                    f"Restart DevVault from a terminal where "
                    f"`where.exe {os.path.basename(cmd[0])}` works.",
                    error=True,
                )
                return
            except Exception as exc:
                self.set_status(f"⚠ {type(exc).__name__}: {exc}", error=True)
                return

            # Read output file as utf-8, replacing bad bytes.
            result = None
            if os.path.isfile(out_path):
                try:
                    with open(
                        out_path, "r",
                        encoding="utf-8", errors="replace",
                    ) as f:
                        result = f.read()
                except Exception:
                    # Fall back to binary read if the file is odd
                    with open(out_path, "rb") as f:
                        result = f.read().decode("utf-8", errors="replace")

            if not result and proc.stdout.strip():
                result = proc.stdout

            if not result:
                stderr = (proc.stderr or proc.stdout or "").strip()
                self.set_status(f"⚠ No output. {stderr[:300]}", error=True)
                return

            self.output.setPlainText(result)
            self.set_status("✓ Done")

    def _copy(self) -> None:
        QApplication.clipboard().setText(self.output.toPlainText())
        self.set_status("Copied ✓")

    def set_status(self, msg: str, error: bool = False) -> None:
        self.status.setText(msg)
        self.status.setProperty("error", error)
        self.status.style().unpolish(self.status)
        self.status.style().polish(self.status)