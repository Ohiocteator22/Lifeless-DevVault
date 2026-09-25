# DevVault v1.1.0

_Released 2026-09-25_

This release turns DevVault from a collection of tools into a fast, keyboard-driven workspace. It adds a command palette, clipboard detection, a fullscreen borderless UI, four working script obfuscators, and proper Windows branding.

---

## ✨ Highlights

### Command palette (Ctrl+K)

Press `Ctrl+K` anywhere and the window shrinks into a centered Spotlight-style palette. Type to filter tools by name, description, or keyword. `↑↓` to navigate, `Enter` to open, `Esc` to cancel and return to fullscreen.

### Clipboard detection

Focus DevVault with a recognized snippet on your clipboard and a banner appears offering to open the right tool with the content already in the input box. Detects:

- JSON
- JWTs
- UUIDs
- MD5 / SHA-1 / SHA-256 hashes
- URLs
- Lua bytecode
- Base64
- Lua / JavaScript / Python / PowerShell source

Dismissals are remembered, and you can turn the feature off permanently from the banner.

### Fullscreen borderless UI

DevVault now launches fullscreen with no window chrome. Minimize and close live in the top bar. The palette mode temporarily shrinks the window to a centered 640×420 box — the earlier location/size glitches from the old dialog approach are gone.

### Proper Windows identity

The taskbar and Task Manager now show **DevVault** instead of `python.exe`, via `SetCurrentProcessExplicitAppUserModelID` and an embedded version resource. A multi-size `.ico` is embedded in the EXE and applied at runtime.

### Script tab — four working obfuscators

| Language   | Backend                  |
| ---------- | ------------------------ |
| Lua        | `@gamely/prometheus-cli` |
| JavaScript | `javascript-obfuscator`  |
| Python     | `pyobfus`                |
| PowerShell | `psobf` v2.0.1           |

Each tool auto-detects its backend on `PATH` and shows a friendly install hint if missing. All obfuscators run as local subprocesses — nothing touches the network.

---

## 🐛 Fixes

- **PowerShell obfuscator crash** — fixed `UnicodeDecodeError` when output contained non-ASCII bytes. All subprocess I/O now uses UTF-8 with error replacement.
- **Windows tool resolution** — subprocess calls now resolve `.cmd` / `.exe` shims explicitly via `shutil.which`, bypassing the `CreateProcess` extension quirk that caused "Tool not found" errors.

---

## 🗑️ Removed

- **Lua Deobfuscator** — Prometheus obfuscates source-level Lua, not bytecode. Feeding obfuscated source to `unluac` fails by design, so the tool was removed to avoid misleading users.

---

## 📦 Install

1. Download `DevVault-v1.1.0-windows-x64.zip` below
2. Extract anywhere
3. Double-click `DevVault.exe`

No installer, no Python, no admin rights.

> **Windows SmartScreen warning** — the binary is unsigned. Click **More Info → Run Anyway** on first launch.

---

## 🔧 Obfuscator backends

Install whichever you want to use:

| Language   | Install                                                      |
| ---------- | ------------------------------------------------------------ |
| Lua        | `npm install -g @gamely/prometheus-cli`                      |
| JavaScript | `npm install -g javascript-obfuscator`                       |
| Python     | `pip install pyobfus`                                        |
| PowerShell | `go install github.com/TaurusOmar/psobf/v2/cmd/psobf@v2.0.1` |

---

## ⌨️ Shortcuts

| Key        | Action                              |
| ---------- | ----------------------------------- |
| **Ctrl+K** | Command palette                     |
| **Esc**    | Close palette, return to fullscreen |
| **↑ / ↓**  | Navigate palette or tool list       |
| **Enter**  | Open highlighted tool               |
| **Alt+F4** | Quit                                |

---

## ⬆️ Upgrading from v1.0.0

Replace the contents of your `DevVault/` folder with the new release. Your settings — theme, favorites, clipboard dismissals — are stored in `%APPDATA%\DevVault\` and carry over automatically.

---

## Full changelog

See [CHANGELOGS.md](CHANGELOGS.md) for the complete history.
