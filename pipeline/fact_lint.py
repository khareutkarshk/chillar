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
OUTRO_S = 2.0                               # outro receipt after the voice (cuts on the last word, 1.9 s)
LAUGH_MIN = {"12": 1, "30": 3, "60": 6, "90": 9}
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


JARGON = [l.split("\t")[0] for l in (BRAND / "jargon.tsv").read_text().splitlines()
          if l.strip() and not l.startswith("#")] if (BRAND / "jargon.tsv").exists() else []
JARGON_MAX = {"12": 1, "30": 2, "60": 3, "90": 4}     # distinct finance terms one reel can define and still be followed
HOOK_HOLD_S = 12.0                          # the line that answers L1's question must not start before this
WORD_RANGE = {"12": (26, 42), "30": (70, 95), "60": (140, 180), "90": (215, 260)}   # CLAUDE.md §4, written words
STALE_TSV = BRAND / "stale-bits.tsv"
# §3: no real finance/payment/jeweller brands on screen or in the voice; "<Word> app" is always suspect
BRAND_NAMES = ("paytm|phonepe|phone pe|gpay|google pay|bhim|cred|zerodha|groww|upstox|razorpay|amazon pay|mobikwik|"
               "freecharge|hdfc|icici|sbi|axis bank|kotak|paypal|flipkart|swiggy|zomato|tanishq|malabar|kalyan|joyalukkas|"
               "bajaj|lic|policybazaar|navi|slice|jupiter|fi money|angel one|nippon|sbi mf|mirae|bharatpe")
BRAND_RE = re.compile(rf"(?<![\w-])({BRAND_NAMES})(?![\w-])", re.I)
APP_RE = re.compile(r"\b([A-Z][\w]+(?: Care)? app)\b")      # "BIS Care app", "Foo app" (capitalised, as written)
APP_OK = {"UPI app", "Banking app", "Bank app", "Phone app"}
TAKEAWAY_MAX = 16                           # what the viewer can repeat to a parent, in one breath


def jargon_in(text: str) -> list[str]:
    return [t for t in JARGON if re.search(rf"(?<![\w-]){re.escape(t)}(?![\w-])", text, re.I if len(t) > 3 else 0)]


def discussable(ep) -> list[str]:
    """After one watch the viewer can discuss it with their father (2026-10-21): a jargon-free takeaway, an informed
    adult's first question answered by a line, few terms. An outcome, not a scene — the reel needs no dad in it."""
    out, m = [], ep.meta
    take = str(m.get("takeaway", "")).strip()
    if not take or take.startswith("<"):
        out.append("takeaway missing in the frontmatter — the one sentence (≤ 16 words) the viewer can explain to a parent "
                   "after watching; the payoff line must say it in the reel's words")
    else:
        if len(take.split()) > TAKEAWAY_MAX:
            out.append(f"takeaway is {len(take.split())} words (> {TAKEAWAY_MAX}) — say it in one breath")
        if len(jargon_in(take)) > 1:
            out.append(f"takeaway uses jargon ({', '.join(jargon_in(take))}) — keep at most the reel's one core term, "
                       "say the rest in plain words")
    dad = str(m.get("follow_up", "")).strip()
    ids = {l.id for l in ep.lines}
    hit = re.search(r"(?:→|->)\s*(L\d+)", dad)
    if not dad or dad.startswith("<"):
        out.append("follow_up missing in the frontmatter — an informed adult's first sceptical question + the line "
                   "that answers it: "
                   "\"Toh mera paisa gaya kahan? → L7\"")
    elif not hit or hit.group(1) not in ids:
        out.append(f"follow_up must end with → L# of a line that answers it (got: {dad[:60]})")
    loop = str(m.get("open_loop", "")).strip()
    ids_ = re.findall(r"L\d+", loop)
    if not loop or loop.startswith("<"):
        out.append("open_loop missing in the frontmatter — the question the hook plants and only the payoff answers, "
                   "\"L2 → L9\" (3–15 s is where viewers swipe; an unanswered question keeps them)")
    elif len(ids_) != 2 or not set(ids_) <= ids:
        out.append(f"open_loop must name two existing lines, plant → payoff (got: {loop[:40]})")
    else:
        first_ch, last_ch = ep.lines[0].chapter, ep.lines[-1].chapter
        by_id = {l.id: l for l in ep.lines}
        if by_id[ids_[0]].chapter != first_ch:
            out.append(f"open_loop plant {ids_[0]} must be in the first chapter (the hook), by ~5 s")
        if by_id[ids_[1]].chapter != last_ch:
            out.append(f"open_loop close {ids_[1]} must be in the last chapter — answered earlier, the loop lets them go")
    used = sorted({t for l in ep.lines for t in jargon_in(l.spoken)}, key=str.lower)
    cap = JARGON_MAX.get(ep.format, 3)
    if len(used) > cap:
        out.append(f"jargon: {len(used)} finance terms ({', '.join(used)}) — max {cap} for {ep.format} s; each one said must "
                   "be defined in plain words the first time (brand/jargon.tsv), so cut the ones the takeaway doesn't need")
    return out


def hook_hold(ep) -> list[str]:
    """The answer to L1's question must not arrive before ~12 s (3–15 s is where viewers swipe)."""
    ans = str(ep.meta.get("hook_answer", "")).strip()
    ids = [l.id for l in ep.lines]
    if not re.fullmatch(r"L\d+", ans) or ans not in ids:
        return ["hook_answer missing in the frontmatter — the line (L#) that answers L1's question; the lint checks it "
                "starts at 12 s or later"] if not ans or ans.startswith("<") else [f"hook_answer must be one existing line like L5 (got: {ans[:20]})"]
    spoken = 0
    for line in ep.lines:
        if line.id == ans:
            break
        spoken += sum(spoken_len(m) - 1 for m in NUM_TOKEN.findall(line.spoken)) + len(line.spoken.split())
    t = spoken / WPS
    if t < HOOK_HOLD_S:
        return [f"hook answered too early: {ans} starts at ≈ {t:.1f} s, outside the hold of ≥ {HOOK_HOLD_S:.0f} s — "
                "keep L1's question open longer (move the answer later or add a complication first)"]
    return []


def stale_lint(ep) -> list[str]:
    """Bits reviewers already rejected, §3 brand/app names, and claims facts.md lists as Not usable."""
    out = []
    pats = []
    if STALE_TSV.exists():
        for l in STALE_TSV.read_text().splitlines():
            if l.strip() and not l.startswith("#"):
                pat, _, why = l.partition("\t")
                pats.append((re.compile(pat, re.I), why.strip() or "stale bit"))
    nu = []
    fp = Path(ep.dir) / "facts.md"
    if fp.exists():
        m = re.search(r"^##\s*Not usable[^\n]*\n(.*?)(?=^##\s|\Z)", fp.read_text(), re.M | re.S)
        for b in re.findall(r"^\s*[-*]\s+(.+)$", m.group(1), re.M) if m else []:
            # distinctive words: ≥ 6 letters, outside the parenthetical reason; need 3 of them to call it a restatement
            core = re.sub(r"\(.*?\)", "", b)
            kw = {w.lower() for w in re.findall(r"[A-Za-z]{6,}", core)} - {"average", "indian", "household", "source", "primary"}
            if len(kw) >= 3:
                nu.append((kw, b.strip()[:60]))
    for line in ep.lines:
        for rx, why in pats:
            if rx.search(line.spoken):
                out.append(f"{line.id} stale bit /{rx.pattern}/ — {why}: \"{line.spoken[:70]}\"")
        for m in BRAND_RE.finditer(line.spoken):
            out.append(f"{line.id} names a real brand '{m.group(0)}' (CLAUDE.md §3) — say it generically: \"{line.spoken[:70]}\"")
        for m in APP_RE.finditer(line.spoken):
            if m.group(1) not in APP_OK and not BRAND_RE.search(m.group(1)):
                out.append(f"{line.id} names an app '{m.group(1)}' (CLAUDE.md §3: no app/brand names) — say it generically")
        low = {w.lower() for w in re.findall(r"[A-Za-z]{6,}", line.spoken)}
        for kw, b in nu:
            if len(kw & low) >= max(3, (len(kw) + 1) // 2 + (len(kw) % 2 == 0)):
                out.append(f"{line.id} restates a facts.md 'Not usable' claim ({b}…) — cut or reframe it")
    return out


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
    wlo, whi = WORD_RANGE[fmt]
    if not wlo <= words <= whi:
        out.append(f"written words: {words} outside {wlo}–{whi} for {fmt} s ({'cut' if words > whi else 'add'} "
                   f"{words - whi if words > whi else wlo - words}) — counted as the reviewer does: spoken words of script lines, "
                   "no [F#]/[JOKE]/{directions}")
    out += hook_hold(ep)
    out += discussable(ep)
    out.insert(0, f"script: {words} words written · ≈ {spoken} spoken (numbers in full) · ≈ {secs:.0f} s incl. outro · {jokes} jokes")
    return out


def _digits(t: str) -> str:
    return re.sub(r"(?<=\d)[,\s](?=\d)", "", t)


_SRC_TEXT: dict[str, str] = {}


def _source_text(name: str) -> str:
    if name not in _SRC_TEXT:
        import source_index
        try:
            _SRC_TEXT[name] = _digits(" ".join(t for _, t in source_index.extract_pages(source_index.SOURCE_DIR / name)))
        except Exception:
            _SRC_TEXT[name] = ""
    return _SRC_TEXT[name]


def verify_plan(ep) -> list[dict]:
    """Which facts the fact-checker must re-verify at the source, and which it only holds the script to.
    The researcher marks a row it checked against a cached primary source `VERIFIED <cached file> <page/§>`;
    a row is trusted when that file is cached and every number in the claim is in its text (or it's a fresh
    library entry). Everything else — unmarked rows, numbers the text doesn't show, stale entries — is `check`."""
    import facts_library
    lib = facts_library.entries()
    cached = {e.get("file") for e in json.loads((BRAND / "sources" / "index.json").read_text()).values()} \
        if (BRAND / "sources" / "index.json").exists() else set()
    out = []
    for fid, f in ep.facts.items():
        notes, src = f.get("notes", ""), f.get("source_text", "")
        m = re.search(r"library:(L-[A-Z0-9-]+)", notes)
        if not f["source"]:
            st, why = ("check", "re-do the arithmetic") if COMPUTED.search(src) else ("trusted", "hypothetical example")
        elif m and m.group(1) in lib and not facts_library.why_stale(lib[m.group(1)]):
            st, why = "trusted", f"fresh library entry {m.group(1)}"
        elif "VERIFIED" not in notes:
            st, why = "check", "not marked VERIFIED by the researcher"
        else:
            files = [c for c in cached if c and c in notes]
            if not files:
                st, why = "check", "VERIFIED but names no cached file in brand/sources"
            else:
                text = " ".join(_source_text(c) for c in files)
                nums = {_digits(n).strip("₹%") for n in NUM_TOKEN.findall(f["claim"])}
                missing = sorted(n for n in nums if n and n not in text)
                st, why = ("check", f"numbers not in {files[0]}: {', '.join(missing)}") if missing else \
                    ("trusted", f"VERIFIED in {files[0]}")
        out.append({"fact": fid, "status": st, "why": why})
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
        # a Culture now row that peaked over a month ago is an evergreen classic: fine, but ≤ 2 per reel (CLAUDE.md §3)
        peaks, old = memes.culture_peaks(ep), {}
        for line in ep.lines:
            for mid in MEME_CUE.findall(" ".join(line.directions) + " " + line.raw):
                t = rows.get(mid.upper())
                age = peaks.get(memes.norm_title(t)) if t else None
                if age is not None and age > memes.FRESH_PEAK_MONTHS:
                    old.setdefault(mid.upper(), (line.id, t, age))
        if len(old) > memes.CLASSICS_PER_REEL:
            warnings.append(f"{len(old)} planned memes peaked over a month ago ({', '.join(old)}) — classic meme budget "
                            f"is ≤ {memes.CLASSICS_PER_REEL} per reel; swap the rest for rows that peaked this month")
    except Exception as ex:          # memes/network trouble never blocks the fact gate
        warnings.append(f"recent-meme check skipped ({ex})")
    unused = set(ep.facts) - {f for l in ep.lines for f in l.facts}
    for fid in sorted(unused):
        warnings.append(f"{fid} is never cited in script.md")
    jokes = [l.id for l in ep.lines if l.joke]
    script = script_lint(ep) if ep.lines else []
    if ep.lines:
        problems += stale_lint(ep)            # writer-fixable, and /produce's gate sends non-F# problems back
    try:
        plan = verify_plan(ep)
    except Exception as ex:          # never blocks the gate: without a plan the fact-checker verifies everything
        plan, _ = [], warnings.append(f"verify plan skipped ({ex})")
    return {"episode": ep.name, "ok": not problems, "problems": problems, "warnings": warnings, "script": script,
            "joke_lines": jokes, "facts": len(ep.facts), "lines": len(ep.lines), "verify": plan}


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
        chk = [v for v in r["verify"] if v["status"] == "check"]
        if r["verify"]:
            print(f"  · verify at source: {', '.join(v['fact'] + ' (' + v['why'] + ')' for v in chk) or 'none'}"
                  f" · trusted: {', '.join(v['fact'] for v in r['verify'] if v['status'] == 'trusted') or 'none'}")
        if r["joke_lines"]:
            print(f"  · joke lines to punch up: {', '.join(r['joke_lines'])}")
        print("  ✓ clean" if r["ok"] else "  RENDER BLOCKED until fixed (or --allow-unsourced)")
    return 0 if r["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
