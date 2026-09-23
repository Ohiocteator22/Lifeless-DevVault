from typing import List
from PySide6.QtCore import QSettings


class AppSettings:
    def __init__(self) -> None:
        self._s = QSettings("DevVault", "DevVault")

    # --- theme --------------------------------------------------------

    @property
    def theme(self) -> str:
        return self._s.value("theme", "dark", type=str)

    @theme.setter
    def theme(self, value: str) -> None:
        self._s.setValue("theme", value)

    # --- favorites ----------------------------------------------------

    @property
    def favorites(self) -> List[str]:
        raw = self._s.value("favorites", [])
        if raw is None:
            return []
        if isinstance(raw, str):
            return [raw]
        return list(raw)

    @favorites.setter
    def favorites(self, value: List[str]) -> None:
        self._s.setValue("favorites", value)

    def is_favorite(self, tool_id: str) -> bool:
        return tool_id in self.favorites

    def toggle_favorite(self, tool_id: str) -> bool:
        favs = self.favorites
        if tool_id in favs:
            favs.remove(tool_id)
        else:
            favs.append(tool_id)
        self.favorites = favs
        return tool_id in favs

    # --- clipboard ----------------------------------------------------

    @property
    def clipboard_enabled(self) -> bool:
        return self._s.value("clipboard_enabled", True, type=bool)

    @clipboard_enabled.setter
    def clipboard_enabled(self, value: bool) -> None:
        self._s.setValue("clipboard_enabled", value)

    @property
    def clipboard_dismissed(self) -> List[str]:
        raw = self._s.value("clipboard_dismissed", [])
        if raw is None:
            return []
        if isinstance(raw, str):
            return [raw]
        return list(raw)

    @clipboard_dismissed.setter
    def clipboard_dismissed(self, value: List[str]) -> None:
        # Cap to last 50 to prevent unbounded growth
        self._s.setValue("clipboard_dismissed", value[-50:])


settings = AppSettings()