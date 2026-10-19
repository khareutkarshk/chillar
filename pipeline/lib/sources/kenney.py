"""Kenney.nl CC0 audio packs. Zips are cached once; files are matched by name."""
from __future__ import annotations

import re
import shutil
import zipfile
from pathlib import Path

from ..common import CACHE, Candidate, polite_sleep, session, text_of
from ..licenses import LicenseRefused

PACKS = ["impact-sounds", "casino-audio", "interface-sounds", "ui-audio", "digital-audio"]
CC0_URL = "https://creativecommons.org/publicdomain/zero/1.0/"

# query word -> filename fragments that Kenney actually uses
SYNONYMS = {
    "stamp": ["impactpunch_heavy", "impactwood_heavy", "impactplank"],
    "thunk": ["impactpunch_heavy", "impactwood_heavy"],
    "coin": ["chipslay", "chipsstack", "chipscollide", "impactmetal_light"],
    "clink": ["chipscollide", "impactglass_light", "impactmetal_light"],
    "click": ["click", "switch", "tick"],
    "whoosh": ["swoosh", "whoosh"],
    "glitch": ["error", "glitch", "phaserdown"],
    "ding": ["confirmation", "bong", "pluck"],
    "typing": ["click", "tick"],
}
_pages: dict[str, str] = {}


def _pack_dir(pack: str) -> Path:
    return CACHE / "kenney" / pack


def _page(pack: str) -> str:
    if pack not in _pages:
        polite_sleep()
        r = session.get(f"https://kenney.nl/assets/{pack}", timeout=30)
        r.raise_for_status()
        _pages[pack] = r.text
    return _pages[pack]


def _ensure_pack(pack: str) -> Path:
    d = _pack_dir(pack)
    if d.exists() and any(d.rglob("*.ogg")):
        return d
    html = _page(pack)
    if "Creative Commons CC0" not in text_of(html):
        raise LicenseRefused(f"kenney:{pack} page no longer states CC0")
    m = re.search(r"https://kenney\.nl/media/pages/assets/[^\"' ]+\.zip", html)
    if not m:
        raise RuntimeError(f"kenney:{pack} zip link not found")
    d.mkdir(parents=True, exist_ok=True)
    z = d / "pack.zip"
    with session.get(m.group(0), timeout=120, stream=True) as r:
        r.raise_for_status()
        with open(z, "wb") as f:
            shutil.copyfileobj(r.raw, f)
    with zipfile.ZipFile(z) as zf:
        for name in zf.namelist():  # extract audio only, no path traversal
            if name.lower().endswith((".ogg", ".wav", ".mp3")) and ".." not in name:
                target = d / Path(name).name
                with zf.open(name) as src, open(target, "wb") as dst:
                    shutil.copyfileobj(src, dst)
    z.unlink()
    return d


def search(query: str, kind: str = "sfx", n: int = 5, **_) -> list[Candidate]:
    if kind != "sfx":
        return []
    words = [w for w in re.split(r"\W+", query.lower()) if w]
    frags = set(words)
    for w in words:
        frags.update(SYNONYMS.get(w, []))
    out = []
    for pack in PACKS:
        try:
            d = _ensure_pack(pack)
        except Exception as e:  # network or license problem: skip pack, keep going
            print(f"    kenney:{pack} skipped ({e})")
            continue
        for f in sorted(d.iterdir()):
            stem = f.stem.lower()
            if any(fr in stem for fr in frags):
                out.append(Candidate(
                    source="kenney", source_id=f"{pack}/{f.name}", title=f"{pack} · {f.stem}",
                    kind="sfx", page_url=f"https://kenney.nl/assets/{pack}",
                    download_url=f"file://{f}", license_name="CC0 1.0", license_url=CC0_URL,
                    attribution_required=False, author="Kenney", ext=f.suffix.lstrip(".")))
                if len(out) >= n:
                    return out
    return out


def verify(c: Candidate) -> str:
    pack = c.source_id.split("/")[0]
    t = text_of(_page(pack))
    if "Creative Commons CC0" not in t:
        raise LicenseRefused(f"kenney:{pack} page no longer states CC0")
    i = t.find("License")
    return f"kenney.nl/assets/{pack} page text:\n{t[max(0, i - 200):i + 300]}"


def download(c: Candidate, dest: Path) -> Path:
    src = Path(c.download_url.removeprefix("file://"))
    dest = dest.with_suffix(src.suffix)
    shutil.copy2(src, dest)
    return dest
