import hashlib

from app.core.tool import Tool, ToolMeta
from app.ui.transform_tool import TransformTool


ALGOS = ("md5", "sha1", "sha256", "sha384", "sha512")


class HashWidget(TransformTool):
    input_label = "Text to hash"
    output_label = "Hashes"
    input_placeholder = "Hello DevVault"
    transform_label = "Hash"
    live = True

    def transform(self, text: str) -> str:
        if not text:
            return ""
        data = text.encode("utf-8")
        lines = []
        for algo in ALGOS:
            h = hashlib.new(algo, data).hexdigest()
            lines.append(f"{algo.upper():<8}  {h}")
        return "\n".join(lines)


class HashTool(Tool):
    meta = ToolMeta(
        id="encoding.hash",
        name="Hash Generator",
        category="Encoding",
        icon="#️⃣",
        description="MD5, SHA-1, SHA-256, SHA-384, SHA-512.",
        keywords=("hash", "sha", "sha256", "md5", "digest", "checksum"),
    )

    def create_widget(self, parent=None):
        return HashWidget(parent)