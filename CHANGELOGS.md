# DevVault — Changelog

All notable changes to DevVault are documented here.  
Format loosely follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [1.1.0] — 2026-09-25

### Added

- **Command palette (Ctrl+K)** — Spotlight-style launcher. Shrinks the window to a centered palette; type to filter, ↑↓ to navigate, Enter to open, Esc to cancel.
- **Fullscreen borderless UI** — DevVault launches fullscreen with no window chrome. Minimize and close buttons live in the top bar.
- **Clipboard detection banner** — on window focus, DevVault fingerprints the clipboard and offers to open the matching tool with content pre-filled. Detects JSON, JWTs, UUIDs, MD5/SHA-1/SHA-256 hashes, URLs, Lua bytecode, Base64, and Lua / JavaScript / Python / PowerShell source.
- **App icon** — multi-size `.ico` embedded in the EXE and set at runtime via `QApplication.setWindowIcon`.
- **Windows identity** — Task Manager and taskbar show **DevVault** instead of `python.exe`, via `AppUserModelID` and an embedded version resource.
- **Window controls** — minimize and close buttons in the top bar for the frameless window.
- **JavaScript Obfuscator** — wraps `javascript-obfuscator` with control-flow flattening, dead-code injection, and string-array encoding.
- **Python Obfuscator** — wraps `pyobfus`.
- **PowerShell Obfuscator** — wraps `psobf` v2.0.1 with six obfuscation levels (char join, Base64, GZip+Base64, fragmentation, AES-256 CTR).
- **`SubprocessObfuscatorWidget`** base class — adding a new language obfuscator is now ~40 lines.
- **`app/core/resources.py`** — path resolver that works from source, PyInstaller onedir, and PyInstaller onefile.
- **`version_info.txt`** — Windows EXE version resource.
- **`build.ps1`** — one-shot PyInstaller build script.
- **`DevVault.spec`** — bundles icon, embeds version info, excludes unused Qt modules.

### Changed

- App now launches in fullscreen borderless mode instead of a resizable window.
- `Ctrl+K` opens a palette page inside the main window instead of a separate dialog, eliminating the earlier location/size glitches.
- Settings now include `clipboard_enabled` and `clipboard_dismissed`.

### Fixed

- Fixed `UnicodeDecodeError` crash when PowerShell obfuscator output contained non-ASCII bytes. All subprocess I/O now uses UTF-8 with `errors="replace"`.
- Fixed tool resolution on Windows — subprocess calls now resolve `.cmd` / `.exe` shims explicitly via `shutil.which`, bypassing the `CreateProcess` extension quirk.

### Removed

- **Lua Deobfuscator** — Prometheus obfuscates source-level Lua, not bytecode, so an obfuscate → decompile roundtrip isn't meaningful. Removed to avoid misleading users.

---

## [1.0.0] — 2026-09-23

### Added

- **Shell** — category sidebar, tool grid, favorites, live search, dark/light theme toggle.
- **Data** — JSON Formatter (pretty-print + validate, live as you type).
- **Encoding** — Base64 (auto-detects encode/decode direction), Hash Generator (MD5, SHA-1, SHA-256, SHA-384, SHA-512).
- **Testing** — UUID Generator (bulk v4 UUIDs).
- **Script** — Lua Obfuscator wrapping Prometheus via `@gamely/prometheus-cli`.
- Tool registry architecture — new tools register themselves and automatically appear in sidebar, search, and favorites.
- Portable Windows build via PyInstaller `--onedir`.
- Favorites and theme persistence via `QSettings`.

### Notes

- Initial public release.
- Windows-only.
- Unsigned binary — SmartScreen may warn on first run.

---

[Unreleased]: https://github.com/Ohiocteator22/Lifeless-DevVault/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/Ohiocteator22/Lifeless-DevVault/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/Ohiocteator22/Lifeless-DevVault/releases/tag/v1.0.0
