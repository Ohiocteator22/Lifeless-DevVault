import json

from app.core.tool import Tool, ToolMeta
from app.ui.transform_tool import TransformTool


class JsonFormatterWidget(TransformTool):
    input_label = "Raw JSON"
    output_label = "Formatted JSON"
    input_placeholder = '{"name":"DevVault","version":0.1,"features":["json","base64"]}'
    transform_label = "Format"
    live = True

    def transform(self, text: str) -> str:
        if not text.strip():
            return ""
        data = json.loads(text)
        return json.dumps(data, indent=2, ensure_ascii=False)


class JsonFormatterTool(Tool):
    meta = ToolMeta(
        id="data.json_formatter",
        name="JSON Formatter",
        category="Data",
        icon="📦",
        description="Pretty-print and validate JSON locally.",
        keywords=("json", "format", "pretty", "beautify", "validate"),
    )

    def create_widget(self, parent=None):
        return JsonFormatterWidget(parent)