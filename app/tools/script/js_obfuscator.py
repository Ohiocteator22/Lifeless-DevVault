from app.core.tool import Tool, ToolMeta
from app.tools.script.language_obfuscators import SubprocessObfuscatorWidget


class JsObfuscatorWidget(SubprocessObfuscatorWidget):
    input_ext = ".js"
    output_ext = ".js"
    input_label = "JavaScript Source"
    output_label = "Obfuscated Output"
    input_placeholder = "console.log('hello');"

    def _exe(self) -> str | None:
        return self.resolve_exe(
            "javascript-obfuscator.cmd",
            "javascript-obfuscator.exe",
            "javascript-obfuscator",
        )

    def tool_check(self) -> str | None:
        if not self._exe():
            return "⚠ Install: npm install -g javascript-obfuscator"
        return None

    def build_command(self, in_path, out_path, preset):
        exe = self._exe() or "javascript-obfuscator"
        return [
            exe,
            in_path,
            "--output",
            out_path,
            "--compact",
            "true",
            "--control-flow-flattening",
            "true",
            "--dead-code-injection",
            "true",
            "--string-array",
            "true",
        ]


class JsObfuscatorTool(Tool):
    meta = ToolMeta(
        id="script.js_obfuscator",
        name="JavaScript Obfuscator",
        category="Script",
        icon="📜",
        description="Obfuscate JS via javascript-obfuscator (npm).",
        keywords=("javascript", "js", "obfuscate", "node", "npm", "script"),
    )

    def create_widget(self, parent=None):
        return JsObfuscatorWidget(parent)