from dataclasses import dataclass
from typing import Tuple
from PySide6.QtWidgets import QWidget


@dataclass(frozen=True)
class ToolMeta:
    id: str
    name: str
    category: str
    icon: str = ""
    description: str = ""
    keywords: Tuple[str, ...] = ()


class Tool:
    """Base class for every DevVault tool."""

    meta: ToolMeta

    def create_widget(self, parent: QWidget | None = None) -> QWidget:
        raise NotImplementedError