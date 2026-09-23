from app.core.registry import registry
from app.tools.script.lua_obfuscator import LuaObfuscatorTool
from app.tools.script.js_obfuscator import JsObfuscatorTool
from app.tools.script.py_obfuscator import PyObfuscatorTool
from app.tools.script.ps_obfuscator import PsObfuscatorTool
from app.tools.script.bat_obfuscator import BatObfuscatorTool


def register_script_tools() -> None:
    registry.register(LuaObfuscatorTool())
    registry.register(JsObfuscatorTool())
    registry.register(PyObfuscatorTool())
    registry.register(PsObfuscatorTool())
    registry.register(BatObfuscatorTool())