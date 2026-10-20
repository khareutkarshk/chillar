#!/usr/bin/env python3
"""A hard spending stop for a batch of reels — counts every Claude session on this machine (the master, its
helpers and every headless produce.py agent), not just one episode's agents.

  budget.py start --pct-now 53 --stop-at-pct 70 [--usd-per-pct 4.5]   arm it (writes .cache/batch_budget.json)
  budget.py check                                                     spent / cap / projected weekly %; exit 3 = over
  budget.py stop                                                      disarm

The weekly limit is shown as a %, but nothing local can read it; ccusage can read the API-equivalent dollars of
every Claude Code session. --usd-per-pct converts one to the other (calibrated 2026-10-21: ≈ $4.9–6.4 of ccusage
cost per weekly %; 4.5 is the cautious default, so the stop comes early, never late).
While armed, produce.py runs `check` before every agent (cached for 3 min) and stops with exit 3
("batch budget") once spent ≥ cap. The master stops everything on that stop.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.common import ROOT  # noqa: E402

LEDGER = ROOT / ".cache" / "batch_budget.json"
CACHE_S = 180
CLAUDE = ("claude", "opus", "sonnet", "haiku", "fable")


def claude_usd_since(day: str) -> float:
    """API-equivalent $ of every Claude model since <day> (YYYYMMDD), from ccusage's local logs."""
    r = subprocess.run(["npx", "--yes", "ccusage@latest", "daily", "--since", day, "--json"], cwd=ROOT,
                       capture_output=True, text=True, timeout=180)
    rows = json.loads(r.stdout).get("daily", [])
    return round(sum(m.get("cost", 0) for row in rows for m in row.get("modelBreakdowns", [])
                     if any(k in m.get("modelName", "").lower() for k in CLAUDE)), 2)


def state() -> dict | None:
    return json.loads(LEDGER.read_text()) if LEDGER.exists() else None


def check(force: bool = False) -> dict:
    s = state()
    if not s:
        return {"armed": False}
    if force or time.time() - s.get("checked_at", 0) > CACHE_S:
        s["spent"] = round(claude_usd_since(s["since"]) - s["baseline"], 2)
        s["checked_at"] = time.time()
        LEDGER.write_text(json.dumps(s, indent=1))
    s["pct_now"] = round(s["pct_start"] + s["spent"] / s["usd_per_pct"], 1)
    s["over"] = s["spent"] >= s["cap"]
    s["armed"] = True
    return s


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    st = sub.add_parser("start")
    st.add_argument("--pct-now", type=float, required=True, help="weekly limit used right now, %% (from /usage)")
    st.add_argument("--stop-at-pct", type=float, required=True)
    st.add_argument("--usd-per-pct", type=float, default=4.5)
    sub.add_parser("check")
    sub.add_parser("stop")
    a = ap.parse_args()
    if a.cmd == "start":
        since = dt.date.today().strftime("%Y%m%d")
        s = {"since": since, "baseline": claude_usd_since(since), "pct_start": a.pct_now, "usd_per_pct": a.usd_per_pct,
             "cap": round((a.stop_at_pct - a.pct_now) * a.usd_per_pct, 2), "stop_at_pct": a.stop_at_pct,
             "spent": 0.0, "checked_at": time.time(), "armed_at": dt.datetime.now().isoformat(timespec="seconds")}
        LEDGER.parent.mkdir(exist_ok=True)
        LEDGER.write_text(json.dumps(s, indent=1))
        print(f"budget armed: cap ${s['cap']} (≈ {a.pct_now}% → {a.stop_at_pct}% of the weekly limit at "
              f"${a.usd_per_pct}/%), baseline ${s['baseline']} already spent today")
        return 0
    if a.cmd == "stop":
        LEDGER.unlink(missing_ok=True)
        print("budget disarmed")
        return 0
    s = check(force=True)
    if not s["armed"]:
        print("budget: not armed")
        return 0
    print(f"budget: ${s['spent']} of ${s['cap']} · ≈ {s['pct_now']}% weekly (stop at {s['stop_at_pct']}%)"
          + (" · OVER — stop everything" if s["over"] else ""))
    return 3 if s["over"] else 0


if __name__ == "__main__":
    sys.exit(main())
