# DevVault — Changelog

All notable changes to DevVault are documented here.  
Format loosely follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [1.2.0] — 2026-09-26

### Added

- **Automatic update check** — on startup, DevVault queries the GitHub releases API on a background thread and shows a banner if a newer version is available.
  - **View Release** button opens the release page in the default browser.
  - **Skip This Version** button persists your choice via `QSettings`; that exact version never shows again.
  - **Later** button hides the banner for the current session only.
  - Check runs ~2.5 seconds after launch and fails silently when offline, rate-limited, or already up-to-date.
- **`app/core/version.py`** — single source of truth for `APP_VERSION`. Must be kept in sync with `version_info.txt` when bumping releases.
- **`app/core/updater.py`** — `UpdateChecker(QThread)` using only Python's standard library (`urllib`), no new dependencies.
- **`app/ui/update_banner.py`** — reusable banner widget, styled to match the clipboard banner.
- **`update_check_enabled`** and **`skipped_version`** settings.

### Changed

- `MainWindow` now runs the update check via `QTimer.singleShot(2500, ...)` after the window is drawn, so startup remains instantaneous.
- `MainWindow.closeEvent` waits briefly for the update thread to finish cleanly before quitting.
- Update banner and clipboard banner share theme styling via a combined QSS selector.

### Notes

- Updater is intentionally minimal: no telemetry, no install IDs, no usage data. User-Agent is just `DevVault/<version>`.
- Manual disabling is available via `QSettings` (`update_check_enabled = false`). A Settings page exposing this from the UI is planned.

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
- **PowerShell Obfuscator** — wraps `psobf` v2.0.1 with six obfuscation levels.
- **`SubprocessObfuscatorWidget`** base class — adding a new language obfuscator is now ~40 lines.
- **`app/core/resources.py`** — path resolver that works from source, PyInstaller onedir, and PyInstaller onefile.
- **`version_info.txt`** — Windows EXE version resource.
- **`build.ps1`** — one-shot PyInstaller build script.
- **`DevVault.spec`** — bundles icon, embeds version info, excludes unused Qt modules.

### Changed

- App now launches in fullscreen borderless mode instead of a resizable window.
- `Ctrl+K` opens a palette page inside the main window instead of a separate dialog, eliminating earlier location/size glitches.
- Settings now include `clipboard_enabled` and `clipboard_dismissed`.

### Fixed

- Fixed `UnicodeDecodeError` crash when PowerShell obfuscator output contained non-ASCII bytes. All subprocess I/O now uses UTF-8 with `errors="replace"`.
- Fixed tool resolution on Windows — subprocess calls now resolve `.cmd` / `.exe` shims explicitly via `shutil.which`, bypassing the `CreateProcess` extension quirk.

### Removed

- **Lua Deobfuscator** — Prometheus obfuscates source-level Lua, not bytecode, so an obfuscate → decompile roundtrip isn't meaningful.

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

[Unreleased]: https://github.com/Ohiocteator22/Lifeless-DevVault/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/Ohiocteator22/Lifeless-DevVault/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/Ohiocteator22/Lifeless-DevVault/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/Ohiocteator22/Lifeless-DevVault/releases/tag/v1.0.0
