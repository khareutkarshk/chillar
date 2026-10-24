#!/usr/bin/env python3
"""Reusable facts library (brand/facts-library.md) + a local cache of primary sources.

  facts_library.py list                         every entry, with age and whether it is stale
  facts_library.py stale                        only entries that must be re-verified (exit 1 if any)
  facts_library.py copy episodes/<ep> L-ID ...  append entries to the episode's facts.md as new F#
                                                (notes carry "library:L-ID" so the fact-checker can skip
                                                re-verifying fresh ones)
  facts_library.py fresh episodes/<ep>          which episode facts came from a fresh library entry
                                                (the fact-checker only spot-checks those)
  facts_library.py cache <url> [name]           download a source (PDF/HTML) into brand/sources/ with a
                                                browser User-Agent; logged in brand/sources/index.json

Stale = checked > 90 days ago, or changes=budget and a Union Budget (1 Feb) has passed since checked.
"""
from __future__ import annotations

import datetime as dt
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.common import BRAND, slug  # noqa: E402

LIB = BRAND / "facts-library.md"
SRC = BRAND / "sources"
MAX_AGE = 90
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/127.0.0.0 Safari/537.36")


def entries() -> dict[str, dict]:
    out = {}
    for row in LIB.read_text().splitlines():
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        if len(cells) >= 5 and re.fullmatch(r"L-[A-Z0-9-]+", cells[0]):
            out[cells[0]] = {"id": cells[0], "claim": cells[1], "source": cells[2], "checked": cells[3],
                             "changes": cells[4], "notes": cells[5] if len(cells) > 5 else ""}
    return out


def why_stale(e: dict, today: dt.date | None = None) -> str:
    today = today or dt.date.today()
    try:
        checked = dt.date.fromisoformat(e["checked"])
    except ValueError:
        return "no valid checked date"
    age = (today - checked).days
    if age > MAX_AGE:
        return f"checked {age} days ago (> {MAX_AGE})"
    if e["changes"] == "budget":
        budget = dt.date(today.year, 2, 1) if today >= dt.date(today.year, 2, 1) else dt.date(today.year - 1, 2, 1)
        if checked < budget:
            return f"Union Budget {budget} came after the last check"
    return ""


def next_fid(facts_md: str) -> int:
    ids = [int(m) for m in re.findall(r"^\|\s*F(\d+)\s*\|", facts_md, re.M)]
    return max(ids, default=0) + 1


def cmd_copy(ep: Path, ids: list[str]) -> int:
    lib = entries()
    fp = ep / "facts.md"
    text = fp.read_text() if fp.exists() else (
        f"# Facts — {ep.name}\n\nEvery number or factual claim in script.md must cite one of these ids, e.g. `[F1]`.\n\n"
        "| id | claim | source | checked | notes |\n|----|-------|--------|---------|-------|\n")
    rows, n = [], next_fid(text)
    for lid in ids:
        e = lib.get(lid)
        if not e:
            print(f"  ✗ {lid}: not in {LIB.name}")
            return 1
        stale = why_stale(e)
        if stale:
            print(f"  ! {lid}: STALE ({stale}) — the fact-checker must re-verify it")
        rows.append(f"| F{n} | {e['claim']} | {e['source']} | {e['checked']} | library:{lid}. {e['notes']} |")
        print(f"  F{n} ← {lid}")
        n += 1
    # insert after the last table row of the first table
    lines = text.splitlines()
    last = max((i for i, l in enumerate(lines) if l.strip().startswith("|")), default=len(lines) - 1)
    lines[last + 1:last + 1] = rows
    fp.write_text("\n".join(lines) + "\n")
    return 0


def cmd_fresh(ep: Path) -> int:
    lib = entries()
    for row in (ep / "facts.md").read_text().splitlines():
        m = re.match(r"^\|\s*(F\d+)\s*\|.*library:(L-[A-Z0-9-]+)", row)
        if m:
            e = lib.get(m.group(2))
            state = "missing from library" if not e else (why_stale(e) or "fresh")
            print(f"{m.group(1)}  {m.group(2)}  {state}")
    return 0


def cmd_cache(url: str, name: str | None) -> int:
    # url and name come from agents reading the web: only http(s), only a plain filename inside brand/sources/
    if urllib.parse.urlsplit(url).scheme not in ("http", "https"):
        print(f"  ✗ not an http(s) URL: {url}")
        return 2
    if name is not None and not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,99}", name):
        print(f"  ✗ name must be a plain filename (letters, digits, . _ -): {name}")
        return 2
    SRC.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*", "Accept-Language": "en-IN,en;q=0.9"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data, ctype = r.read(), r.headers.get("Content-Type", "")
    ext = ".pdf" if "pdf" in ctype or url.lower().endswith(".pdf") else ".html"
    fn = SRC / ((name or slug(re.sub(r"^https?://", "", url), 80)) + ext)
    fn.write_bytes(data)
    idx_p = SRC / "index.json"
    idx = json.loads(idx_p.read_text()) if idx_p.exists() else {}
    idx[url] = {"file": fn.name, "fetched": dt.date.today().isoformat(), "bytes": len(data)}
    idx_p.write_text(json.dumps(idx, indent=1))
    print(fn)
    return 0


def main() -> int:
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    if a[0] in ("list", "stale"):
        bad = 0
        for e in entries().values():
            s = why_stale(e)
            bad += bool(s)
            if a[0] == "list" or s:
                print(f"{e['id']:<22} {e['checked']}  {e['changes']:<12} {'STALE: ' + s if s else 'fresh'}")
        return 1 if a[0] == "stale" and bad else 0
    if a[0] == "copy" and len(a) >= 3:
        return cmd_copy(Path(a[1]), a[2:])
    if a[0] == "fresh" and len(a) == 2:
        return cmd_fresh(Path(a[1]))
    if a[0] == "cache" and len(a) >= 2:
        return cmd_cache(a[1], a[2] if len(a) > 2 else None)
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
