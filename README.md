<div align="center">

# 🧰 DevVault

**A local, desktop-first developer toolbox.**

Stop opening 20 browser tabs for tiny developer tasks.

[![Release](https://img.shields.io/github/v/release/Ohiocteator22/Lifeless-DevVault?style=flat-square)](https://github.com/Ohiocteator22/DevVault/releases/latest)
[![Platform](https://img.shields.io/badge/platform-Windows-blue?style=flat-square)](#install)
[![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE)

</div>

---

## What is DevVault?

DevVault is a single, offline desktop app that puts all the tiny utilities developers constantly need in one place. No browser. No accounts. No data ever leaves your machine.

> **If it's a tiny developer task, it should already be here.**

![DevVault tool grid](docs/screenshot-grid.png)

---

## Features

### 🖥️ Shell

- Fullscreen, borderless UI with dark and light themes
- Category sidebar with Favorites
- Live search across tool names, descriptions, and keywords
- **Ctrl+K command palette** — Spotlight-style quick launcher

### 📦 Data

- **JSON Formatter** — pretty-print and validate JSON as you type

### 🔐 Encoding

- **Base64** — auto-detects encode vs decode direction
- **Hash Generator** — MD5, SHA-1, SHA-256, SHA-384, SHA-512

### 🧪 Testing

- **UUID Generator** — bulk v4 UUID generation

### 🛡️ Script

Local wrappers around external CLI obfuscators:

- **Lua** — via [Prometheus](https://github.com/prometheus-lua/Prometheus)
- **JavaScript** — via [javascript-obfuscator](https://github.com/javascript-obfuscator/javascript-obfuscator)
- **Python** — via [pyobfus](https://pypi.org/project/pyobfus/)
- **PowerShell** — via [psobf](https://github.com/TaurusOmar/psobf)

### 📋 Clipboard detection

When you focus DevVault with a recognized snippet on your clipboard, a banner appears offering to open the right tool with the content pre-filled. Detects JSON, JWTs, UUIDs, hashes, URLs, Base64, and source code in Lua / JavaScript / Python / PowerShell.

![Clipboard detection banner](docs/screenshot-clipboard.png)

---

## Install

### Download the portable build

1. Go to the [latest release](https://github.com/Ohiocteator22/DevVault/releases/latest)
2. Download `DevVault-v*-windows-x64.zip`
3. Extract anywhere
4. Double-click `DevVault.exe`

No installer, no Python required, no admin rights.

> **Windows SmartScreen may warn you** on first run because the binary is unsigned. Click **More info → Run anyway**.

### Run from source

```powershell
git clone https://github.com/Ohiocteator22/DevVault.git
cd DevVault
python -m venv .venv
.venv\Scripts\activate
pip install PySide6
python -m app.main
```

Requires Python 3.11+.

---

## Optional: obfuscator backends

The Script tab wraps external CLI tools. DevVault detects each one on your `PATH` and shows a friendly install hint if it's missing. Install whichever you need:

| Language   | Install                                                      |
| ---------- | ------------------------------------------------------------ |
| Lua        | `npm install -g @gamely/prometheus-cli`                      |
| JavaScript | `npm install -g javascript-obfuscator`                       |
| Python     | `pip install pyobfus`                                        |
| PowerShell | `go install github.com/TaurusOmar/psobf/v2/cmd/psobf@v2.0.1` |

**Notes:**

- The JavaScript obfuscator is the standard one from the `javascript-obfuscator` org, not the deprecated `prometheus-cli` npm package.
- `psobf` is written in Go and installs to `%USERPROFILE%\go\bin` — make sure that folder is on your PATH.
- Obfuscators run as subprocesses and never touch the network. Input and output stay entirely local.

---

## Keyboard shortcuts

| Shortcut   | Action                                     |
| ---------- | ------------------------------------------ |
| **Ctrl+K** | Open the command palette                   |
| **Esc**    | Close the palette and return to fullscreen |
| **↑ / ↓**  | Navigate the palette or the tool list      |
| **Enter**  | Open the highlighted tool                  |
| **Alt+F4** | Quit DevVault                              |

---

## Building from source

DevVault uses PyInstaller for a portable single-folder build.

```powershell
pip install pyinstaller
.\build.ps1
```

Output:

```text
dist/
└── DevVault/
    ├── DevVault.exe
    └── _internal/
```

Zip the folder to distribute:

```powershell
Compress-Archive -Path "dist\DevVault\*" -DestinationPath "DevVault-windows-x64.zip" -Force
```

### Regenerating the app icon

The multi-size ICO is built from the largest PNG in `assets/source/`:

```powershell
cd assets
python make_icon.py
```

---

## Project structure

```text
DevVault/
├── app/
│   ├── main.py                 # entry point + AppUserModelID
│   ├── core/                   # registry, settings, theme, clipboard, paths
│   ├── ui/                     # main window, sidebar, workspace, palette
│   └── tools/                  # individual tools grouped by category
│       ├── data/
│       ├── encoding/
│       ├── script/
│       └── testing/
├── assets/
│   ├── app_icon.ico            # built from source/
│   ├── make_icon.py
│   └── source/                 # high-res PNG sources
├── build.ps1                   # PyInstaller build script
├── DevVault.spec               # PyInstaller configuration
├── version_info.txt            # Windows EXE version resource
└── requirements.txt
```

### Adding a new tool

DevVault's tool registry means adding a tool is: create a class, register it, done.

```python
# app/tools/data/my_tool.py
from app.core.tool import Tool, ToolMeta
from app.ui.transform_tool import TransformTool


class MyToolWidget(TransformTool):
    input_label = "Input"
    output_label = "Output"

    def transform(self, text: str) -> str:
        return text.upper()


class MyTool(Tool):
    meta = ToolMeta(
        id="data.my_tool",
        name="My Tool",
        category="Data",
        icon="✨",
        description="Does something useful.",
        keywords=("my", "tool", "useful"),
    )

    def create_widget(self, parent=None):
        return MyToolWidget(parent)
```

Then in `app/tools/__init__.py`:

```python
registry.register(MyTool())
```

It appears in the sidebar, in search, in the command palette, and can be favorited — no other wiring required.

---

## Privacy

DevVault is **local-first** by design. Nothing you paste into it is sent anywhere.

```text
Your data  →  DevVault  →  Result
```

Not:

```text
Your data  →  Random website  →  Server  →  Result
```

The only network activity comes from tools that explicitly make requests (none currently). Obfuscators run as local subprocesses.

---

## License

MIT — see [LICENSE](LICENSE).

---

<div align="center">

Built because opening twenty tabs for two-second tasks is silly.

</div>
