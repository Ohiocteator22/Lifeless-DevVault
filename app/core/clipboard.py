import base64
import json
import re
from dataclasses import dataclass


@dataclass
class ClipboardMatch:
    kind: str            # internal identifier
    label: str           # human-readable name
    icon: str            # emoji to display in banner
    tool_id: str | None  # registry tool id to open, or None if no tool


def fingerprint(text: str) -> ClipboardMatch | None:
    """Best-effort detection of what the clipboard contains."""
    if not text:
        return None
    s = text.strip()
    if not s or len(s) > 500_000:
        return None

    # --- JSON ---------------------------------------------------------
    if (s.startswith("{") and s.endswith("}")) or (
        s.startswith("[") and s.endswith("]")
    ):
        try:
            json.loads(s)
            return ClipboardMatch("json", "JSON", "📦", "data.json_formatter")
        except Exception:
            pass

    # --- JWT ----------------------------------------------------------
    if re.fullmatch(r"eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+", s):
        return ClipboardMatch("jwt", "JWT", "🔑", None)

    # --- UUID ---------------------------------------------------------
    if re.fullmatch(
        r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-"
        r"[0-9a-fA-F]{4}-[0-9a-fA-F]{12}",
        s,
    ):
        return ClipboardMatch("uuid", "UUID", "🧪", "testing.uuid")

    # --- Hashes -------------------------------------------------------
    if re.fullmatch(r"[0-9a-fA-F]{64}", s):
        return ClipboardMatch("hash-sha256", "SHA-256 hash", "🔐", "encoding.hash")
    if re.fullmatch(r"[0-9a-fA-F]{40}", s):
        return ClipboardMatch("hash-sha1", "SHA-1 hash", "🔐", "encoding.hash")
    if re.fullmatch(r"[0-9a-fA-F]{32}", s):
        return ClipboardMatch("hash-md5", "MD5 hash", "🔐", "encoding.hash")

    # --- URL ----------------------------------------------------------
    if re.match(r"^https?://\S+$", s, re.IGNORECASE):
        return ClipboardMatch("url", "URL", "🌐", None)

    # --- Lua bytecode -------------------------------------------------
    if s.startswith("\x1bLua"):
        return ClipboardMatch("lua-bytecode", "Lua bytecode", "🌙", None)

    # --- Script languages (only if short enough to be script-like) ---
    if len(s) < 50_000:
        if re.search(r"\b(Write-Host|Get-\w+|\$\w+\s*=|\bparam\s*\()", s):
            return ClipboardMatch("ps", "PowerShell", "⚡", "script.ps_obfuscator")
        if re.search(r"^(def |class |import |from \w+ import )", s, re.MULTILINE):
            return ClipboardMatch("py", "Python", "🐍", "script.py_obfuscator")
        if re.search(r"^(local |function |--\[\[)", s, re.MULTILINE):
            return ClipboardMatch("lua", "Lua", "🛡️", "script.lua_obfuscator")
        if re.search(r"\b(function |const |let |=>)", s) and (
            ";" in s or "{" in s
        ):
            return ClipboardMatch("js", "JavaScript", "📜", "script.js_obfuscator")

    # --- Base64 (last, most generic) ----------------------------------
    if (
        len(s) >= 16
        and len(s) % 4 == 0
        and re.fullmatch(r"[A-Za-z0-9+/=\r\n]+", s)
    ):
        try:
            base64.b64decode(s, validate=True)
            return ClipboardMatch("base64", "Base64", "🔐", "encoding.base64")
        except Exception:
            pass

    return None