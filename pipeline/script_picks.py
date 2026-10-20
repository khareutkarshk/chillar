#!/usr/bin/env python3
"""Apply the script-reviewer's joke picks — a punch-up without another writer round.

  script_picks.py episodes/<ep> [--review notes/script-review-2.md] [--dry]

The writer may give its weakest 2–3 joke lines written alternatives as `{alt: "…"}` tags. The reviewer
reads them and writes one line in its review: `picks: L5=2, L11=0` (0 = keep the line as written, n = the
n-th alt). This swaps each picked alt in (the alt's own [F#] replaces the line's; [JOKE] and the other
{…} directions stay) and strips every remaining {alt: …} so nothing downstream ever sees one.
Runs after every script review (produce.py); harmless when there are no alts.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.episode import FACT_RE, load  # noqa: E402

ALT_RE = re.compile(r"\{\s*alt\s*:\s*[\"“]?([^}]*?)[\"”]?\s*\}")
PICKS_RE = re.compile(r"^picks:\s*(.*)$", re.M | re.I)


def latest_review(ep_dir: Path) -> Path | None:
    rs = sorted((ep_dir / "notes").glob("script-review-*.md"), key=lambda p: int(re.sub(r"\D", "", p.stem) or 0))
    return rs[-1] if rs else None


def picks_of(review: Path | None) -> dict[str, int]:
    if not review or not review.exists():
        return {}
    m = PICKS_RE.search(review.read_text())
    return {k.upper(): int(v) for k, v in re.findall(r"(L\d+)\s*=\s*(\d+)", m.group(1))} if m else {}


def apply(ep_dir: str, review: Path | None = None, dry: bool = False) -> list[str]:
    ep = load(ep_dir)
    script = ep.dir / "script.md"
    text = script.read_text()
    picks = picks_of(review or latest_review(ep.dir))
    done = []
    for line in ep.lines:
        alts = ALT_RE.findall(line.raw)
        if not alts:
            continue
        new = ALT_RE.sub("", line.raw)
        k = picks.get(line.id, 0)
        if 1 <= k <= len(alts):
            alt = alts[k - 1].strip()
            facts = "" if FACT_RE.search(alt) else " ".join(f"[{f}]" for f in line.facts)
            tags = " ".join(re.findall(r"\[JOKE\]|\{[^}]*\}", new))
            new = " ".join(x for x in (alt, facts, tags) if x)
            done.append(f"{line.id}: alt {k} → {alt[:60]}")
        new = re.sub(r"[ \t]+", " ", new).strip()
        text = text.replace(line.raw, new, 1)
    if not dry and text != script.read_text():
        script.write_text(text)
    return done


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("episode")
    ap.add_argument("--review", type=Path)
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    done = apply(a.episode, a.review, a.dry)
    print("script picks: " + ("; ".join(done) if done else "none applied (alts stripped)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
