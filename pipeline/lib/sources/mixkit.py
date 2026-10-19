"""Mixkit free SFX + music (scraped politely; no API exists).

IMPORTANT: Mixkit pages also show paid Envato Elements items (item-type "elements-sfx" /
"elements-music"). Only item-type "sfx" / "music" are free Mixkit items; everything else is
dropped here.
"""
from __future__ import annotations

import re
from pathlib import Path

from ..common import Candidate, polite_sleep, session, slug
from ..licenses import LicenseRefused
from . import browser

LICENSE_PAGE = "https://mixkit.co/license/"
LIC = {
    "sfx": ("Mixkit Sound Effects Free License", "https://mixkit.co/license/#sfxFree", "sfxFree"),
    "music": ("Mixkit Stock Music Free License", "https://mixkit.co/license/#musicFree", "musicFree"),
}
_license_text: dict[str, str] = {}

CARDS_JS = """() => [...document.querySelectorAll('.item-grid-card')].map(card => {
  const p = card.querySelector('[data-controller="audio-player"]');
  if (!p) return null;
  const t = card.querySelector('.item-grid-card__title');
  const d = card.querySelector('[data-test-id="duration"]');
  return { id: p.dataset.audioPlayerItemIdValue, type: p.dataset.audioPlayerItemTypeValue,
           preview: p.dataset.audioPlayerPreviewUrlValue,
           title: t ? t.innerText.trim() : '', duration: d ? d.innerText.trim() : '' };
}).filter(Boolean)"""


def _dur(s: str) -> float | None:
    m = re.match(r"(\d+):(\d+)", s or "")
    return int(m.group(1)) * 60 + int(m.group(2)) if m else None


def _pages_for(query: str, kind: str) -> list[str]:
    base = "https://mixkit.co/free-sound-effects/" if kind == "sfx" else "https://mixkit.co/free-stock-music/"
    words = [w for w in re.split(r"\W+", query.lower()) if w]
    slugs = [slug(query)] + [w for w in words if w != slug(query)]
    if kind == "music":
        slugs = [s for s in slugs] + [f"tag/{s}" for s in slugs]
    return [f"{base}{s}/" for s in dict.fromkeys(slugs)]


def search(query: str, kind: str = "sfx", n: int = 5, max_dur: float | None = None, **_) -> list[Candidate]:
    if kind not in ("sfx", "music"):
        return []
    page = browser.headless().new_page()
    out, seen = [], set()
    try:
        for url in _pages_for(query, kind):
            polite_sleep()
            r = page.goto(url, wait_until="networkidle", timeout=60000)
            if not r or r.status != 200 or "/discover/" in page.url:
                continue  # /discover/ search pages list only paid Envato items
            for it in page.evaluate(CARDS_JS):
                if it["type"] != kind or it["id"] in seen:
                    continue  # drop elements-sfx / elements-music (paid)
                d = _dur(it["duration"])
                if max_dur and d and d > max_dur + 0.5:
                    continue
                seen.add(it["id"])
                if kind == "sfx":
                    dl = f"https://assets.mixkit.co/active_storage/sfx/{it['id']}/{it['id']}.wav"
                    ext = "wav"
                else:
                    dl, ext = it["preview"], "mp3"
                name, lic_url, _ = LIC[kind]
                out.append(Candidate(
                    source="mixkit", source_id=f"{kind}-{it['id']}", title=it["title"], kind=kind,
                    page_url=f"{page.url}#{it['id']}", download_url=dl, license_name=name,
                    license_url=lic_url, attribution_required=False, author="Mixkit",
                    duration=d, ext=ext))
                if len(out) >= n:
                    return out
    finally:
        page.close()
    return out


def _license(kind: str) -> str:
    if kind not in _license_text:
        _, _, key = LIC[kind]
        page = browser.headless().new_page()
        try:
            page.goto(LICENSE_PAGE, wait_until="networkidle", timeout=60000)
            for sel in ['button:has-text("Reject all")', 'button:has-text("Accept all")']:
                if page.locator(sel).count():
                    page.locator(sel).first.click()
                    break
            page.click(f'[data-license="{key}"]')
            page.wait_for_timeout(1500)
            # the modal isn't part of body.innerText; read raw textContent instead
            t = re.sub(r"\s+", " ", page.evaluate("document.body.textContent"))
            name = LIC[kind][0]
            i = t.find(f"Items under the {name}")
            j = t.rfind("License", 0, i) if i >= 0 else -1
            _license_text[kind] = t[max(j - 40, i - 400, 0):i + 1500] if i >= 0 else ""
        finally:
            page.close()
    return _license_text[kind]


def verify(c: Candidate) -> str:
    text = _license(c.kind)
    if "commercial" not in text.lower():
        raise LicenseRefused(f"{c.key}: could not confirm commercial use in Mixkit license text")
    return f"{c.license_name} (read from {LICENSE_PAGE} at download time):\n{text}"


def download(c: Candidate, dest: Path) -> Path:
    dest = dest.with_suffix("." + c.ext)
    with session.get(c.download_url, timeout=120, stream=True,
                     headers={"Referer": "https://mixkit.co/"}) as r:
        r.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in r.iter_content(1 << 16):
                f.write(chunk)
    return dest
