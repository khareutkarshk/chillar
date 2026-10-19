"""Freesound API v2 — Creative Commons 0 ONLY.

Token auth gives HQ previews (128 kbps mp3), fine for SFX. If FREESOUND_OAUTH_TOKEN is set the
original file is downloaded instead.
"""
from __future__ import annotations

import json
from pathlib import Path

from ..common import Candidate, env, session
from ..licenses import LicenseRefused

API = "https://freesound.org/apiv2"
CC0 = "http://creativecommons.org/publicdomain/zero/1.0/"
FIELDS = "id,name,username,duration,previews,license,url,avg_rating,num_downloads,type"


def _key() -> str:
    k = env("FREESOUND_API_KEY")
    if not k:
        raise RuntimeError("FREESOUND_API_KEY missing in .env")
    return k


def search(query: str, kind: str = "sfx", n: int = 5, max_dur: float | None = None,
           min_dur: float | None = None) -> list[Candidate]:
    filt = 'license:"Creative Commons 0"'
    if max_dur or min_dur:
        filt += f" duration:[{min_dur or 0} TO {max_dur or '*'}]"
    r = session.get(f"{API}/search/text/", params={
        "query": query, "filter": filt, "fields": FIELDS, "page_size": max(n * 3, 15),
        "sort": "score", "token": _key()}, timeout=30)
    r.raise_for_status()
    results = r.json().get("results", [])
    # prefer well-rated, much-downloaded sounds among the relevant ones
    results.sort(key=lambda s: (-(s.get("avg_rating") or 0) * min(s.get("num_downloads") or 0, 500)))
    out = []
    for s in results:
        if s.get("license") != CC0:
            continue
        out.append(Candidate(
            source="freesound", source_id=str(s["id"]), title=s["name"], kind=kind,
            page_url=s["url"], download_url=s["previews"]["preview-hq-mp3"],
            license_name="CC0 1.0", license_url=CC0, attribution_required=False,
            author=s.get("username", ""), duration=s.get("duration"), ext="mp3",
            extra={"original_type": s.get("type")}))
        if len(out) >= n:
            break
    return out


def verify(c: Candidate) -> str:
    """Re-read the sound's license from the API at download time."""
    r = session.get(f"{API}/sounds/{c.source_id}/",
                    params={"fields": "id,name,username,license,url", "token": _key()}, timeout=30)
    r.raise_for_status()
    s = r.json()
    if s.get("license") != CC0:
        raise LicenseRefused(f"freesound:{c.source_id} is now '{s.get('license')}', not CC0")
    return "Freesound API response at download time:\n" + json.dumps(s, indent=2)


def download(c: Candidate, dest: Path) -> Path:
    oauth = env("FREESOUND_OAUTH_TOKEN")
    if oauth:
        url = f"{API}/sounds/{c.source_id}/download/"
        headers = {"Authorization": f"Bearer {oauth}"}
        ext = c.extra.get("original_type") or "wav"
    else:
        url, headers, ext = c.download_url, {}, "mp3"
    dest = dest.with_suffix("." + ext)
    with session.get(url, headers=headers, timeout=60, stream=True) as r:
        r.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in r.iter_content(1 << 16):
                f.write(chunk)
    return dest
