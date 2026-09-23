import shutil

from app.core.tool import Tool, ToolMeta
from app.tools.script.language_obfuscators import SubprocessObfuscatorWidget


class BatObfuscatorWidget(SubprocessObfuscatorWidget):
    input_ext = ".bat"
    output_ext = ".bat"
    input_label = "Batch Source"
    output_label = "Obfuscated Output"
    input_placeholder = "@echo off\necho hello"

    def tool_check(self) -> str | None:
        if not shutil.which("python") and not shutil.which("python.exe"):
            return "⚠ Python required for BatchCrypt"
        return None

    def build_command(self, in_path, out_path, preset):
        # Requires BatchCrypt.py to be reachable from cwd or PATH.
        # See note at the bottom of the file for setup.
        return ["python", "BatchCrypt.py", in_path, out_path]


class BatObfuscatorTool(Tool):
    meta = ToolMeta(
        id="script.bat_obfuscator",
        name="Batch Obfuscator",
        category="Script",
        icon="🖥️",
        description="Obfuscate .bat files via BatchCrypt (Python).",
        keywords=(
            "batch", "bat", "cmd", "obfuscate", "batchcrypt", "script",
        ),
    )

    def create_widget(self, parent=None):
        return BatObfuscatorWidget(parent)