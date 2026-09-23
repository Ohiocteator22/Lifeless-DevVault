from app.core.tool import Tool, ToolMeta
from app.tools.script.language_obfuscators import SubprocessObfuscatorWidget


# Levels supported by psobf v2.0.1
POWER_SHELL_PRESETS = [
    "1",  # Char join
    "2",  # Base64
    "3",  # Base64 (alternate)
    "4",  # GZip + Base64
    "5",  # Script fragmentation
    "6",  # AES-256 CTR
]


class PsObfuscatorWidget(SubprocessObfuscatorWidget):
    input_ext = ".ps1"
    output_ext = ".ps1"
    input_label = "PowerShell Source"
    output_label = "Obfuscated Output"
    input_placeholder = "Write-Host 'hello'"
    presets = POWER_SHELL_PRESETS

    def _exe(self) -> str | None:
        return self.resolve_exe("psobf.exe", "psobf.cmd", "psobf")

    def tool_check(self) -> str | None:
        if not self._exe():
            return (
                "⚠ Install: go install "
                "github.com/TaurusOmar/psobf/v2/cmd/psobf@v2.0.1"
            )
        return None

    def build_command(self, in_path, out_path, preset):
        exe = self._exe() or "psobf"
        level = preset if preset else "2"
        return [
            exe,
            "-i", in_path,
            "-o", out_path,
            "-level", level,
        ]


class PsObfuscatorTool(Tool):
    meta = ToolMeta(
        id="script.ps_obfuscator",
        name="PowerShell Obfuscator",
        category="Script",
        icon="⚡",
        description="Obfuscate PowerShell scripts via psobf (6 levels).",
        keywords=(
            "powershell", "ps1", "obfuscate", "psobf", "script", "windows",
        ),
    )

    def create_widget(self, parent=None):
        return PsObfuscatorWidget(parent)