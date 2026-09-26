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
        return tool_id in self.favorites

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
        self._s.setValue("clipboard_dismissed", value[-50:])

    # --- updates ------------------------------------------------------

    @property
    def update_check_enabled(self) -> bool:
        return self._s.value("update_check_enabled", True, type=bool)

    @update_check_enabled.setter
    def update_check_enabled(self, value: bool) -> None:
        self._s.setValue("update_check_enabled", value)

    @property
    def skipped_version(self) -> str:
        return self._s.value("skipped_version", "", type=str)

    @skipped_version.setter
    def skipped_version(self, value: str) -> None:
        self._s.setValue("skipped_version", value)


settings = AppSettings()