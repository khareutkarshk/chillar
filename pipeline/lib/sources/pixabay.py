"""Pixabay: images + video via the official API; audio (SFX + music) scraped politely.

Audio scraping needs a visible Chrome window (Cloudflare). It is against Pixabay's ToS, so keep
volume tiny. Refused automatically: tracks registered with YouTube Content ID, AI-generated audio.
"""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import quote, urljoin

from ..common import Candidate, env, polite_sleep, session, text_of
from ..licenses import LicenseRefused
from . import browser

LICENSE_URL = "https://pixabay.com/service/license-summary/"
LICENSE = "Pixabay Content License"
BOOT_JS = "async () => { const r = await fetch(window.__BOOTSTRAP_URL__); return await r.text(); }"
_page = None


def _browser_page():
    global _page
    if _page is None or _page.is_closed():
        _page = browser.headed().new_page()
    return _page


def _boot(url: str) -> dict:
    pg = _browser_page()
    polite_sleep()
    pg.goto(url, wait_until="domcontentloaded", timeout=60000)
    browser.wait_past_challenge(pg)
    pg.wait_for_timeout(1500)
    return json.loads(pg.evaluate(BOOT_JS))


def _media_items(o, acc):
    if isinstance(o, dict):
        if o.get("mediaType") == "audio" and isinstance(o.get("sources"), dict):
            acc.append(o)
            return acc
        for v in o.values():
            _media_items(v, acc)
    elif isinstance(o, list):
        for v in o:
            _media_items(v, acc)
    return acc


def _audio_candidate(m: dict, kind: str) -> Candidate:
    src = m["sources"]
    return Candidate(
        source="pixabay", source_id=str(m["id"]), title=m.get("name") or m.get("heading") or "",
        kind=kind, page_url="https://pixabay.com" + m["href"],
        download_url=urljoin("https://pixabay.com/", src.get("downloadUrl") or src.get("src") or ""),
        license_name=LICENSE,
        license_url=LICENSE_URL, attribution_required=False,
        author=(m.get("artist") or (m.get("user") or {}).get("username", "")),
        duration=m.get("duration"), ext="mp3",
        extra={"hasYoutubeContentId": m.get("hasYoutubeContentId"),
               "isAiGenerated": m.get("isAiGenerated"),
               "mirror_of_freesound": "(Freesound)" in (m.get("artist") or "")})


def search(query: str, kind: str = "sfx", n: int = 5, max_dur: float | None = None,
           min_dur: float | None = None, **_) -> list[Candidate]:
    if kind in ("image", "video"):
        return _api_search(query, kind, n)
    if kind not in ("sfx", "music"):
        return []
    section = "sound-effects" if kind == "sfx" else "music"
    data = _boot(f"https://pixabay.com/{section}/search/{quote(query)}/")
    out = []
    for m in _media_items(data.get("page", data), []):
        d = m.get("duration") or 0
        if m.get("hasYoutubeContentId") or m.get("isAiGenerated"):
            continue
        if (max_dur and d > max_dur) or (min_dur and d < min_dur):
            continue
        out.append(_audio_candidate(m, kind))
        if len(out) >= n:
            break
    return out


def _api_search(query: str, kind: str, n: int) -> list[Candidate]:
    key = env("PIXABAY_API_KEY")
    if not key:
        raise RuntimeError("PIXABAY_API_KEY missing in .env")
    url = "https://pixabay.com/api/" if kind == "image" else "https://pixabay.com/api/videos/"
    params = {"key": key, "q": query, "per_page": max(3, n), "safesearch": "true"}
    if kind == "image":
        params["image_type"] = "illustration"
    r = session.get(url, params=params, timeout=30)
    r.raise_for_status()
    out = []
    for h in r.json().get("hits", [])[:n]:
        if kind == "image":
            dl, ext = h.get("largeImageURL"), "jpg"
        else:
            v = h["videos"].get("large") or h["videos"].get("medium")
            dl, ext = v["url"], "mp4"
        out.append(Candidate("pixabay", str(h["id"]), h.get("tags", query), kind, h["pageURL"], dl,
                             LICENSE, LICENSE_URL, False, h.get("user", ""), ext=ext,
                             extra={"api": {k: h.get(k) for k in ("id", "pageURL", "tags", "user")}}))
    return out


def verify(c: Candidate) -> str:
    if c.kind in ("image", "video"):
        return (f"Pixabay API result — API content is under the {LICENSE} ({LICENSE_URL}).\n"
                + json.dumps(c.extra.get("api"), indent=2))
    data = _boot(c.page_url)
    m = (data.get("page") or {}).get("mediaItem") or {}
    if str(m.get("id")) != c.source_id:
        raise LicenseRefused(f"{c.key}: item page did not load")
    if m.get("hasYoutubeContentId"):
        raise LicenseRefused(f"{c.key}: registered with YouTube Content ID (claims risk)")
    if m.get("isAiGenerated"):
        raise LicenseRefused(f"{c.key}: AI-generated audio (unclear copyright)")
    if (m.get("sources") or {}).get("downloadUrl"):
        c.download_url = urljoin("https://pixabay.com/", m["sources"]["downloadUrl"])
    page_text = text_of(_browser_page().content())
    if LICENSE not in page_text:
        raise LicenseRefused(f"{c.key}: page does not state the {LICENSE}")
    i = page_text.find(LICENSE)
    c.extra["attribution"] = text_of(m.get("attributionHtml") or "")
    return (f"Pixabay item page at download time states: ...{page_text[max(0, i - 120):i + 200]}...\n"
            + json.dumps({k: m.get(k) for k in ("id", "name", "artist", "duration", "hasYoutubeContentId",
                                                "isAiGenerated", "contentIdCertificateUrl", "publishedDate")},
                         indent=2))


def download(c: Candidate, dest: Path) -> Path:
    dest = dest.with_suffix("." + c.ext)
    if c.kind in ("image", "video"):
        r = session.get(c.download_url, timeout=120)
    else:  # use the browser's cookies (Cloudflare)
        r = browser.headed().request.get(c.download_url, timeout=120000,
                                         headers={"Referer": c.page_url})
        if not r.ok:
            raise RuntimeError(f"{c.key}: download HTTP {r.status}")
        dest.write_bytes(r.body())
        return dest
    r.raise_for_status()
    dest.write_bytes(r.content)
    return dest
