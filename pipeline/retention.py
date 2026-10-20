#!/usr/bin/env python3
"""Map a posted reel's Instagram retention curve to the script lines — the audience's own review.

  retention.py episodes/<ep> 0:100 3:71 8:60 15:52 30:44 45:38 [--views 12400] [--skip 41]
  -> episodes/<ep>/notes/retention.md (joke_log.py feeds its drops to the next reels' writers)

Read the points off Insights → the reel → "Retention" (seconds:percent still watching; 6–10 points is
plenty, always include 0 and 3). --skip is Instagram's skip rate (% who swiped away in the first 3 s).
Each stretch between two points gets a drop rate (% per second); a stretch losing viewers ≥ 1.5× faster
than the reel's median is a **drop**, listed with the lines the voice was saying (from .cache/words.json).
Free: no agent, no API.
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.episode import load  # noqa: E402

DROP_X = 1.5


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("episode")
    ap.add_argument("points", nargs="+", help="seconds:percent, e.g. 0:100 3:71 8:60")
    ap.add_argument("--views", type=int)
    ap.add_argument("--skip", type=float, help="Instagram skip rate, %%")
    a = ap.parse_args()
    ep = load(a.episode)
    pts = sorted((float(t), float(v)) for t, v in (p.split(":") for p in a.points))
    if len(pts) < 3:
        sys.exit("retention: give at least 3 points (include 0 and 3)")
    words = json.loads((ep.cache / "words.json").read_text())
    text = {l.id: l.spoken for l in ep.lines}

    def lines_between(t0: float, t1: float) -> list[str]:
        ids = []
        for w in words:
            if t0 <= w["start"] < t1 and w.get("line") and w["line"] not in ids:
                ids.append(w["line"])
        return ids

    spans = []
    for (t0, v0), (t1, v1) in zip(pts, pts[1:]):
        spans.append((t0, t1, v0 - v1, (v0 - v1) / max(t1 - t0, 0.1)))
    med = statistics.median(r for *_, r in spans) or 0.1
    out = [f"# Retention — {ep.name}", ""]
    meta = [f"views {a.views:,}" if a.views else "", f"skip rate {a.skip:g}%" if a.skip is not None else "",
            f"hold at 3 s {next((v for t, v in pts if t >= 3), pts[-1][1]):g}%", f"end {pts[-1][1]:g}% at {pts[-1][0]:g} s"]
    out += [" · ".join(m for m in meta if m), "", f"Median loss {med:.1f} %/s. Drops (≥ {DROP_X}× median):", ""]
    drops = 0
    for t0, t1, lost, rate in spans:
        if rate < DROP_X * med:
            continue
        drops += 1
        ids = lines_between(t0, t1)
        said = " / ".join(f"{i} \"{text.get(i, '')[:70]}\"" for i in ids[:3]) or "(no voice — check the visuals there)"
        out.append(f"- drop {t0:g}–{t1:g} s: −{lost:g}% ({rate:.1f} %/s) while saying {said}")
    if not drops:
        out.append("- no drop above the median rate — an even curve")
    out += ["", "All stretches:", ""] + [f"  {t0:g}–{t1:g} s  −{lost:g}%  ({rate:.1f} %/s)" for t0, t1, lost, rate in spans]
    dest = ep.dir / "notes" / "retention.md"
    dest.write_text("\n".join(out) + "\n")
    print("\n".join(out[:6 + drops]))
    print(f"→ {dest.relative_to(ep.dir.parent.parent)} (joke_log.py picks the drops up for the next script)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
