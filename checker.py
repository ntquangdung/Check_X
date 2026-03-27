from __future__ import annotations

import json
import time
from dataclasses import dataclass

try:
    from DrissionPage import Chromium, ChromiumOptions
except ImportError:  # pragma: no cover
    Chromium = None
    ChromiumOptions = None


LIVE_STATUS = "live"
SUSPENDED_STATUS = "suspended"
DIE_STATUS = "die"
UNKNOWN_STATUS = "unknown"

SUSPENDED_TEXT = "Account suspended"
DIE_TEXTS = [
    "This account doesn\u2019t exist",
    "This account doesn't exist",
    "Page doesn\u2019t exist",
    "Page doesn't exist",
    "Try searching for another.",
    "Try searching for another",
]


@dataclass
class CheckResult:
    username: str
    status: str
    reason: str
    profile_url: str

    def as_dict(self) -> dict:
        return {
            "username": self.username,
            "status": self.status,
            "reason": self.reason,
            "profile_url": self.profile_url,
        }


class BatchChecker:
    def __init__(self, headless: bool = True, load_mode: str = "eager", timeout: float = 100):
        self.headless = headless
        self.load_mode = load_mode
        self.timeout = timeout

    def _build_browser(self):
        if Chromium is None or ChromiumOptions is None:
            raise RuntimeError("Chua cai DrissionPage. Hay chay: pip install -r requirements.txt")

        options = ChromiumOptions()
        if self.headless:
            options.headless(True)
        options.set_argument("--disable-gpu")
        options.set_argument("--disable-blink-features=AutomationControlled")
        options.set_argument("--window-size=1400,900")
        options.set_argument("--no-first-run")
        options.set_argument("--no-default-browser-check")
        options.set_user_agent(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        return Chromium(options)

    def _current_url(self, tab) -> str:
        try:
            return (tab.url or "").strip().lower()
        except Exception:  # noqa: BLE001
            return ""

    def _has_visible_exact_span_text(self, tab, text_value: str) -> bool:
        target = json.dumps(text_value)
        js = f"""
const target = {target};
const roots = Array.from(document.querySelectorAll('main, article'));
const nodes = roots.length ? roots.flatMap(root => Array.from(root.querySelectorAll('span'))) : Array.from(document.querySelectorAll('span'));
return nodes.some(el => {{
  const text = (el.textContent || '').trim();
  if (text !== target) return false;
  const style = window.getComputedStyle(el);
  const rect = el.getBoundingClientRect();
  return style.display !== 'none' &&
         style.visibility !== 'hidden' &&
         rect.width > 0 &&
         rect.height > 0;
}});
"""
        try:
            return bool(tab.run_js(js))
        except Exception:  # noqa: BLE001
            return False

    def _has_any_visible_span_text(self, tab, text_values: list[str]) -> bool:
        return any(self._has_visible_exact_span_text(tab, value) for value in text_values)

    def _match_state(self, tab, username: str) -> CheckResult | None:
        url = f"https://x.com/{username}"
        username_text = f"@{username}"
        current_url = self._current_url(tab)
        expected_urls = {
            f"https://x.com/{username.lower()}",
            f"https://twitter.com/{username.lower()}",
        }

        if current_url.rstrip("/") not in expected_urls:
            return None

        if self._has_visible_exact_span_text(tab, username_text):
            return CheckResult(username, LIVE_STATUS, f"Tim thay @{username}.", url)

        if self._has_visible_exact_span_text(tab, SUSPENDED_TEXT):
            return CheckResult(username, SUSPENDED_STATUS, "Trang xuat hien 'Account suspended'.", url)

        if self._has_any_visible_span_text(tab, DIE_TEXTS):
            return CheckResult(username, DIE_STATUS, "Trang xuat hien 'This account doesn't exist'.", url)

        return None

    def _wait_for_state(self, tab, username: str) -> CheckResult:
        started_at = time.time()
        while time.time() - started_at < self.timeout:
            result = self._match_state(tab, username)
            if result is not None:
                return result
            time.sleep(0.8)

        raise RuntimeError(
            f"Het {self.timeout} giay ma van khong thay 1 trong 3 dieu kien cho @{username}."
        )

    def check_many(self, usernames: list[str]) -> list[dict]:
        browser = None
        results = []
        try:
            browser = self._build_browser()
            tab = browser.latest_tab
            try:
                if self.load_mode == "none":
                    tab.set.load_mode.none()
                else:
                    tab.set.load_mode.eager()
            except Exception:  # noqa: BLE001
                pass
            try:
                tab.set.timeouts(base=self.timeout, page_load=self.timeout)
            except Exception:  # noqa: BLE001
                pass

            total = len(usernames)
            for index, username in enumerate(usernames, start=1):
                print(f"Dang kiem tra {index}/{total}: @{username}")
                url = f"https://x.com/{username}"
                try:
                    try:
                        tab.get("about:blank", retry=0, timeout=5)
                        time.sleep(0.2)
                    except Exception:  # noqa: BLE001
                        pass
                    tab.get(url, retry=1, timeout=self.timeout)
                    result = self._wait_for_state(tab, username)
                except Exception as exc:  # noqa: BLE001
                    result = CheckResult(
                        username=username,
                        status=UNKNOWN_STATUS,
                        reason=f"Khong the xac nhan 3 dieu kien: {type(exc).__name__}: {exc}",
                        profile_url=url,
                    )
                results.append(result.as_dict())
        finally:
            if browser is not None:
                browser.quit()

        return results
