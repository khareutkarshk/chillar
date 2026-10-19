"""Lazily-started Playwright browsers shared by the scraping adapters.

- headless(): plain headless Chromium (Mixkit doesn't block it)
- headed():   visible Google Chrome with a persistent profile (needed to pass Pixabay's
              Cloudflare check). Requires a display ($DISPLAY); a window will open briefly.
"""
from __future__ import annotations

import atexit
import os

from ..common import CACHE

_pw = None
_headless = None
_headed = None


def _playwright():
    global _pw
    if _pw is None:
        from playwright.sync_api import sync_playwright
        _pw = sync_playwright().start()
        atexit.register(close)
    return _pw


def headless():
    global _headless
    if _headless is None:
        _headless = _playwright().chromium.launch()
    return _headless


def headed():
    global _headed
    if _headed is None:
        if not os.environ.get("DISPLAY") and not os.environ.get("WAYLAND_DISPLAY"):
            raise RuntimeError("Pixabay audio needs a visible browser; no $DISPLAY. Run from your desktop session.")
        prof = CACHE / "chrome-profile"
        prof.mkdir(parents=True, exist_ok=True)
        _headed = _playwright().chromium.launch_persistent_context(
            str(prof), channel="chrome", headless=False,
            args=["--disable-blink-features=AutomationControlled", "--window-size=900,700"],
            viewport={"width": 900, "height": 700})
    return _headed


def wait_past_challenge(page, tries: int = 20) -> None:
    for _ in range(tries):
        page.wait_for_timeout(1500)
        if "moment" not in page.title().lower():
            return
    raise RuntimeError(f"stuck on bot check at {page.url}")


def close():
    global _pw, _headless, _headed
    for b in (_headed, _headless):
        try:
            if b:
                b.close()
        except Exception:
            pass
    if _pw:
        try:
            _pw.stop()
        except Exception:
            pass
    _pw = _headless = _headed = None
