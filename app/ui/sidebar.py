from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QButtonGroup,
    QFrame,
    QLabel,
    QPushButton,
    QVBoxLayout,
)


STATIC_ENTRIES = [
    ("All", "🧰  All Tools"),
    ("Favorites", "⭐  Favorites"),
]


class Sidebar(QFrame):
    category_selected = Signal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("Sidebar")
        self.setFixedWidth(220)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 16, 12, 16)
        layout.setSpacing(4)

        brand = QLabel("DEVVAULT")
        brand.setObjectName("Brand")
        layout.addWidget(brand)
        layout.addSpacing(12)

        self.group = QButtonGroup(self)
        self.group.setExclusive(True)

        for key, label in STATIC_ENTRIES:
            layout.addWidget(self._make_button(key, label))

        self._dynamic_layout = QVBoxLayout()
        self._dynamic_layout.setContentsMargins(0, 8, 0, 0)
        self._dynamic_layout.setSpacing(4)
        layout.addLayout(self._dynamic_layout)

        layout.addStretch()

    def _make_button(self, key: str, label: str) -> QPushButton:
        btn = QPushButton(label)
        btn.setObjectName("SidebarButton")
        btn.setCheckable(True)
        btn.clicked.connect(lambda _, k=key: self.category_selected.emit(k))
        self.group.addButton(btn)
        if key == "All":
            btn.setChecked(True)
        return btn

    def set_categories(self, categories: list[str]) -> None:
        icons = {
            "Text": "🔤",
            "Data": "📦",
            "Encoding": "🔐",
            "Time": "🕐",
            "Testing": "🧪",
            "Web": "🌐",
            "Utilities": "🛠",
        }
        for category in categories:
            label = f"{icons.get(category, '•')}  {category}"
            self._dynamic_layout.addWidget(self._make_button(category, label))