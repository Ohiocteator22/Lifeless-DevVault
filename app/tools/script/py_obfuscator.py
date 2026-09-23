import shutil

from app.core.tool import Tool, ToolMeta
from app.tools.script.language_obfuscators import SubprocessObfuscatorWidget


class PyObfuscatorWidget(SubprocessObfuscatorWidget):
    input_ext = ".py"
    output_ext = ".py"
    input_label = "Python Source"
    output_label = "Obfuscated Output"
    input_placeholder = "print('hello')"

    def tool_check(self) -> str | None:
        if not shutil.which("pyobfus") and not shutil.which("pyobfus.cmd"):
            return "⚠ Install: pip install pyobfus"
        return None

    def build_command(self, in_path, out_path, preset):
        return ["pyobfus", in_path, "-o", out_path]


class PyObfuscatorTool(Tool):
    meta = ToolMeta(
        id="script.py_obfuscator",
        name="Python Obfuscator",
        category="Script",
        icon="🐍",
        description="Obfuscate Python via pyobfus (AST-based).",
        keywords=("python", "py", "obfuscate", "pyobfus", "script"),
    )

    def create_widget(self, parent=None):
        return PyObfuscatorWidget(parent)