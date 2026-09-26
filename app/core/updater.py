import json
import urllib.request
import urllib.error

from PySide6.QtCore import QThread, Signal

from app.core.version import APP_VERSION, is_newer


GITHUB_REPO = "Ohiocteator22/Lifeless-DevVault"
API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
TIMEOUT_SECONDS = 8


class UpdateChecker(QThread):
    """
    One-shot background check for a newer release.

    Emits `result(dict | None)`:
      dict = {
          "version":  "1.2.0",
          "title":    "DevVault v1.2.0",
          "url":      "https://github.com/.../releases/tag/v1.2.0",
          "notes":    "markdown body...",
      }
      None = no update, or the check failed (silent).
    """

    result = Signal(object)

    def run(self) -> None:
        data = self._fetch_latest()
        if data is None:
            self.result.emit(None)
            return

        tag = data.get("tag_name") or ""
        html_url = data.get("html_url") or ""
        title = data.get("name") or tag
        body = data.get("body") or ""

        if not tag or not is_newer(tag, APP_VERSION):
            self.result.emit(None)
            return

        self.result.emit(
            {
                "version": tag.lstrip("vV"),
                "title": title,
                "url": html_url,
                "notes": body,
            }
        )

    def _fetch_latest(self) -> dict | None:
        try:
            req = urllib.request.Request(
                API_URL,
                headers={
                    "User-Agent": f"DevVault/{APP_VERSION}",
                    "Accept": "application/vnd.github+json",
                },
            )
            with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
                if resp.status != 200:
                    return None
                return json.loads(resp.read().decode("utf-8"))
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError):
            return None
        except Exception:
            return None