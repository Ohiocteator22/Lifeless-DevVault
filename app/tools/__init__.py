from app.core.registry import registry
from app.tools.data.json_formatter import JsonFormatterTool
from app.tools.encoding.base64_tool import Base64Tool
from app.tools.encoding.hash_tool import HashTool
from app.tools.script import register_script_tools
from app.tools.testing.uuid_tool import UuidTool


def register_all_tools() -> None:
    registry.register(JsonFormatterTool())
    registry.register(Base64Tool())
    registry.register(HashTool())
    registry.register(UuidTool())
    register_script_tools()