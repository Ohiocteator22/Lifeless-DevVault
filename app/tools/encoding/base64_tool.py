import base64
import binascii

from app.core.tool import Tool, ToolMeta
from app.ui.transform_tool import TransformTool


class Base64Widget(TransformTool):
    input_label = "Text  →  Base64   (or paste Base64 to decode)"
    output_label = "Result"
    input_placeholder = "hello world"
    transform_label = "Encode"
    live = True

    def transform(self, text: str) -> str:
        if not text.strip():
            return ""
        # Heuristic: try to decode if it looks like base64
        stripped = text.strip()
        looks_b64 = (
            len(stripped) % 4 == 0
            and all(c.isalnum() or c in "+/=\n\r" for c in stripped)
            and any(c.isupper() or c.isdigit() or c in "+/=" for c in stripped)
        )
        if looks_b64:
            try:
                decoded = base64.b64decode(stripped, validate=True).decode("utf-8")
                return decoded
            except (binascii.Error, UnicodeDecodeError):
                pass
        return base64.b64encode(stripped.encode("utf-8")).decode("ascii")


class Base64Tool(Tool):
    meta = ToolMeta(
        id="encoding.base64",
        name="Base64",
        category="Encoding",
        icon="🔐",
        description="Encode or decode Base64 — auto-detects direction.",
        keywords=("base64", "encode", "decode", "b64"),
    )

    def create_widget(self, parent=None):
        return Base64Widget(parent)