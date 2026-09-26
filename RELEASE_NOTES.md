# DevVault v1.2.0

_Released 2026-09-26_

This release adds a background update checker so you never miss a new version. It also lays the groundwork for future automatic builds.

---

## ✨ Highlights

### Automatic update check

DevVault now checks GitHub for a newer release ~2.5 seconds after launch, on a background thread. If a newer version exists, a banner appears at the top of the workspace:

> 🚀 **DevVault v1.3.0 is available** &nbsp; [View Release] &nbsp; [Skip This Version] &nbsp; [Later]

- **View Release** — opens the GitHub release page in your default browser
- **Skip This Version** — remembers your choice; that exact version never shows again
- **Later** — hides the banner for this session; it reappears next launch

The check is a single HTTPS GET to the GitHub releases API. No telemetry, no tracking, no data leaves your machine beyond the standard request.

If you're offline, the API is unreachable, or you're already on the latest version, the check fails silently — no error banner, no nag.

### Privacy

The updater is intentionally minimal:

- No unique identifiers sent
- No install IDs
- No usage statistics
- User-Agent is just `DevVault/1.2.0`
- Respects GitHub's standard rate limits (60 checks/hour per IP — you'll do one per launch)

You can disable the check permanently with a single setting (`update_check_enabled` in `QSettings`). A Settings page exposing this from the UI is planned for a future release.

---

## 🔧 Under the hood

- **`app/core/version.py`** — single source of truth for the app version. Keep it in sync with `version_info.txt` when bumping releases.
- **`app/core/updater.py`** — `UpdateChecker(QThread)` hits the GitHub releases API using only `urllib` (no new dependencies).
- **`app/ui/update_banner.py`** — banner widget matching the existing clipboard banner style.
- Update banner and clipboard banner are stacked in the top of the workspace; only one is visible at a time under normal use.

---

## 🐛 Fixes

- None in this release. All obfuscators, the command palette, and clipboard detection are unchanged from v1.1.0.

---

## 📦 Install

1. Download `DevVault-v1.2.0-windows-x64.zip` below
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

## ⬆️ Upgrading from v1.1.0

Replace the contents of your `DevVault/` folder with the new release. Your settings — theme, favorites, clipboard dismissals — are stored in `%APPDATA%\DevVault\` and carry over automatically.

Once you're on v1.2.0, **future releases will notify you automatically**. No manual checks required.

---

## Full changelog

See [CHANGELOGS.md](CHANGELOGS.md) for the complete history.
