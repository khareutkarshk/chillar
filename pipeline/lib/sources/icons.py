"""Lucide (ISC) and Tabler (MIT) icons via unpkg; Google Noto Emoji (Apache-2.0) SVGs.

Query = icon name (e.g. "receipt", "coins") or, for noto, an emoji character / codepoint.
"""
from __future__ import annotations

import json
from pathlib import Path

from ..common import Candidate, session, slug

SETS = {
    "lucide": ("lucide-static", "https://unpkg.com/lucide-static@{v}/icons/{name}.svg"),
    "tabler": ("@tabler/icons", "https://unpkg.com/@tabler/icons@{v}/icons/outline/{name}.svg"),
}
NOTO = "https://raw.githubusercontent.com/googlefonts/noto-emoji/main/svg/emoji_u{cp}.svg"
NOTO_LICENSE = "https://raw.githubusercontent.com/googlefonts/noto-emoji/main/svg/LICENSE"
_pkg: dict[str, dict] = {}


def _pkg_json(pkg: str) -> dict:
    if pkg not in _pkg:
        r = session.get(f"https://unpkg.com/{pkg}/package.json", timeout=30)
        r.raise_for_status()
        _pkg[pkg] = r.json()
    return _pkg[pkg]


def search(query: str, kind: str = "icon", n: int = 3, icon_set: str | None = None, **_) -> list[Candidate]:
    if kind != "icon":
        return []
    out = []
    name = slug(query)                          # goes into an unpkg URL path
    for set_name in ([icon_set] if icon_set else ["lucide", "tabler", "noto"]):
        if set_name == "noto":
            cps = [f"{ord(ch):x}" for ch in query if ord(ch) > 0x2000 and ch != "️"]
            if not cps and query.lower().startswith(("u+", "1f")):
                cps = [query.lower().removeprefix("u+")]
            if not cps:
                continue
            cp = "_".join(cps)
            url = NOTO.format(cp=cp)
            if session.head(url, timeout=20).status_code != 200:
                continue
            out.append(Candidate("noto", cp, f"noto emoji {query}", "icon",
                                 f"https://github.com/googlefonts/noto-emoji/blob/main/svg/emoji_u{cp}.svg",
                                 url, "Apache-2.0", NOTO_LICENSE, True, "Google", ext="svg",
                                 extra={"attribution": "Noto Emoji © Google, Apache-2.0"}))
            continue
        pkg, tmpl = SETS[set_name]
        meta = _pkg_json(pkg)
        url = tmpl.format(v=meta["version"], name=name)
        if session.head(url, timeout=20, allow_redirects=True).status_code != 200:
            continue
        lic = meta.get("license", "")
        out.append(Candidate(set_name, f"{name}@{meta['version']}", f"{set_name} {name}", "icon",
                             f"https://unpkg.com/{pkg}@{meta['version']}/", url,
                             {"ISC": "ISC", "MIT": "MIT"}.get(lic, lic),
                             f"https://unpkg.com/{pkg}@{meta['version']}/LICENSE", True, set_name,
                             ext="svg", extra={"attribution": f"{set_name} icons, {lic} license"}))
    return out[:n]


def verify(c: Candidate) -> str:
    if c.source == "noto":
        r = session.get(NOTO_LICENSE, timeout=30)
        r.raise_for_status()
        return r.text[:3000]
    pkg = SETS[c.source][0]
    meta = _pkg_json(pkg)
    return f"{pkg}@{meta['version']} package.json license field: {meta.get('license')}\n" + \
        json.dumps({k: meta.get(k) for k in ("name", "version", "license", "homepage")}, indent=2)


def download(c: Candidate, dest: Path) -> Path:
    dest = dest.with_suffix(".svg")
    r = session.get(c.download_url, timeout=30)
    r.raise_for_status()
    dest.write_bytes(r.content)
    return dest
