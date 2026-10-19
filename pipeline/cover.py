#!/usr/bin/env python3
"""Export the 1080x1920 cover from cover.md (+ a 3:4 profile-grid crop preview).

  cover.py episodes/<ep>  -> output/cover.png, output/cover_grid_preview.png
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_composition import build  # noqa: E402
from lib.common import BRAND, ROOT  # noqa: E402
from lib.episode import load  # noqa: E402
import json  # noqa: E402

TOK = json.loads((BRAND / "tokens.json").read_text())


def cover(ep_dir: str) -> Path:
    ep = load(ep_dir)
    c = ep.cover
    words = len(str(c.get("cover_text", "")).split())
    if words > 5:
        print(f"  ! cover_text has {words} words — brand rule is ≤5")
    params = {"text": c.get("cover_text", ep.meta.get("title", "")), "kicker": c.get("cover_kicker", ""),
              "stamp": c.get("cover_stamp", ""), "mascot": c.get("cover_mascot", "side-eye")}
    field = c.get("cover_field") or TOK["fieldSequence"][0]
    if field not in TOK["fieldSlots"]:
        print(f"  ! cover_field '{field}' unknown — using {TOK['fieldSequence'][0]}")
        field = TOK["fieldSequence"][0]
    proj = ep.cache / "cover_build"
    if proj.exists():
        shutil.rmtree(proj)
    build({"duration": 1.0, "title": "cover", "theme": ep.theme, "scenes": [
        {"id": "bg", "component": "chapter-field", "params": {"chapters": [{"start": 0, "field": field}], "grain": True},
         "start": 0, "duration": 1.0, "track": 0},
        {"id": "cover", "component": "cover", "params": params, "start": 0, "duration": 1.0, "track": 1}]},
        proj, "cover")
    snaps = ep.cache / "cover_snaps"
    if snaps.exists():
        shutil.rmtree(snaps)
    subprocess.run(["npx", "--no-install", "hyperframes", "snapshot", str(proj), "--at", "0.5", "--no-end", "--keep",
                    "-o", str(snaps), "--timeout", "20000"], cwd=ROOT, check=True, capture_output=True)
    shot = next(snaps.glob("at-0.5s.png"))
    out = ep.output / "cover.png"
    Image.open(shot).convert("RGB").save(out)
    Image.open(shot).convert("RGB").save(ep.output / "cover.jpg", "JPEG", quality=92, optimize=True)   # IG upload: JPEG sRGB
    g = TOK["safeZone"]["coverGridCrop"]
    Image.open(out).crop((g["x"], g["y"], g["x"] + g["w"], g["y"] + g["h"])).save(ep.output / "cover_grid_preview.png")
    print(f"cover: {out}")
    return out


if __name__ == "__main__":
    cover(sys.argv[1])
