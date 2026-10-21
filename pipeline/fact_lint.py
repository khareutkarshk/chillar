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
from lib.common import BRAND  # noqa: E402
from lib.episode import load  # noqa: E402

FORMATS = json.loads((BRAND / "tokens.json").read_text())["formats"]

NUMBERISH = re.compile(
    r"(₹|\d|%|\b(lakh|crore|hazaar|hazar|thousand|million|billion|percent|pratishat|"
    r"ek|do|teen|char|paanch|das|sau)\b)", re.I)
# common spoken words that collide with number words in Hinglish ("do" = do / two)
SOFT = re.compile(r"\b(ek|do|teen|char|paanch|das|sau)\b", re.I)
STALE_DAYS = 180
WPS = 3.2                                   # Sunny @ pace 1.2 after clean (measured: 3.09 / 3.33 on the first two reels)
OUTRO_S = 3.5                               # outro receipt after the voice
LAUGH_MIN = {"30": 3, "60": 6, "90": 9}
FIRST_LAUGH_S = 5.0
# absolutes that a fact rarely supports — flag them on cited lines so the writer checks before review
ABSOLUTE = re.compile(r"\b(hamesha|kabhi nahi|kabhi bhi nahi|har baar|sab kuch|guaranteed|guarantee|pakka|always|never|forever)\b", re.I)
MAX_LINE_WORDS = 14
# the only URL-less facts allowed (creator's call, 2026-10-20): an invented example the script frames as one,
# or arithmetic on other facts ("computed from F1, F3") — and those must themselves be sourced or hypothetical
HYPOTHETICAL = re.compile(r"\bhypothetical\b", re.I)
COMPUTED = re.compile(r"\bcomputed from\b", re.I)
# a fact that is an example (a typical slip, an invented offer, a worked balance) must be *said* as one the first
# time the voice uses it — "₹13,532 gayab" stated as everyone's salary failed 4 of 6 first script reviews
EXAMPLE_CLAIM = re.compile(r"^\W*(illustrative|hypothetical|worked example|example|typical)\b", re.I)
FRAMING = re.compile(r"\b(maan lo|maano|maan le|man lo|socho|soch lo|imagine|example|misaal|jaise|jaisa|agar|typical|"
                     r"aksar|kuch aisa|kuch aise|kisi|ek (offer|slip|bank|app|banda|bandi|dost|cart|phone|card|"
                     r"loan|salary|naukri|company|shop|dukaan|sale)|"
                     # a first-person story is framing too: "mere card pe ₹10,000" is one person's bill, not a law
                     r"maine|mera|meri|mere|mujhe|humne|hamara|mummy|papa|mom|dad)\b", re.I)


def is_example(f: dict) -> bool:
    return bool(EXAMPLE_CLAIM.search(f["claim"]) or HYPOTHETICAL.search(f.get("source_text", ""))
                or COMPUTED.search(f.get("source_text", "")))
MEME_CUE = re.compile(r"\{meme:\s*(M\d+)", re.I)
NUM_TOKEN = re.compile(r"₹?\d[\d,]*(?:\.\d+)?%?(?:-\d+)?")


def spoken_len(tok: str) -> int:
    """How many words the voice says for a written number token (Hinglish/English reading)."""
    t = tok
    n = 1 if t.startswith("₹") else 0           # "rupaye"
    t = t.lstrip("₹")
    if t.endswith("%"):
        n += 1                                  # "percent"
        t = t[:-1]
    if re.fullmatch(r"\d{4}-\d{2}", t):        # 2025-26 -> "twenty twenty-five twenty-six"
        return n + 4
    whole, _, dec = t.partition(".")
    if dec:
        n += 1 + len(dec)                       # "point two five"
    v = int(whole.replace(",", "") or 0)
    if v == 0:
        return n + 1
    for size in (10_000_000, 100_000, 1000, 100):   # crore, lakh, hazaar, sau: "<k> <unit>"
        if v >= size:
            n += 2
            v %= size
    return n + (1 if v else 0)


# "Hisaab: …", "Group chat: …", "Rule: …" — a 1–3 word label and a colon, outside a quote
LABEL_COLON = re.compile(r"^((?:[\w'₹]+\s?){1,3}):\s")


def script_lint(ep) -> list[str]:
    """Self-check the writer runs before handing off: spoken length, laughs, absolutes, long lines."""
    out = []
    fmt = ep.format
    lo, hi = FORMATS[fmt]["seconds"]
    words = spoken = 0
    first_joke_at = None
    for line in ep.lines:
        toks = line.spoken.split()
        w = len(toks)
        sp = sum(spoken_len(m) - 1 for m in NUM_TOKEN.findall(line.spoken)) + w
        if line.joke and first_joke_at is None:
            first_joke_at = (spoken + sp) / WPS            # the punchline ends the line
        words += w
        spoken += sp
        if w > MAX_LINE_WORDS:
            out.append(f"{line.id} is {w} words (> {MAX_LINE_WORDS}) — hard to say in one breath")
        if (m := LABEL_COLON.match(line.spoken)) and not re.match(r"maan lo|socho|matlab", m.group(1), re.I):
            out.append(f"{line.id} opens with '{m.group(0).strip()}' — a label-plus-colon reads as caption-speak when Sunny "
                       f"says it; say it as a sentence (\"Hisaab simple hai —\", \"Group chat mein…\")")
        for alt in re.findall(r"\{\s*alt\s*:([^}]*)\}", line.raw):
            if re.search(r"\d", alt) and not re.search(r"\[F\d+\]", alt):
                out.append(f"{line.id} alt has a number without its [F#]: {alt.strip()[:50]}")
        if line.facts and (m := ABSOLUTE.search(line.spoken)):
            out.append(f"{line.id} says '{m.group(0)}' — does {', '.join(line.facts)} support an absolute? \"{line.spoken}\"")
    secs = spoken / WPS + OUTRO_S
    if not lo <= secs <= hi:
        out.append(f"spoken length ≈ {spoken} words with numbers read in full ≈ {secs:.0f} s incl. outro — outside {lo}–{hi} s for {fmt} s")
    jokes = sum(1 for l in ep.lines if l.joke)
    if jokes < LAUGH_MIN[fmt] + 1:
        out.append(f"{jokes} [JOKE] lines — minimum {LAUGH_MIN[fmt]} real laughs; aim for {LAUGH_MIN[fmt] + 1}+ so one dud doesn't fail review")
    if first_joke_at is None or first_joke_at > FIRST_LAUGH_S:
        out.append(f"first laugh lands at ≈ {first_joke_at or 0:.1f} s — must be by {FIRST_LAUGH_S:.0f} s")
    out.insert(0, f"script: {words} words written · ≈ {spoken} spoken (numbers in full) · ≈ {secs:.0f} s incl. outro · {jokes} jokes")
    return out


def lint(ep_dir: str) -> dict:
    ep = load(ep_dir)
    problems, warnings = [], []
    for fid, f in ep.facts.items():
        src = f.get("source_text", "")
        if f["source"]:
            pass
        elif HYPOTHETICAL.search(src):
            warnings.append(f"{fid}: hypothetical — the script must frame it as an example, never as a real offer")
        elif COMPUTED.search(src):
            base = re.findall(r"F\d+", src)
            bad = [b for b in base if b not in ep.facts or not (ep.facts[b]["source"]
                   or HYPOTHETICAL.search(ep.facts[b].get("source_text", "")))]
            if not base or bad:
                problems.append(f"{fid}: computed from {', '.join(bad) or '?'} — name sourced (or hypothetical) facts")
        else:
            problems.append(f"{fid}: no source URL (or mark it 'hypothetical' / 'computed from F#')")
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
    # examples said as examples: the first line citing one (or the line before it) carries a framing cue
    first_use: dict[str, int] = {}
    for i, line in enumerate(ep.lines):
        for fid in line.facts:
            first_use.setdefault(fid, i)
    framed: set[str] = set()
    for fid, i in sorted(first_use.items(), key=lambda kv: kv[1]):
        f = ep.facts.get(fid)
        if not f or not is_example(f):
            continue
        refs = set(re.findall(r"F\d+", " ".join((f["claim"], f.get("notes", ""), f.get("source_text", ""))))) - {fid}
        said = " ".join(l.spoken for l in ep.lines[max(0, i - 1):i + 1])
        if refs & framed or FRAMING.search(said):        # built on an example the viewer already heard framed
            framed.add(fid)
        else:
            problems.append(f"{ep.lines[i].id} is the first line citing {fid}, an example/hypothetical fact, but says it as "
                            f"a general truth — frame it as one (\"maan lo\", \"ek typical …\", \"jaise\") in this line or "
                            f"the one before: \"{ep.lines[i].spoken}\"")
    # planned memes the last few reels already used (validate blocks them later, at a higher price)
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import memes
        rows = memes.culture_rows(ep)
        recent = memes.recent_use(ep.dir)
        for line in ep.lines:
            for mid in MEME_CUE.findall(" ".join(line.directions) + " " + line.raw):
                t = rows.get(mid.upper())
                if t and memes.norm_title(t) in recent:
                    warnings.append(f"{line.id} plans {mid} \"{t}\", already used in {recent[memes.norm_title(t)]} — "
                                    "pick another Culture now row")
        # a Culture now row is only as fresh as its `peaked` date: ≤ 1 old classic per reel, nothing past 6 months
        peaks, old = memes.culture_peaks(ep), {}
        for line in ep.lines:
            for mid in MEME_CUE.findall(" ".join(line.directions) + " " + line.raw):
                t = rows.get(mid.upper())
                age = peaks.get(memes.norm_title(t)) if t else None
                if age is not None and age > memes.FRESH_PEAK_MONTHS:
                    old.setdefault(mid.upper(), (line.id, t, age))
        for mid, (lid, t, age) in old.items():
            if age > memes.OLD_PEAK_MONTHS:
                warnings.append(f"{lid} plans {mid} \"{t}\", which peaked {age} months ago — stale meme; use a row that "
                                "peaked this month or cut the beat")
        if len(old) > memes.CLASSICS_PER_REEL:
            warnings.append(f"{len(old)} planned memes peaked over a month ago ({', '.join(old)}) — stale meme budget is "
                            f"≤ {memes.CLASSICS_PER_REEL} classic per reel; swap the rest for rows that peaked this month")
    except Exception as ex:          # memes/network trouble never blocks the fact gate
        warnings.append(f"recent-meme check skipped ({ex})")
    unused = set(ep.facts) - {f for l in ep.lines for f in l.facts}
    for fid in sorted(unused):
        warnings.append(f"{fid} is never cited in script.md")
    jokes = [l.id for l in ep.lines if l.joke]
    script = script_lint(ep) if ep.lines else []
    return {"episode": ep.name, "ok": not problems, "problems": problems, "warnings": warnings, "script": script,
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
        for x in r["script"]:
            print(f"  {'·' if x.startswith('script:') else '~'} {x}")
        if r["joke_lines"]:
            print(f"  · joke lines to punch up: {', '.join(r['joke_lines'])}")
        print("  ✓ clean" if r["ok"] else "  RENDER BLOCKED until fixed (or --allow-unsourced)")
    return 0 if r["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
