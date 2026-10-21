#!/usr/bin/env python3
"""Write components/_catalog.md — one entry per component (purpose, layer, minimum duration, params
with defaults, SFX events) so the director reads ~2k tokens instead of every component.json.

  component_catalog.py            regenerate
  component_catalog.py --check    exit 1 if the catalog is stale (a component.json is newer)
Regenerated automatically by component_gallery.py; run it by hand after editing a component.json.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.common import ROOT  # noqa: E402

COMP = ROOT / "components"
OUT = COMP / "_catalog.md"
AUTO = {"chapter-field", "transition", "wordmark", "captions", "outro"}   # placed by the pipeline


def short(v) -> str:
    """A default the director can copy without opening component.json: lists of objects show the full
    shape of one item (every key, with its default), long strings are kept up to 60 chars."""
    if isinstance(v, list) and v and isinstance(v[0], dict):
        item = "{" + ", ".join(f'"{k}": {short(x)}' for k, x in v[0].items()) + "}"
        return f"[{item}, …]" if len(v) > 1 else f"[{item}]"
    if isinstance(v, list) and len(v) > 3:
        return json.dumps(v[:2], ensure_ascii=False)[:-1] + ", …]"
    s = json.dumps(v, ensure_ascii=False)
    return s if len(s) <= 60 else s[:57] + "…\""


def entry(name: str, m: dict) -> str:
    params = ", ".join(f"{k}={short(v)}" for k, v in m.get("params", {}).items())
    sfx = ", ".join(f"{e['sound']}@{e['at']}s" for e in m.get("sfx", []))
    bits = [f"layer {m.get('layer', 'scene')}"]
    if m.get("minDuration"):
        bits.append(f"min {m['minDuration']}s")
    if m.get("rehook"):
        bits.append("re-hook")
    if sfx:
        bits.append(f"sfx {sfx}")
    if m.get("styles"):
        bits.append("styles " + "/".join(m["styles"]))
    out = [f"### {name}" + ("  _(auto — never place in scenes.json)_" if name in AUTO else ""),
           m.get("description", "").strip(), f"`{' · '.join(bits)}`"]
    if params and name not in AUTO:
        out.append(f"params: {params}")
    return "\n".join(x for x in out if x) + "\n"


def render() -> str:
    metas = {p.parent.name: json.loads(p.read_text()) for p in sorted(COMP.glob("*/component.json"))}
    head = ("# Component catalog (generated — `pipeline/component_catalog.py`, don't edit)\n\n"
            "Read this instead of the component folders. Open a `components/<name>/component.json` only for a\n"
            "component you are about to use and need its full `example`. Layers: `scene` lasts until the next scene;\n"
            "`overlay` needs `until`/`duration`. Times in params are seconds from the scene's start.\n\n"
            "**scenes.json keys** (full spec: `pipeline/validate_scenes.py` docstring — no need to open it):\n"
            "scene `{id, component, at, params, fact?, cut?}` · overlay adds `until` or `duration` · "
            "times: seconds, `\"w12\"` (word 12 start), `\"w12.end\"`, `\"w12+0.2\"` · "
            "`cut`: whip | zoom | wipe | page (default hard cut) · top level: `scenes`, `effects` "
            "(`{type: \"punch\", at}`), `theme` (pastel | calm | night), `outro {cut, params}` (1.9 s, fixed), "
            "`music {track, under_voice_db}` · scene components with a content zone accept `params.dy` (px, nudge down + / up −).\n\n")
    placeable = [entry(n, m) for n, m in metas.items() if n not in AUTO]
    auto = [entry(n, m) for n, m in metas.items() if n in AUTO]
    return head + "\n".join(placeable) + "\n## Placed by the pipeline\n\n" + "\n".join(auto)


def stale() -> bool:
    if not OUT.exists():
        return True
    t = OUT.stat().st_mtime
    return any(p.stat().st_mtime > t for p in COMP.glob("*/component.json"))


def main() -> int:
    if "--check" in sys.argv:
        bad = stale()
        print("catalog: stale — run pipeline/component_catalog.py" if bad else "catalog: up to date")
        return 1 if bad else 0
    OUT.write_text(render())
    print(f"catalog: {OUT.relative_to(ROOT)} ({len(list(COMP.glob('*/component.json')))} components)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
