"""Active brand theme (brand/tokens.json "theme", overridable per episode in episode.toml [render] theme)."""
from __future__ import annotations

import json

from .common import BRAND

TOK = json.loads((BRAND / "tokens.json").read_text())


def theme(name: str | None = None) -> dict:
    name = name or TOK["theme"]
    if name not in TOK["themes"]:
        raise SystemExit(f"unknown theme '{name}' — one of {sorted(TOK['themes'])}")
    return {"name": name, **TOK["themes"][name]}


def palette_hexes(name: str | None = None) -> list[str]:
    """Every colour that may appear on screen in this theme: palette + every field bg + field ink."""
    t = theme(name)
    out = list(t["palette"].values())
    for f in t["fields"].values():
        out += [f["bg"], f["ink"]]
    return sorted(set(out))
