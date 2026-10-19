"""Pexels API — photos + video. Style is illustrated: use sparingly."""
from __future__ import annotations

import json
from pathlib import Path

from ..common import Candidate, env, session

LICENSE_URL = "https://www.pexels.com/license/"


def _headers() -> dict:
    k = env("PEXELS_API_KEY")
    if not k:
        raise RuntimeError("PEXELS_API_KEY missing in .env")
    return {"Authorization": k}


def search(query: str, kind: str = "image", n: int = 5, **_) -> list[Candidate]:
    if kind not in ("image", "video"):
        return []
    url = "https://api.pexels.com/v1/search" if kind == "image" else "https://api.pexels.com/videos/search"
    r = session.get(url, headers=_headers(), params={"query": query, "per_page": n,
                                                     "orientation": "portrait"}, timeout=30)
    r.raise_for_status()
    out = []
    for it in r.json().get("photos" if kind == "image" else "videos", []):
        if kind == "image":
            dl, ext, author = it["src"]["large2x"], "jpg", it.get("photographer", "")
        else:
            files = sorted(it.get("video_files", []), key=lambda f: -(f.get("height") or 0))
            files = [f for f in files if (f.get("height") or 0) <= 1920] or files
            dl, ext, author = files[0]["link"], "mp4", it.get("user", {}).get("name", "")
        out.append(Candidate(
            source="pexels", source_id=str(it["id"]), title=it.get("alt") or query, kind=kind,
            page_url=it["url"], download_url=dl, license_name="Pexels License",
            license_url=LICENSE_URL, attribution_required=False, author=author, ext=ext,
            extra={"api": {k: it.get(k) for k in ("id", "url", "width", "height")}}))
    return out


def verify(c: Candidate) -> str:
    # Pexels pages sit behind bot protection; the API terms cover every API result.
    return ("Pexels API result (all API content is under the Pexels License: free for commercial "
            f"use, no attribution required; {LICENSE_URL}).\n" + json.dumps(c.extra.get("api"), indent=2))


def download(c: Candidate, dest: Path) -> Path:
    dest = dest.with_suffix("." + c.ext)
    with session.get(c.download_url, timeout=120, stream=True) as r:
        r.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in r.iter_content(1 << 16):
                f.write(chunk)
    return dest
