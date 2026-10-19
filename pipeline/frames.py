#!/usr/bin/env python3
"""Pull review frames at 540×960 — half size, a quarter of the image tokens of a full 1080×1920
frame, still enough to judge layout and legibility. Hard cap of 12 frames per call.

  frames.py episodes/<ep> 3.4 8.2 21.37          explicit times (seconds)
  frames.py episodes/<ep> --qa                   the timestamps qa.py flagged (.cache/qa.json)
  frames.py episodes/<ep> 3.4 --full             one full-size frame (only to read small text)
  -> .cache/review/t<time>.png, paths printed one per line (frames older than the video are deleted first)
  Sizes: frames are 540×960 = HALF size — a 20 px glyph in a frame is 40 px in the reel.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.episode import load  # noqa: E402

CAP = 12


def grab(video: Path, t: float, out: Path, full: bool = False) -> bool:
    scale = [] if full else ["-vf", "scale=540:960:flags=lanczos"]
    r = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{t:.3f}", "-i", str(video),
                        "-frames:v", "1", *scale, str(out)], capture_output=True)
    return r.returncode == 0 and out.exists()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("episode")
    ap.add_argument("times", nargs="*", type=float)
    ap.add_argument("--qa", action="store_true", help="add the times flagged in .cache/qa.json")
    ap.add_argument("--full", action="store_true", help="full 1080×1920 (costs 4× the tokens)")
    ap.add_argument("--video", type=Path)
    a = ap.parse_args()
    ep = load(a.episode)
    video = a.video or ep.output / "final.mp4"
    if not video.exists():
        video = ep.cache / "video.mp4"
    times = list(a.times)
    if a.qa:
        q = ep.cache / "qa.json"
        times += json.loads(q.read_text()).get("frames_to_check", []) if q.exists() else []
    times = sorted(dict.fromkeys(round(t, 2) for t in times))
    if len(times) > CAP:
        print(f"frames: {len(times)} requested, cap is {CAP} per round — keeping the first {CAP}. "
              f"Use the contact sheet for the rest.", file=sys.stderr)
        times = times[:CAP]
    out = ep.cache / "review"
    out.mkdir(parents=True, exist_ok=True)
    # frames older than the video are from an earlier render — delete them so nobody judges a stale cut
    stale = [f for f in out.glob("*.png") if f.stat().st_mtime < video.stat().st_mtime]
    for f in stale:
        f.unlink()
    if stale:
        print(f"frames: removed {len(stale)} stale frame(s) from an earlier render", file=sys.stderr)
    for t in times:
        p = out / f"t{t:06.2f}{'_full' if a.full else ''}.png"
        if grab(video, t, p, a.full):
            print(p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
