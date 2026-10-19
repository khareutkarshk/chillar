#!/usr/bin/env python3
"""Render every component's example through the real HyperFrames runtime and tile the
settled frames into components/_gallery/gallery.png (+ components/<name>/preview.png).

  component_gallery.py [name ...]      # default: all components
  component_gallery.py --mid           # also capture a mid-animation frame per component
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_composition import all_components, build, component_meta  # noqa: E402
from lib.common import BRAND, ROOT  # noqa: E402
import json  # noqa: E402

TOK = json.loads((BRAND / "tokens.json").read_text())
FIELD_CYCLE = ["note10", "note20", "note50", "note500", "note2000", "bone"]

OUT = ROOT / "components" / "_gallery"
SKIP = {"captions", "chapter-field", "transition"}   # captions + field are shown under every tile


def demo_captions(start: float, dur: float) -> list[dict]:
    words = "ye caption ka active word hai".split()
    step = dur / len(words)
    ws = [{"text": w, "start": round(start + i * step, 3), "end": round(start + (i + 1) * step, 3)} for i, w in enumerate(words)]
    return [{"start": ws[0]["start"], "end": ws[2]["end"], "words": ws[:3]},
            {"start": ws[3]["start"], "end": ws[-1]["end"], "words": ws[3:]}]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("names", nargs="*")
    ap.add_argument("--mid", action="store_true")
    ap.add_argument("--theme", default=TOK["theme"], help=f"one of {sorted(TOK['themes'])}")
    a = ap.parse_args()
    names = [n for n in (a.names or all_components()) if n not in SKIP]

    scenes, shots, t, chapters = [], [], 0.0, []
    for k, n in enumerate(names):
        chapters.append({"start": round(t, 3), "field": FIELD_CYCLE[k % len(FIELD_CYCLE)]})
        meta = component_meta(n)
        d = max(float(meta.get("minDuration", 1.5)) + 0.8, 2.2)
        scenes.append({"id": f"g-{n}", "component": n, "params": meta.get("example", {}),
                       "start": round(t, 3), "duration": round(d, 3), "track": 2 if meta.get("layer") == "overlay" else 1})
        shots.append((n, round(t + d - 0.15, 3), round(t + 0.12, 3)))
        t += d
    total = round(t, 3)
    scenes.insert(0, {"id": "bg", "component": "chapter-field", "params": {"chapters": chapters, "grain": True},
                      "start": 0, "duration": total, "track": 0})
    caps = demo_captions(0, total) if "captions" in all_components() else []
    proj = OUT / "project"
    if proj.exists():
        shutil.rmtree(proj)
    build({"duration": total, "scenes": scenes, "captions": caps, "title": "Chillar component gallery", "theme": a.theme}, proj, "gallery")

    lint = subprocess.run(["npx", "--no-install", "hyperframes", "lint", str(proj)], cwd=ROOT, capture_output=True, text=True)
    print(lint.stdout[-2500:] or lint.stderr[-2500:])
    times = [s[1] for s in shots] + ([s[2] for s in shots] if a.mid else [])
    snap_dir = OUT / "snaps"
    if snap_dir.exists():
        shutil.rmtree(snap_dir)
    r = subprocess.run(["npx", "--no-install", "hyperframes", "snapshot", str(proj), "--at", ",".join(map(str, times)),
                        "--no-end", "--keep", "-o", str(snap_dir), "--timeout", "20000"],
                       cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout[-3000:], r.stderr[-3000:])
        return 1

    def snap(ts: float) -> Path:
        name = f"at-{('%g' % ts)}s.png"
        return snap_dir / name

    font = ImageFont.truetype(str(BRAND / "fonts" / "Mukta-ExtraBold.ttf"), 34)
    cols, tw, th = 4, 432, 768
    tiles = [(n, snap(ts)) for n, ts, _ in shots] + ([(n + " (mid)", snap(tm)) for n, _, tm in shots] if a.mid else [])
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (tw + 24) + 24, rows * (th + 70) + 24), "#ECEAE4")
    d = ImageDraw.Draw(sheet)
    for i, (n, p) in enumerate(tiles):
        x, y = 24 + (i % cols) * (tw + 24), 24 + (i // cols) * (th + 70)
        if p.exists():
            im = Image.open(p).convert("RGB")
            if not n.endswith("(mid)") and a.theme == TOK["theme"]:
                im.save(ROOT / "components" / n / "preview.png")
            sheet.paste(im.resize((tw, th)), (x, y))
        d.rectangle([x - 2, y - 2, x + tw + 1, y + th + 1], outline="#151515", width=3)
        fld = FIELD_CYCLE[(i % len(shots)) % len(FIELD_CYCLE)]
        d.text((x, y + th + 12), f"{n}  ·  {fld}", fill="#151515", font=font)
    name = "gallery.png" if a.theme == TOK["theme"] else f"gallery-{a.theme}.png"
    sheet.save(OUT / name)
    print(f"gallery: {OUT / name} ({len(tiles)} tiles, theme {a.theme})")
    import component_catalog
    component_catalog.main()       # keep components/_catalog.md (what the director reads) in step
    return 0


if __name__ == "__main__":
    sys.exit(main())
