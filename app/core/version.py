"""DevVault version — single source of truth."""

APP_VERSION = "1.2.0"


def parse_version(s: str) -> tuple[int, ...]:
    """
    Convert "v1.2.0" or "1.2.0-beta" into a comparable tuple (1, 2, 0).
    Non-numeric suffixes are dropped.
    """
    s = s.strip().lstrip("vV")
    parts: list[int] = []
    for chunk in s.split("."):
        num = ""
        for ch in chunk:
            if ch.isdigit():
                num += ch
            else:
                break
        parts.append(int(num) if num else 0)
    return tuple(parts)


def is_newer(remote: str, local: str = APP_VERSION) -> bool:
    """True if `remote` is a newer version than `local`."""
    return parse_version(remote) > parse_version(local)