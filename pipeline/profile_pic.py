#!/usr/bin/env python3
"""Instagram profile pictures: Chillar on a softly lit field, one per theme.

  profile_pic.py [--expr side-eye]  -> brand/profile/dp-<theme>.png/.jpg (1080x1080) + dp-preview.png
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_composition import TOK, build  # noqa: E402
from lib.common import BRAND, ROOT  # noqa: E402

OUT = BRAND / "profile"
FIELD = {"pastel": "note10", "calm": "note10", "night": "note10"}   # mocha · sage · forest


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--expr", default="side-eye")
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    tiles = []
    for theme in TOK["themes"]:
        proj = OUT / ".build"
        shutil.rmtree(proj, ignore_errors=True)
        build({"duration": 1.0, "title": "dp", "theme": theme, "scenes": [
            {"id": "bg", "component": "chapter-field", "params": {"chapters": [{"start": 0, "field": FIELD[theme]}], "grain": True},
             "start": 0, "duration": 1.0, "track": 0},
            {"id": "dp", "component": "avatar", "params": {"expr": a.expr}, "start": 0, "duration": 1.0, "track": 1}]}, proj, "dp")
        snaps = OUT / ".snaps"
        shutil.rmtree(snaps, ignore_errors=True)
        subprocess.run(["npx", "--no-install", "hyperframes", "snapshot", str(proj), "--at", "0.5", "--no-end", "--keep",
                        "-o", str(snaps), "--timeout", "20000"], cwd=ROOT, check=True, capture_output=True)
        sq = Image.open(next(snaps.glob("at-0.5s.png"))).convert("RGB").crop((0, 420, 1080, 1500))
        sq.save(OUT / f"dp-{theme}.png")
        sq.save(OUT / f"dp-{theme}.jpg", "JPEG", quality=95)
        tiles.append((theme, sq))
        shutil.rmtree(proj, ignore_errors=True)
        shutil.rmtree(snaps, ignore_errors=True)
    # preview: each as the circle Instagram shows, at full size and at feed size (110 px)
    W = 420
    prev = Image.new("RGB", (len(tiles) * (W + 40) + 40, W + 220), "#ECEAE4")
    mask = Image.new("L", (W, W), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, W - 1, W - 1), fill=255)
    for i, (theme, sq) in enumerate(tiles):
        x = 40 + i * (W + 40)
        prev.paste(sq.resize((W, W)), (x, 30), mask)
        small = sq.resize((110, 110))
        m2 = Image.new("L", (110, 110), 0)
        ImageDraw.Draw(m2).ellipse((0, 0, 109, 109), fill=255)
        prev.paste(small, (x + W // 2 - 55, W + 60), m2)
        ImageDraw.Draw(prev).text((x, W + 190), theme, fill="#151515")
    prev.save(OUT / "dp-preview.png")
    print(f"profile pictures: {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
