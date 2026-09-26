from PySide6.QtWidgets import QApplication


DARK_QSS = """
QMainWindow, QWidget {
    background: #1e1e2e;
    color: #cdd6f4;
    font-size: 13px;
}
QFrame#Sidebar {
    background: #181825;
    border-right: 1px solid #313244;
}
QLabel#Brand {
    color: #89b4fa;
    font-size: 15px;
    font-weight: 700;
    letter-spacing: 2px;
}
QPushButton#SidebarButton {
    background: transparent;
    color: #bac2de;
    text-align: left;
    padding: 8px 12px;
    border-radius: 6px;
    border: none;
}
QPushButton#SidebarButton:hover {
    background: #313244;
    color: #cdd6f4;
}
QPushButton#SidebarButton:checked {
    background: #313244;
    color: #89b4fa;
    font-weight: 600;
}
QFrame#TopBar {
    background: #1e1e2e;
    border-bottom: 1px solid #313244;
}
QLineEdit#SearchBar {
    background: #181825;
    color: #cdd6f4;
    border: 1px solid #313244;
    border-radius: 8px;
    padding: 8px 12px;
    selection-background-color: #89b4fa;
}
QLineEdit#SearchBar:focus {
    border: 1px solid #89b4fa;
}
QToolButton#IconButton {
    background: transparent;
    border: none;
    font-size: 16px;
    padding: 6px 10px;
    border-radius: 6px;
}
QToolButton#IconButton:hover {
    background: #313244;
}
QFrame#ToolCard {
    background: #181825;
    border: 1px solid #313244;
    border-radius: 10px;
    min-height: 130px;
}
QFrame#ToolCard:hover {
    background: #232336;
    border: 1px solid #89b4fa;
}
QLabel#CardIcon { font-size: 22px; }
QLabel#CardName {
    font-size: 14px;
    font-weight: 600;
    color: #cdd6f4;
}
QLabel#CardDesc {
    color: #7f849c;
    font-size: 12px;
}
QToolButton#StarButton {
    background: transparent;
    border: none;
    color: #f9e2af;
    font-size: 18px;
    padding: 0 2px;
}
QToolButton#StarButton:hover { color: #fab387; }
QLabel#EmptyLabel {
    color: #7f849c;
    font-size: 14px;
}
QFrame#ToolHeader {
    background: #1e1e2e;
    border-bottom: 1px solid #313244;
}
QLabel#ToolTitle {
    font-size: 15px;
    font-weight: 600;
    color: #cdd6f4;
    padding-left: 8px;
}
QPushButton#BackButton {
    background: transparent;
    color: #89b4fa;
    border: none;
    padding: 6px 10px;
    border-radius: 6px;
}
QPushButton#BackButton:hover {
    background: #313244;
}
QPushButton {
    background: #313244;
    color: #cdd6f4;
    border: 1px solid #45475a;
    border-radius: 6px;
    padding: 7px 14px;
}
QPushButton:hover { background: #45475a; }
QPushButton#PrimaryButton {
    background: #89b4fa;
    color: #1e1e2e;
    border: none;
    font-weight: 600;
}
QPushButton#PrimaryButton:hover { background: #b4befe; }
QPlainTextEdit {
    background: #181825;
    color: #cdd6f4;
    border: 1px solid #313244;
    border-radius: 8px;
    padding: 8px;
    selection-background-color: #89b4fa;
}
QPlainTextEdit:focus { border: 1px solid #89b4fa; }
QLabel#StatusLabel { color: #a6e3a1; }
QLabel#StatusLabel[error="true"] { color: #f38ba8; }
QLabel { color: #bac2de; }
QScrollArea { border: none; }
QScrollBar:vertical {
    background: #181825;
    width: 10px;
    margin: 0;
}
QScrollBar::handle:vertical {
    background: #45475a;
    border-radius: 5px;
    min-height: 30px;
}
QScrollBar::handle:vertical:hover { background: #585b70; }
QScrollBar::add-line, QScrollBar::sub-line { height: 0; }
QSplitter::handle { background: #313244; }

/* Info banners (clipboard + update) */
QFrame#ClipboardBanner, QFrame#UpdateBanner {
    background: #313244;
    border-bottom: 1px solid #45475a;
}
QLabel#ClipboardIcon { font-size: 18px; }
QLabel#ClipboardText { color: #cdd6f4; font-size: 13px; }

/* Palette page */
QWidget#PalettePage { background: #1e1e2e; }
QLineEdit#PaletteInput {
    background: #181825;
    color: #cdd6f4;
    border: none;
    border-bottom: 1px solid #313244;
    padding: 14px 16px;
    font-size: 15px;
    selection-background-color: #89b4fa;
}
QListWidget#PaletteList {
    background: #1e1e2e;
    border: none;
    outline: none;
    padding: 6px;
}
QListWidget#PaletteList::item {
    padding: 10px 12px;
    border-radius: 6px;
    color: #cdd6f4;
}
QListWidget#PaletteList::item:selected {
    background: #313244;
    color: #89b4fa;
}
QLabel#PaletteHint {
    color: #7f849c;
    padding: 6px 12px;
    font-size: 11px;
}
"""


LIGHT_QSS = """
QMainWindow, QWidget {
    background: #eff1f5;
    color: #4c4f69;
    font-size: 13px;
}
QFrame#Sidebar {
    background: #e6e9ef;
    border-right: 1px solid #ccd0da;
}
QLabel#Brand {
    color: #1e66f5;
    font-size: 15px;
    font-weight: 700;
    letter-spacing: 2px;
}
QPushButton#SidebarButton {
    background: transparent;
    color: #5c5f77;
    text-align: left;
    padding: 8px 12px;
    border-radius: 6px;
    border: none;
}
QPushButton#SidebarButton:hover { background: #ccd0da; }
QPushButton#SidebarButton:checked {
    background: #ccd0da;
    color: #1e66f5;
    font-weight: 600;
}
QFrame#TopBar {
    background: #eff1f5;
    border-bottom: 1px solid #ccd0da;
}
QLineEdit#SearchBar {
    background: #ffffff;
    color: #4c4f69;
    border: 1px solid #ccd0da;
    border-radius: 8px;
    padding: 8px 12px;
}
QLineEdit#SearchBar:focus { border: 1px solid #1e66f5; }
QToolButton#IconButton {
    background: transparent;
    border: none;
    font-size: 16px;
    padding: 6px 10px;
    border-radius: 6px;
}
QToolButton#IconButton:hover { background: #ccd0da; }
QFrame#ToolCard {
    background: #ffffff;
    border: 1px solid #ccd0da;
    border-radius: 10px;
    min-height: 130px;
}
QFrame#ToolCard:hover { border: 1px solid #1e66f5; }
QLabel#CardIcon { font-size: 22px; }
QLabel#CardName { font-size: 14px; font-weight: 600; }
QLabel#CardDesc { color: #6c6f85; font-size: 12px; }
QToolButton#StarButton {
    background: transparent;
    border: none;
    color: #df8e1d;
    font-size: 18px;
    padding: 0 2px;
}
QToolButton#StarButton:hover { color: #fe640b; }
QFrame#ToolHeader {
    background: #eff1f5;
    border-bottom: 1px solid #ccd0da;
}
QLabel#ToolTitle { font-size: 15px; font-weight: 600; padding-left: 8px; }
QPushButton#BackButton {
    background: transparent;
    color: #1e66f5;
    border: none;
    padding: 6px 10px;
    border-radius: 6px;
}
QPushButton#BackButton:hover { background: #ccd0da; }
QPushButton {
    background: #e6e9ef;
    color: #4c4f69;
    border: 1px solid #ccd0da;
    border-radius: 6px;
    padding: 7px 14px;
}
QPushButton:hover { background: #dce0e8; }
QPushButton#PrimaryButton {
    background: #1e66f5;
    color: #ffffff;
    border: none;
    font-weight: 600;
}
QPushButton#PrimaryButton:hover { background: #4f86f7; }
QPlainTextEdit {
    background: #ffffff;
    color: #4c4f69;
    border: 1px solid #ccd0da;
    border-radius: 8px;
    padding: 8px;
}
QPlainTextEdit:focus { border: 1px solid #1e66f5; }
QLabel#StatusLabel { color: #40a02b; }
QLabel#StatusLabel[error="true"] { color: #d20f39; }
QScrollArea { border: none; }
QSplitter::handle { background: #ccd0da; }

/* Info banners (clipboard + update) */
QFrame#ClipboardBanner, QFrame#UpdateBanner {
    background: #dce0e8;
    border-bottom: 1px solid #ccd0da;
}
QLabel#ClipboardIcon { font-size: 18px; }
QLabel#ClipboardText { color: #4c4f69; font-size: 13px; }

/* Palette page */
QWidget#PalettePage { background: #eff1f5; }
QLineEdit#PaletteInput {
    background: #ffffff;
    color: #4c4f69;
    border: none;
    border-bottom: 1px solid #ccd0da;
    padding: 14px 16px;
    font-size: 15px;
}
QListWidget#PaletteList {
    background: #eff1f5;
    border: none;
    outline: none;
    padding: 6px;
}
QListWidget#PaletteList::item {
    padding: 10px 12px;
    border-radius: 6px;
    color: #4c4f69;
}
QListWidget#PaletteList::item:selected {
    background: #dce0e8;
    color: #1e66f5;
}
QLabel#PaletteHint {
    color: #8c8fa1;
    padding: 6px 12px;
    font-size: 11px;
}
"""


def apply_theme(app: QApplication, name: str) -> None:
    app.setStyleSheet(DARK_QSS if name == "dark" else LIGHT_QSS)