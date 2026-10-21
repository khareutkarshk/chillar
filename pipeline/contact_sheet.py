#!/usr/bin/env python3
"""Contact sheet (one frame every 3 s) + automatic palette check + safe-zone guide sheet.

  contact_sheet.py episodes/<ep> [--video output/final.mp4] [--every 3]
  -> output/contact_sheet.png, output/contact_sheet_guides.png, .cache/palette_report.json
"""
from __future__ import annotations

import argparse
import itertools
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.common import BRAND  # noqa: E402
from lib.episode import load  # noqa: E402

TOK = json.loads((BRAND / "tokens.json").read_text())
from lib.theme import palette_hexes  # noqa: E402


def pal_array(theme: str | None = None) -> np.ndarray:
    return np.array([[int(h[i:i + 2], 16) for i in (1, 3, 5)] for h in palette_hexes(theme)], float)


PAL = pal_array()
SAFE = TOK["safeZone"]
OFF_DIST = 22.0   # RGB distance from any palette colour or palette-pair blend (anti-aliasing, soft light, shadows)


def frame_at(video: Path, t: float, out: Path) -> bool:
    r = subprocess.run(["ffmpeg", "-hide_banner", "-y", "-ss", f"{t:.3f}", "-i", str(video), "-frames:v", "1", str(out)],
                       capture_output=True)
    return r.returncode == 0 and out.exists()


def off_palette(img: Image.Image) -> tuple[float, np.ndarray]:
    a = np.asarray(img.convert("RGB").resize((270, 480)), float).reshape(-1, 3)
    best = np.min(np.linalg.norm(a[:, None, :] - PAL[None], axis=2), axis=1)
    for i, j in itertools.combinations(range(len(PAL)), 2):   # distance to each blend segment
        p, q = PAL[i], PAL[j]
        d = q - p
        tt = np.clip(((a - p) @ d) / (d @ d), 0, 1)
        dist = np.linalg.norm(a - (p + tt[:, None] * d), axis=1)
        best = np.minimum(best, dist)
    mask = (best > OFF_DIST).reshape(480, 270)
    # ignore high-contrast edges: H.264 4:2:0 chroma subsampling fringes every sharp ink edge.
    # A genuinely off-palette SHAPE still has a flat interior, which is what we count.
    lum = np.asarray(img.convert("L").resize((270, 480)), float)
    g = np.zeros_like(lum)
    g[1:-1, 1:-1] = np.maximum.reduce([abs(lum[1:-1, 2:] - lum[1:-1, :-2]), abs(lum[2:, 1:-1] - lum[:-2, 1:-1])])
    edge = g > 24
    edge = edge | np.roll(edge, 1, 0) | np.roll(edge, -1, 0) | np.roll(edge, 1, 1) | np.roll(edge, -1, 1)
    mask &= ~edge
    return float(mask.mean()), mask


def guides(im: Image.Image) -> Image.Image:
    g = im.copy().convert("RGB")
    d = ImageDraw.Draw(g)
    W, H = g.size
    sx, sy = W / 1080, H / 1920
    box = [SAFE["left"] * sx, SAFE["top"] * sy, W - SAFE["right"] * sx, H - SAFE["bottom"] * sy]
    d.rectangle(box, outline="#D9302C", width=2)
    cb = SAFE["captionBand"]
    d.rectangle([box[0], cb[0] * sy, box[2], cb[1] * sy], outline="#1E9E58", width=2)
    c = SAFE["coverGridCrop"]
    d.rectangle([0, c["y"] * sy, W - 1, (c["y"] + c["h"]) * sy], outline="#6B675E", width=1)
    return g


def sheet(ep_dir: str, video: Path | None = None, every: float = 3.0) -> Path:
    global PAL
    ep = load(ep_dir)
    PAL = pal_array(ep.theme)
    video = video or ep.output / "final.mp4"
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                                "default=nw=1:nk=1", str(video)], capture_output=True, text=True).stdout)
    times = list(np.arange(0, dur - 0.05, every)) + [max(0, dur - 0.1)]
    try:    # the punchline's last frame, just before the outro: the 3 s grid skipped it and a coin on the payoff
            # headline shipped (2026-10-31)
        oc = json.loads((ep.cache / "scenes.resolved.json").read_text()).get("outro_start")
        if oc and not any(oc - 0.6 <= t < oc for t in times):
            times = sorted(times + [max(0.0, oc - 0.15)])
    except (OSError, ValueError):
        pass
    fdir = ep.cache / "frames"
    fdir.mkdir(exist_ok=True)
    tw, th, cols = 360, 640, 4
    font = ImageFont.truetype(str(BRAND / "fonts" / "Mukta-ExtraBold.ttf"), 26)
    rows = (len(times) + cols - 1) // cols
    S = Image.new("RGB", (cols * (tw + 20) + 20, rows * (th + 56) + 20), "#ECEAE4")
    G = S.copy()
    report = []
    for k, t in enumerate(times):
        fp = fdir / f"f{k:03d}.png"
        if not frame_at(video, t, fp):
            continue
        im = Image.open(fp).convert("RGB")
        frac, mask = off_palette(im)
        report.append({"t": round(float(t), 2), "off_palette_pct": round(frac * 100, 2), "frame": str(fp)})
        x, y = 20 + (k % cols) * (tw + 20), 20 + (k // cols) * (th + 56)
        small = im.resize((tw, th))
        S.paste(small, (x, y))
        G.paste(guides(small), (x, y))
        for canvas in (S, G):
            d = ImageDraw.Draw(canvas)
            d.rectangle([x - 2, y - 2, x + tw + 1, y + th + 1], outline="#151515", width=3)
            flag = "  ⚠ palette" if frac > 0.004 else ""
            d.text((x, y + th + 10), f"{t:5.1f}s{flag}", fill="#D9302C" if flag else "#151515", font=font)
        if frac > 0.004:
            heat = Image.fromarray(np.uint8(mask * 255)).resize(im.size)
            red = Image.new("RGB", im.size, "#D9302C")
            Image.composite(red, im.convert("L").convert("RGB"), heat).save(fdir / f"f{k:03d}_offpalette.png")
    out = ep.output / "contact_sheet.png"
    S.save(out)
    G.save(ep.output / "contact_sheet_guides.png")
    (ep.cache / "palette_report.json").write_text(json.dumps(report, indent=2))
    bad = [r for r in report if r["off_palette_pct"] > 0.4]
    print(f"contact sheet: {out} ({len(report)} frames)  palette: "
          + ("clean" if not bad else f"{len(bad)} frame(s) >0.4% off-palette: " + ", ".join(f"{r['t']}s" for r in bad)))
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    ap.add_argument("--video", type=Path)
    ap.add_argument("--every", type=float, default=3.0)
    a = ap.parse_args()
    sheet(a.episode, a.video, a.every)
