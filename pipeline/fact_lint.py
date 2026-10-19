#!/usr/bin/env python3
"""Mechanical fact gate: every number/claim line cites a fact; every fact has a source URL.

  fact_lint.py episodes/<ep>          exit 0 = clean, 1 = problems (render is blocked)
  fact_lint.py episodes/<ep> --json   machine-readable report

/fact-check does the human-level verification (is the source still right, is it outdated);
this script only guarantees nothing slips through uncited.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.episode import load  # noqa: E402

NUMBERISH = re.compile(
    r"(₹|\d|%|\b(lakh|crore|hazaar|hazar|thousand|million|billion|percent|pratishat|"
    r"ek|do|teen|char|paanch|das|sau)\b)", re.I)
# common spoken words that collide with number words in Hinglish ("do" = do / two)
SOFT = re.compile(r"\b(ek|do|teen|char|paanch|das|sau)\b", re.I)
STALE_DAYS = 180


def lint(ep_dir: str) -> dict:
    ep = load(ep_dir)
    problems, warnings = [], []
    for fid, f in ep.facts.items():
        if not f["source"]:
            problems.append(f"{fid}: no source URL")
        try:
            age = (dt.date.today() - dt.date.fromisoformat(f["checked"])).days
            if age > STALE_DAYS:
                warnings.append(f"{fid}: last checked {age} days ago — re-verify")
        except ValueError:
            problems.append(f"{fid}: 'checked' date missing or not YYYY-MM-DD")
    for line in ep.lines:
        for fid in line.facts:
            if fid not in ep.facts:
                problems.append(f"{line.id} cites {fid}, which is not in facts.md")
        hard = NUMBERISH.search(SOFT.sub("", line.spoken))
        soft = SOFT.search(line.spoken)
        if hard and not line.facts:
            problems.append(f"{line.id} has a number/claim but no [F#]: \"{line.spoken}\"")
        elif soft and not line.facts and not hard:
            warnings.append(f"{line.id} may contain a number word ('{soft.group(0)}') — cite if it's a figure")
    unused = set(ep.facts) - {f for l in ep.lines for f in l.facts}
    for fid in sorted(unused):
        warnings.append(f"{fid} is never cited in script.md")
    jokes = [l.id for l in ep.lines if l.joke]
    return {"episode": ep.name, "ok": not problems, "problems": problems, "warnings": warnings,
            "joke_lines": jokes, "facts": len(ep.facts), "lines": len(ep.lines)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    r = lint(a.episode)
    if a.json:
        print(json.dumps(r, indent=2, ensure_ascii=False))
    else:
        print(f"fact lint — {r['episode']}: {r['lines']} lines, {r['facts']} facts")
        for p in r["problems"]:
            print(f"  ✗ {p}")
        for w in r["warnings"]:
            print(f"  ! {w}")
        if r["joke_lines"]:
            print(f"  · joke lines to punch up: {', '.join(r['joke_lines'])}")
        print("  ✓ clean" if r["ok"] else "  RENDER BLOCKED until fixed (or --allow-unsourced)")
    return 0 if r["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
