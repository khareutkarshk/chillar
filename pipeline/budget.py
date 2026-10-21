#!/usr/bin/env python3
"""A hard spending stop for a batch of reels — counts every Claude session on this machine (the master, its
helpers and every headless produce.py agent), not just one episode's agents. Headless agents run with
--no-session-persistence, so ccusage never sees them: their cost is read from episodes/*/notes/usage.jsonl instead
(the 2026-10-28 batch showed $0.63 spent while its agents had spent ≈ $13).

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
import os
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
    """API-equivalent $ of every Claude model since <day> (YYYYMMDD), from ccusage's local logs.
    Raises RuntimeError when ccusage can't answer (offline npx, a malformed log line) — callers decide."""
    try:
        r = subprocess.run(["npx", "--yes", "ccusage@latest", "daily", "--since", day, "--json"], cwd=ROOT,
                           capture_output=True, text=True, timeout=180)
        rows = json.loads(r.stdout).get("daily", [])
    except (subprocess.TimeoutExpired, json.JSONDecodeError, OSError, AttributeError) as e:
        raise RuntimeError(f"ccusage unavailable: {e}") from e
    return round(sum(m.get("cost", 0) for row in rows for m in row.get("modelBreakdowns", [])
                     if any(k in m.get("modelName", "").lower() for k in CLAUDE)), 2)


def agent_usd_since(armed_at: str) -> float:
    """$ of every headless produce.py agent run since the batch was armed, from the episodes' usage.jsonl."""
    total = 0.0
    for log in (ROOT / "episodes").glob("*/notes/usage.jsonl"):
        for line in log.read_text(errors="replace").splitlines():
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if str(row.get("at", "")) >= armed_at:
                total += float(row.get("cost") or 0)
    return round(total, 2)


def state() -> dict | None:
    for _ in range(3):              # two reels may write it at once; writes are atomic, so a retry suffices
        if not LEDGER.exists():
            return None
        try:
            return json.loads(LEDGER.read_text())
        except (json.JSONDecodeError, OSError):
            time.sleep(0.5)
    return None


def save(s: dict) -> None:
    tmp = LEDGER.with_suffix(f".{os.getpid()}.tmp")
    tmp.write_text(json.dumps(s, indent=1))
    os.replace(tmp, LEDGER)


def check(force: bool = False) -> dict:
    """Never raises: a failed ccusage read keeps the last known spend (logged as stale) so a network blip
    can't kill a reel mid-stage; the next check retries."""
    s = state()
    if not s:
        return {"armed": False}
    if force or time.time() - s.get("checked_at", 0) > CACHE_S:
        try:
            s["spent"] = round(claude_usd_since(s["since"]) - s["baseline"] + agent_usd_since(s["armed_at"]), 2)
            s.pop("stale", None)
        except RuntimeError as e:
            s["stale"] = str(e)[:200]
        s["checked_at"] = time.time()
        save(s)
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
        save(s)
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
          + (" · OVER — stop everything" if s["over"] else "")
          + (f" · ⚠ stale (last good read kept): {s['stale']}" if s.get("stale") else ""))
    return 3 if s["over"] else 0


if __name__ == "__main__":
    sys.exit(main())
