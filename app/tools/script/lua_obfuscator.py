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


PRESETS = ("Minify", "Weak", "Medium", "Strong")


# ---------------------------------------------------------------- discovery

def _npm_prefix() -> str | None:
    """Return the npm global prefix directory."""
    for npm in ("npm.cmd", "npm"):
        exe = shutil.which(npm)
        if not exe:
            continue
        try:
            proc = subprocess.run(
                [exe, "config", "get", "prefix"],
                capture_output=True,
                text=True,
                timeout=10,
                shell=False,
            )
            if proc.returncode == 0:
                path = proc.stdout.strip()
                if path and os.path.isdir(path):
                    return path
        except Exception:
            continue
    return None


def _find_prometheus_cli() -> list[str] | None:
    """
    Return a command prefix that invokes the Lua Prometheus CLI.

    Priority:
      1. `prometheus-cli` / `.cmd` on PATH
      2. npm global prefix folder
      3. npx pinned to the scoped package (auto-installs on first use)
    """
    # 1. On PATH
    for name in ("prometheus-cli.cmd", "prometheus-cli", "prometheus-cli.exe"):
        found = shutil.which(name)
        if found:
            return [found]

    # 2. npm global prefix
    prefix = _npm_prefix()
    if prefix:
        for name in ("prometheus-cli.cmd", "prometheus-cli", "prometheus-cli.ps1"):
            candidate = os.path.join(prefix, name)
            if os.path.isfile(candidate):
                return [candidate]

    # 3. npx fallback — scoped package pinned so it cannot grab the wrong one
    npx = shutil.which("npx.cmd") or shutil.which("npx")
    if npx:
        return [
            npx, "--yes",
            "--package=@gamely/prometheus-cli",
            "--", "prometheus-cli",
        ]

    return None


def _find_node() -> str | None:
    for name in ("node", "node.exe"):
        found = shutil.which(name)
        if found:
            return found
    return None


# --------------------------------------------------------------------- UI

class LuaObfuscatorWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(12)

        # Controls row
        controls = QHBoxLayout()
        controls.addWidget(QLabel("Preset:"))
        self.preset = QComboBox()
        self.preset.addItems(PRESETS)
        self.preset.setCurrentText("Minify")
        controls.addWidget(self.preset)

        self.run_btn = QPushButton("Obfuscate")
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

        # Split input / output
        splitter = QSplitter(Qt.Horizontal)

        left = QWidget()
        ll = QVBoxLayout(left)
        ll.setContentsMargins(0, 0, 0, 0)
        ll.addWidget(QLabel("Lua Source"))
        self.input = QPlainTextEdit()
        self.input.setPlaceholderText(
            '-- input.lua\nprint("Hello, DevVault")\n'
        )
        mono = QFont("Consolas")
        mono.setStyleHint(QFont.Monospace)
        mono.setPointSize(10)
        self.input.setFont(mono)
        ll.addWidget(self.input)
        splitter.addWidget(left)

        right = QWidget()
        rl = QVBoxLayout(right)
        rl.setContentsMargins(0, 0, 0, 0)
        rl.addWidget(QLabel("Obfuscated Output"))
        self.output = QPlainTextEdit()
        self.output.setReadOnly(True)
        self.output.setFont(mono)
        rl.addWidget(self.output)
        splitter.addWidget(right)

        splitter.setSizes([500, 500])
        layout.addWidget(splitter, 1)

        self._check_availability()

    # ---------------------------------------------------------- availability

    def _check_availability(self) -> None:
        if _find_prometheus_cli():
            self.set_status("✓ prometheus-cli available")
            return
        if _find_node():
            self.set_status(
                "⚠ Node found but prometheus-cli missing. Run: "
                "npm install -g @gamely/prometheus-cli",
                error=True,
            )
            return
        self.set_status(
            "⚠ Node.js not found. Install from nodejs.org, then run: "
            "npm install -g @gamely/prometheus-cli",
            error=True,
        )

    # ------------------------------------------------------------------ run

    def _run(self) -> None:
        source = self.input.toPlainText()
        if not source.strip():
            self.set_status("Nothing to obfuscate.", error=True)
            return

        preset = self.preset.currentText()
        base_cmd = _find_prometheus_cli()
        if base_cmd is None:
            self.set_status(
                "⚠ prometheus-cli not available. Run "
                "npm install -g @gamely/prometheus-cli",
                error=True,
            )
            return

        with tempfile.TemporaryDirectory() as tmp:
            in_path = os.path.join(tmp, "input.lua")
            out_path = os.path.join(tmp, "input.obfuscated.lua")

            with open(in_path, "w", encoding="utf-8") as f:
                f.write(source)

            # Record existing files so we can detect any new output file.
            before = set(os.listdir(tmp))

            # Pass --out explicitly so we control the destination. Older
            # builds ignore it and write next to the input anyway.
            cmd = [
                *base_cmd,
                in_path,
                "--preset", preset,
                "--out", out_path,
            ]

            proc = self._invoke(cmd, tmp)

            # If --out wasn't honored, fall back to scanning for new files.
            if not os.path.isfile(out_path) or os.path.getsize(out_path) == 0:
                after = set(os.listdir(tmp))
                new_files = [
                    f for f in (after - before)
                    if f.lower().endswith(".lua") and f != "input.lua"
                ]
                if new_files:
                    out_path = os.path.join(tmp, new_files[0])

            # Read the result
            result = None
            if os.path.isfile(out_path):
                with open(out_path, "r", encoding="utf-8", errors="replace") as f:
                    result = f.read()

            # Some builds print to stdout instead of writing a file.
            if not result and proc and proc.stdout.strip():
                result = proc.stdout

            if not result:
                stderr = ""
                if proc:
                    stderr = (proc.stderr or proc.stdout or "").strip()
                self.set_status(
                    f"⚠ No output. {stderr[:300]}", error=True
                )
                return

            self.output.setPlainText(result)
            self.set_status(f"✓ Obfuscated with preset '{preset}'")

    def _invoke(self, cmd: list[str], cwd: str):
        """Run the CLI and return CompletedProcess, or None on failure."""
        try:
            return subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=180,
                cwd=cwd,
                shell=False,
            )
        except subprocess.TimeoutExpired:
            self.set_status("⚠ Obfuscation timed out (180s).", error=True)
        except FileNotFoundError as exc:
            self.set_status(f"⚠ CLI not found: {exc}", error=True)
        except Exception as exc:
            self.set_status(f"⚠ {exc}", error=True)
        return None

    # -------------------------------------------------------------- helpers

    def _copy(self) -> None:
        QApplication.clipboard().setText(self.output.toPlainText())
        self.set_status("Copied ✓")

    def set_status(self, msg: str, error: bool = False) -> None:
        self.status.setText(msg)
        self.status.setProperty("error", error)
        self.status.style().unpolish(self.status)
        self.status.style().polish(self.status)


class LuaObfuscatorTool(Tool):
    meta = ToolMeta(
        id="script.lua_obfuscator",
        name="Lua Obfuscator",
        category="Script",
        icon="🛡️",
        description="Obfuscate Lua 5.1 / LuaU via Prometheus (Node CLI).",
        keywords=(
            "lua", "obfuscate", "prometheus", "protect", "minify",
            "luau", "roblox", "script",
        ),
    )

    def create_widget(self, parent=None):
        return LuaObfuscatorWidget(parent)