#!/usr/bin/env python3
"""Mechanical QA of a built reel — catches what code can see, so the video-reviewer only judges
taste, comedy and retention.

  qa.py episodes/<ep> [--at 3.4,8.2] [--audio] [--strict]
  -> .cache/qa.json + a short summary; exit 1 on errors (warnings never block)

Reads the built composition (build/index.html) in headless Chrome — no render needed — and seeks
the master timeline to every cut, transition, overlay, odometer landing and the last frame.
Checks:
  empty-cut       a scene has nothing on screen on/after its cut frame (dropped-frame look)
  safe-zone       visible text outside x 60–940 / y 220–1500 (IG UI zones), captions outside their band
  overlap         two pieces of text on top of each other (incl. captions under content)
  caption-band    content text inside the caption band y 1150–1450
  wordmark        something opaque covering the @handle wordmark before the outro
  odometer        an odometer's landed (or count-mode start) value isn't the number in params
  early-number    a number on screen (caption or scene) before the voice says it
  tiny-text       text rendered under 26 px (unreadable on a phone)
  fade-entrance   a scene's content is still semi-transparent 3 frames after its cut
  low-contrast    text that sits on the field (no paper/marker under it) in a colour too close to the
                  field — e.g. ink on a dark field before its marker swipe has drawn (frame 1 = error)
  covered-text    an overlay's paper/stamp/mascot lands on another clip's text (stamp over a sub-line)
  small-object    the paper objects carrying text span < 75 % of the content width (brand: ≈ 860–880 px)
  narrow-frame    a shot's content covers < 65 % of the content width and < 30 % of its height
  small-text      a shot shows text under 36 px (one warning per shot)
  empty-paper     a paper object whose text ends above 70 % of its height when settled (half-empty receipt)
  late-content    settled, a shot shows < 40 % of what it ends on (header alone while the rows print late)
  same-layout     4 shots in a row with the same content box (template feel)
  short-shot      a shot shorter than its component's minDuration (or < 0.8 s)
  hidden-text     text with a painted object on top of it — the mascot's SVG, a tray over its own letter
                  (anything hit-testing finds above the glyphs; pen scribbles and marker swipes are exempt)
  clipped-text    text cut off by its container (overflow) when settled — a letter line half under the tray
  broken-word     a word split across two lines ("Camouflag / ed.")
  late-number     a number the voice says while its shot will show it but doesn't yet (the bar arrives late)
  late-text       a shot whose paper is up but nearly empty of text when settled (a chat card with only dots,
                  a receipt with only its header) — counted in characters, not area
  audio           output/final.mp4 true peak > −1 dBTP, LUFS off −14 (reported only if final.mp4 is
                  older than scenes.json; make_reel re-runs it after mix)
Every issue carries t, the scene/component, a route ([director] / [editor] / [component:x]) and a fix.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_composition import build, component_meta  # noqa: E402
from lib.common import BRAND, ROOT  # noqa: E402
from lib.episode import load  # noqa: E402

TOK = json.loads((BRAND / "tokens.json").read_text())
SAFE = TOK["safeZone"]
WM = TOK["wordmark"]["box"]
F = 1 / 30
TOL = 4            # px of overflow tolerated (anti-aliasing, seeded tilt)
MIN_FONT = 26      # px at 1080 wide
SMALL_FONT = 36    # below this a shot's text is "hard to read" (warn, per shot)
NARROW_W, NARROW_H = 0.65, 0.30   # content box under 65 % of the width AND 30 % of the height = dead field
SAME_RUN, SAME_TOL = 4, 70        # 4 shots in a row with content boxes within 70 px = same composition
NO_PROBE = {"bg", "wordmark"}
CONTRAST_ERR, CONTRAST_WARN = 2.0, 3.0   # text vs what is behind it (WCAG ratio; big headline type)
SMALL_OBJ = 0.75                          # paper objects with text spanning < 75 % of the content width (≈ 660 px)
EMPTY_PAPER, EMPTY_PAPER_MIN_H = 0.7, 300  # a ≥ 300 px paper whose text ends above 70 % of its height = half-empty
LATE_SHARE, LATE_MIN_SHOT = 0.4, 1.5       # settled frame shows < 40 % of the shot's final content (shots ≥ 1.5 s)
COVER_OK = {"marker-highlight", "transition", "captions"}   # overlays meant to sit on text
HIDDEN_ERR, HIDDEN_WARN = 0.5, 0.3   # share of a text's probe points under a painted object
OWN_COVER_OK = {"glyph-character"}   # its eyes and limbs are drawn on its own glyph by design
CLIPPED_ERR, CLIPPED_WARN = 0.4, 0.2  # share of a text's ink clipped by an overflow ancestor
LATE_NUM_ERR = 0.8                    # s after the voice says a number that its shot still hides it
LATE_TEXT_ERR, LATE_TEXT_WARN, LATE_TEXT_MIN = 0.15, 0.35, 20   # settled chars / final chars (finals ≥ 20 chars)
UNITS = {"l": 1e5, "lakh": 1e5, "lac": 1e5, "लाख": 1e5, "k": 1e3, "hazaar": 1e3, "hazar": 1e3, "हज़ार": 1e3,
         "हजार": 1e3, "cr": 1e7, "crore": 1e7, "करोड़": 1e7}


def inr(n: float, decimals: int | None = None) -> str:
    """Indian digit grouping, like CH.inr / toLocaleString('en-IN')."""
    d = decimals if decimals is not None else (2 if abs(n) % 1 else 0)
    s = f"{abs(n):.{d}f}"
    whole, _, frac = s.partition(".")
    head, tail = whole[:-3], whole[-3:]
    while len(head) > 2:
        tail = head[-2:] + "," + tail
        head = head[:-2]
    out = (head + "," + tail) if head else tail
    return ("-" if n < 0 else "") + out + ("." + frac if frac else "")


def digits(s: str) -> str:
    return re.sub(r"\D", "", s)


def chrome_path() -> str:
    r = subprocess.run(["npx", "--no-install", "hyperframes", "browser", "path"], cwd=ROOT, capture_output=True, text=True)
    path = (r.stdout.strip().splitlines() or [""])[-1].strip()
    if not path or not Path(path).exists():
        raise SystemExit("qa: no Chrome found — run `npx hyperframes browser ensure`")
    return path


def probe(html: Path, times: list[float]) -> dict:
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump({"html": str(html), "chrome": chrome_path(), "times": times, "compId": "reel"}, f)
    r = subprocess.run(["node", str(ROOT / "pipeline" / "lib" / "qa_probe.mjs"), f.name], cwd=ROOT,
                       capture_output=True, text=True, timeout=600)
    Path(f.name).unlink(missing_ok=True)
    if r.returncode != 0:
        raise SystemExit(f"qa probe failed:\n{r.stderr[-2000:]}")
    return json.loads(r.stdout)


def sample_times(spec: dict) -> dict[float, str]:
    """time -> why it is sampled (cuts, transitions, overlay midpoints, odometer landings, ends)."""
    ts: dict[float, str] = {}
    add = lambda t, why: ts.setdefault(round(min(max(t, 0.0), spec["duration"] - 0.02), 3), why)  # noqa: E731
    add(0.02, "frame 1")
    for s in spec["scenes"]:
        if s["id"] in NO_PROBE:
            continue
        st, d = s["start"], s["duration"]
        if s["track"] == 1:
            add(st + F, f"{s['id']} cut+1f")
            add(st + 3 * F, f"{s['id']} cut+3f")
            add(st + min(d * 0.5, 1.2), f"{s['id']} settled")
            add(st + d - F, f"{s['id']} last frame")
            if s["id"] == "outro":
                add(st + 0.6, "outro settled")
        elif s["track"] == 2:
            add(st + min(0.25, d / 2), f"{s['id']} in")
            add(st + d / 2, f"{s['id']} mid")
        elif s["track"] == 3:
            cut = s["params"].get("cut", st)
            for k in (-0.1, 0.0, 0.1):
                add(cut + k, f"{s['id']} cut{k:+.1f}")
        if s["component"] == "odometer-number":
            p = s["params"]
            if p.get("from") is not None:
                add(st + float(p.get("rollStart", 0.15)) - F, f"{s['id']} start value")
            add(st + float(p.get("rollStart", 0.15)) + float(p.get("rollDuration", 0.9)) + 0.25, f"{s['id']} landed")
    add(spec["duration"] - 0.05, "last frame")
    return dict(sorted(ts.items()))


def inside(b, x0, y0, x1, y1, tol=TOL) -> bool:
    return b[0] >= x0 - tol and b[1] >= y0 - tol and b[2] <= x1 + tol and b[3] <= y1 + tol


def overlap(a, b) -> float:
    w = min(a[2], b[2]) - max(a[0], b[0])
    h = min(a[3], b[3]) - max(a[1], b[1])
    return max(w, 0) * max(h, 0)


def glyph_lines(x: dict) -> list:
    """A text range's line box spans the font's whole ascent+descent (≈1.6 em for Mukta), far taller
    than the 1.0 leading the brand uses, so stacked lines 'overlap' on paper. Keep each line's ink
    band: ~0.8 em around its centre. (Tilted text gets axis-aligned boxes; the band absorbs that too.)"""
    f = max(x["font"], 1)
    out = []
    for b in x.get("lines") or [x["box"]]:
        cy, h = (b[1] + b[3]) / 2, min(b[3] - b[1], f * 0.8)
        out.append([b[0], cy - h / 2, b[2], cy + h / 2])
    return out


def values(text: str) -> set[float]:
    """Numbers a viewer reads in a string, as values: ₹15,00,000 / 15L / ₹15 lakh → 1500000; 30% → 30."""
    out = set()
    for m in re.finditer(r"(\d[\d,]*(?:\.\d+)?)\s*(lakh|lac|crore|cr|hazaa?r|लाख|करोड़|हज़ार|हजार|[lLkK](?![a-zA-Z]))?", text):
        try:
            v = float(m.group(1).replace(",", ""))
        except ValueError:
            continue
        u = (m.group(2) or "").lower()
        out.add(round(v * UNITS.get(u, 1), 2))
    return out


def spoken_numbers(words: list[dict]) -> list[tuple[float, float, str]]:
    """(value, start, as said) for every number in the voice; a unit word right after scales it (₹1 + लाख)."""
    out = []
    for i, w in enumerate(words):
        vs = values(w["text"])
        if not vs:
            continue
        nxt = words[i + 1]["text"].strip(".,!?;:").lower() if i + 1 < len(words) else ""
        mult = UNITS.get(nxt, 1) if nxt in UNITS and len(nxt) > 1 else 1
        for v in vs:
            out.append((round(v * mult, 2), w["start"], w["text"] + (f" {words[i + 1]['text']}" if mult > 1 else "")))
    return out


def area(b) -> float:
    return max(b[2] - b[0], 0) * max(b[3] - b[1], 0)


def rgb(c: str | None):
    """'rgb(a, b, c)' / 'rgba(…)' (0–255) or 'color(srgb r g b / a)' (0–1, what color-mix computes to)."""
    c = c or ""
    m = re.findall(r"[\d.]+", c)
    if len(m) < 3 or (len(m) >= 4 and float(m[3]) < 0.5):
        return None
    k = 255 if c.startswith("color(") else 1
    return tuple(float(v) * k for v in m[:3])


def contrast(a, b) -> float:
    def lum(c):
        ch = [v / 255 for v in c]
        ch = [v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4 for v in ch]
        return 0.2126 * ch[0] + 0.7152 * ch[1] + 0.0722 * ch[2]
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def centre_in(b, box) -> bool:
    cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
    return box[0] <= cx <= box[2] and box[1] <= cy <= box[3]


def audio_check(ep, issues: list) -> dict:
    final = ep.output / "final.mp4"
    if not final.exists():
        return {"checked": False, "why": "no output/final.mp4 yet"}
    scenes = ep.dir / "scenes" / "scenes.json"
    stale = scenes.exists() and final.stat().st_mtime < scenes.stat().st_mtime
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(final), "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True)
    i = re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)
    p = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r.stderr)
    lufs, tp = (float(i[-1]) if i else None), (float(p[-1]) if p else None)
    if stale:   # final.mp4 predates the current scenes.json — report, don't block on an old mix
        return {"checked": True, "stale": True, "lufs": lufs, "true_peak_dbtp": tp}
    if tp is not None and tp > -1.0:
        issues.append({"sev": "error", "kind": "audio", "t": None, "where": "mix", "route": "editor",
                       "msg": f"true peak {tp:.1f} dBTP on final.mp4 (max −1.0)", "fix": "limit at −1.5 dBTP before the AAC encode"})
    if lufs is not None and abs(lufs + 14) > 1.0:
        issues.append({"sev": "warn", "kind": "audio", "t": None, "where": "mix", "route": "editor",
                       "msg": f"integrated loudness {lufs:.1f} LUFS (target −14)", "fix": "re-run mix"})
    return {"checked": True, "stale": False, "lufs": lufs, "true_peak_dbtp": tp}


def qa(ep_dir: str, extra: list[float] | None = None, audio: bool = True) -> dict:
    ep = load(ep_dir)
    res_p = ep.cache / "scenes.resolved.json"
    if not res_p.exists():
        raise SystemExit("qa: no .cache/scenes.resolved.json — run the validate stage first")
    spec = json.loads(res_p.read_text())
    idx = ep.dir / "build" / "index.html"
    if not idx.exists() or idx.stat().st_mtime < res_p.stat().st_mtime:
        idx = build(spec, ep.dir / "build", "reel")
    words = json.loads((ep.cache / "words.json").read_text())
    scenes = {s["id"]: s for s in spec["scenes"]}
    outro_t = spec["outro_start"]
    trans = [(s["start"], s["start"] + s["duration"]) for s in spec["scenes"] if s["track"] == 3]
    in_transition = lambda t: any(a - 0.01 <= t <= b + 0.01 for a, b in trans)  # noqa: E731

    times = sample_times(spec)
    said = spoken_numbers(words)
    for v, st, _ in said:
        times.setdefault(round(min(st + LATE_NUM_ERR, spec["duration"] - 0.05), 3), f"said {v:g}")
    for t in extra or []:
        times.setdefault(round(t, 3), "requested")
    data = probe(idx, list(times))
    issues: list[dict] = []
    seen: set = set()

    def add(sev, kind, t, where, route, msg, fix, key=None):
        k = key or (kind, where, msg)
        if k in seen:
            return
        seen.add(k)
        issues.append({"sev": sev, "kind": kind, "t": None if t is None else round(t, 2), "where": where,
                       "route": route, "msg": msg, "fix": fix})

    for e in data["errors"]:
        add("error", "js", None, "composition", "component", f"page error: {e[:200]}", "fix the component that throws")

    # first spoken time of every number (digits ≥ 2) — for early-number
    spoken_at: dict[str, float] = {}
    for w in words:
        d = digits(w["text"])
        if len(d) >= 2:
            spoken_at.setdefault(d, w["start"])

    for smp in data["samples"]:
        t = smp["t"]
        why = times.get(t, "")
        punched = smp["stage"] not in ("none", "matrix(1, 0, 0, 1, 0, 0)")
        settled = not why.endswith(("cut+1f", "cut+3f", " in")) and not re.search(r"cut[+-]\d", why)
        moving = in_transition(t) or punched or not settled
        texts = []
        for c in smp["clips"]:
            comp = c["comp"] or ("captions" if c["id"].startswith("cap") else "")
            for x in c["texts"]:
                texts.append({**x, "clip": c["id"], "comp": comp, "track": c["track"]})
            sc = scenes.get(c["id"])
            if c["track"] == 1 and sc and c["id"] != "outro":
                since = t - sc["start"]
                vis = [p for p in c["painted"] if p["op"] >= 0.15] + [x for x in c["texts"] if x["op"] >= 0.15]
                if since <= 4 * F and not vis and not in_transition(t):
                    sev = "error" if since > 2 * F else "warn"
                    add(sev, "empty-cut", t, f"{c['id']} ({c['comp']})", "editor|component:" + c["comp"],
                        f"nothing on screen {since * 30:.0f} frame(s) after the cut — reads as a dropped frame",
                        "have the object present on the cut frame (pop from ~92%, no opacity-0 start) or move the cut",
                        key=("empty-cut", c["id"]))
                if 2 * F < since <= 4 * F and vis and not in_transition(t):
                    best = max(v["op"] for v in vis)
                    if best < 0.7:
                        add("warn", "fade-entrance", t, f"{c['id']} ({c['comp']})", "component:" + c["comp"],
                            f"content at {best:.0%} opacity 3 frames after the cut — a fade, not the brand pop",
                            "snap opacity on frame 1 and let the scale pop do the motion", key=("fade", c["id"]))
            # wordmark covered (before the outro, by an opaque painted object of another clip)
            if t < outro_t - 0.05 and c["id"] not in ("bg", "wordmark") and not c["id"].startswith("cap"):
                wm = (WM["x"], WM["y"], WM["x"] + WM["w"], WM["y"] + WM["h"])
                for p in c["painted"] + c["texts"]:
                    if p["op"] >= 0.6 and overlap(p["box"], wm) > 0.15 * area(wm) and not moving:
                        add("warn", "wordmark", t, f"{c['id']} ({c['comp']})", "director",
                            "covers the @chillar.ind wordmark", "move it above y 1450", key=("wm", c["id"]))
                        break

        for x in texts:
            if x["op"] < 0.5:
                continue
            b, where = x["box"], f"{x['clip']} ({x['comp']}) “{x['text'][:30]}”"
            is_cap = x["comp"] == "captions"
            if x["clip"] == "wordmark":
                continue
            if is_cap:
                cb = SAFE["captionBand"]
                if not moving and not inside(b, SAFE["left"], cb[0] - 20, 1080 - SAFE["right"], cb[1] + 20, tol=8):
                    add("error", "safe-zone", t, where, "component:captions", f"caption box {b} leaves the caption band",
                        "shorter caption chunks", key=("capband", x["clip"]))
            elif not moving and not inside(b, SAFE["left"], SAFE["top"], 1080 - SAFE["right"], 1920 - SAFE["bottom"]):
                add("error", "safe-zone", t, where, f"component:{x['comp']}|director",
                    f"text box {b} crosses the safe zone (x 60–940, y 220–1500)",
                    "shrink/auto-fit or move it inside the content zone", key=("safe", x["clip"], x["text"][:20]))
            if not is_cap and not moving and x["clip"] != "outro":
                cb = SAFE["captionBand"]
                if b[3] > cb[0] + 30 and b[1] < cb[1]:
                    add("warn", "caption-band", t, where, "director", f"content text inside the caption band ({b})",
                        "keep content above y 1150", key=("band", x["clip"], x["text"][:20]))
            if x["font"] < MIN_FONT and x["clip"] != "outro" or (x["clip"] == "outro" and x["font"] < 24):
                add("warn", "tiny-text", t, where, f"component:{x['comp']}",
                    f"text renders at ~{x['font']}px — unreadable on a phone", "≥ 28 px", key=("tiny", x["clip"], x["text"][:20]))
            for wd in x.get("broken") or []:
                if not moving and not is_cap:
                    add("error", "broken-word", t, where, f"component:{x['comp']}",
                        f"“{wd}” breaks across two lines", "shrink to fit (auto-fit) or rephrase so the word stays whole",
                        key=("broken", x["clip"], wd))
            if not moving and not x["odo"] and x["clip"] != "outro":
                comps = {c["id"]: c["comp"] for c in smp["clips"]}
                for cv in x.get("cover") or []:
                    cid, _, under = cv["clip"].partition("|")
                    other = comps.get(cid, "")
                    own = cid == x["clip"]
                    if other in COVER_OK or cid in ("wordmark", "bg") or cv["frac"] < HIDDEN_WARN \
                            or (own and x["comp"] in OWN_COVER_OK):
                        continue
                    sev = "warn" if under or cv["frac"] < HIDDEN_ERR else "error"
                    add(sev, "hidden-text", t, f"{where} {'over' if under else 'under'} {cid} ({other})",
                        f"component:{x['comp']}|director" if own else "director",
                        (f"Chillar sits under {cv['frac']:.0%} of the words — the text reads over a drawing" if under else
                         f"{cv['frac']:.0%} of the text is under a painted object" + (" of its own shot" if own else "")),
                        "move/shrink the object (mascot x/y, tray size) or the text so nothing sits on the words",
                        key=("hidden", x["clip"], x["text"][:16], cid))
                if (x.get("cut") or 0) >= CLIPPED_WARN and settled:
                    add("error" if x["cut"] >= CLIPPED_ERR else "warn", "clipped-text", t, where,
                        f"component:{x['comp']}|director", f"{x['cut']:.0%} of the text is cut off by its container",
                        "make the container taller/wider or shorten the text", key=("clipped", x["clip"], x["text"][:16]))
            # numbers on screen before they are said (frame 1 and the outro are exempt: stakes / sign-off)
            sc = scenes.get(x["clip"])
            first = spec["scenes"][1]["id"] if len(spec["scenes"]) > 1 else ""
            if x["clip"] not in (first, "outro") and (is_cap or sc):
                for num in re.findall(r"₹?\d[\d,.]*%?", x["text"]):
                    d = digits(num)
                    if len(d) < 2 or d not in spoken_at:
                        continue
                    lead = spoken_at[d] - t
                    limit = 0.15 if is_cap else 0.6
                    if lead > limit and not (sc and sc["start"] < 0.05):
                        add("error" if is_cap else "warn", "early-number", t, where, "editor",
                            f"“{num}” is on screen {lead:.1f}s before the voice says it",
                            "reveal it on its word (caption chunk / scene 'at' / param timing)", key=("early", x["clip"], d))

        # text over text
        live = [x for x in texts if x["op"] >= 0.5 and x["clip"] != "wordmark"]
        for i, a in enumerate(live):
            for b in live[i + 1:]:
                if a["clip"] == b["clip"] and (a["i"] in b["anc"] or b["i"] in a["anc"]):
                    continue
                if a["comp"] == b["comp"] == "captions" or moving:
                    continue
                hit = False
                for la in glyph_lines(a):
                    for lb in glyph_lines(b):
                        ov = overlap(la, lb)
                        if ov > 300 and ov > 0.18 * min(area(la), area(lb)):
                            hit = True
                if hit:
                    route = "director" if a["clip"] != b["clip"] else f"component:{a['comp']}"
                    add("error", "overlap", t, f"{a['clip']} “{a['text'][:24]}” × {b['clip']} “{b['text'][:24]}”", route,
                        "text over text", "move one of them / end the overlay at the cut",
                        key=("ov", a["clip"], a["text"][:16], b["clip"], b["text"][:16]))

        # low contrast: text on the bare field (no own background, no paper under its centre)
        field = rgb(smp.get("field"))
        papers = [(c["id"], p["box"]) for c in smp["clips"] for p in c["painted"]
                  if p["op"] >= 0.5 and "marker" not in p["cls"] and c["id"] not in ("bg", "wordmark")]
        for x in texts:
            if x["op"] < 0.6 or x["clip"] == "wordmark" or (moving and why != "frame 1"):
                continue
            fg = rgb(x.get("color"))
            under = rgb(x.get("bg"))
            if under is None:
                if any(centre_in(x["box"], pb) for _, pb in papers):
                    continue          # on paper / an object: its own colours are the component's job
                under = field
            if fg is None or under is None:
                continue
            cr = contrast(fg, under)
            if cr < CONTRAST_WARN:
                sev = "error" if cr < CONTRAST_ERR or why == "frame 1" else "warn"
                add(sev, "low-contrast", t, f"{x['clip']} ({x['comp']}) “{x['text'][:30]}”", f"component:{x['comp']}|director",
                    f"text contrast {cr:.1f}:1 against what is behind it" + (" on FRAME 1" if why == "frame 1" else ""),
                    "give it its background (marker drawn at t=0 on frame 1) or the field's ink colour",
                    key=("contrast", x["clip"], x["text"][:16]))

        # an overlay's opaque object on top of another clip's text
        if not moving:
            for c in smp["clips"]:
                if c["track"] != 2 or c["comp"] in COVER_OK:
                    continue
                for p in c["painted"]:
                    if p["op"] < 0.6 or p["kind"] == "svg":
                        continue
                    for x in texts:
                        if x["clip"] == c["id"] or x["op"] < 0.5 or x["clip"] == "wordmark":
                            continue
                        if any(overlap(p["box"], la) > 0.25 * area(la) for la in glyph_lines(x)):
                            add("error", "covered-text", t, f"{c['id']} ({c['comp']}) × {x['clip']} “{x['text'][:24]}”", "director",
                                "an overlay object covers text underneath it", "move the overlay into empty field or end it before the text",
                                key=("cover", c["id"], x["clip"], x["text"][:16]))
                            break

        # odometer values
        for c in smp["clips"]:
            sc = scenes.get(c["id"])
            if not sc or sc["component"] != "odometer-number":
                continue
            p = sc["params"]
            reading = "".join(x["text"] for x in sorted((x for x in c["texts"] if x["odo"]), key=lambda x: x["box"][0]))
            want = None
            if why.endswith("landed"):
                want = p.get("value")
            elif why.endswith("start value"):
                want = p.get("from")
            if want is None:
                continue
            exp = f"{p.get('prefix', '')}{inr(float(want), p.get('decimals'))}{p.get('suffix', '')}"
            if digits(reading) != digits(exp):
                add("error", "odometer", t, f"{c['id']} (odometer-number)", "component:odometer-number",
                    f"shows “{reading or '(nothing)'}” but should show “{exp}” ({why})",
                    "check the roll/count; the start and landed frames must be fully legible", key=("odo", c["id"], why))

    # ---- layout taste that code can measure (the reviewer flagged these by eye every round) ----
    # content box of each main shot at its first settled sample: union of painted objects + text
    shots: dict[str, dict] = {}
    for smp in data["samples"]:
        t = smp["t"]
        why = times.get(t, "")
        if in_transition(t) or smp["stage"] not in ("none", "matrix(1, 0, 0, 1, 0, 0)") or re.search(r"cut[+-]\d|cut\+\d|\bin$", why):
            continue
        for c in smp["clips"]:
            sc = scenes.get(c["id"])
            if c["track"] != 1 or not sc or c["id"] == "outro" or c["id"] in shots:
                continue
            boxes = [p["box"] for p in c["painted"] if p["op"] >= 0.5] + [x["box"] for x in c["texts"] if x["op"] >= 0.5]
            if not boxes:
                continue
            u = [min(b[0] for b in boxes), min(b[1] for b in boxes), max(b[2] for b in boxes), max(b[3] for b in boxes)]
            small = sorted({round(x["font"]) for x in c["texts"] if x["op"] >= 0.5 and x["font"] < SMALL_FONT})
            txt = [x["box"] for x in c["texts"] if x["op"] >= 0.5]
            pb = [p["box"] for p in c["painted"] if p["op"] >= 0.5 and p["kind"] != "svg" and "marker" not in p["cls"]
                  and not (c["comp"] == "glyph-character" and "gc-bubble" in p["cls"])
                  and any(centre_in(b, p["box"]) for b in txt)]
            paper_w = (max(b[2] for b in pb) - min(b[0] for b in pb)) if pb else 0   # span: side-by-side papers count together
            shots[c["id"]] = {"t": t, "start": sc["start"], "box": u, "comp": c["comp"], "small": small, "paper_w": paper_w,
                            "clip": c}
    # empty paper: judged at the settled sample (what the viewer sees for most of the shot — a receipt sized
    # for all its rows while one row has printed reads as half-empty paper)
    for sid, s_ in shots.items():
        c = s_["clip"]
        txt = [x["box"] for x in c["texts"] if x["op"] >= 0.5]
        for p in c["painted"]:
            pb = p["box"]
            ph = pb[3] - pb[1]
            if p["op"] < 0.5 or p["kind"] == "svg" or "marker" in p["cls"] or ph < EMPTY_PAPER_MIN_H:
                continue
            inner = [b for b in txt if centre_in(b, pb)]
            if not inner:
                continue
            used = (max(b[3] for b in inner) - pb[1]) / ph
            if used < EMPTY_PAPER:
                add("warn", "empty-paper", s_["t"], f"{sid} ({c['comp']})", f"director|component:{c['comp']}",
                    f"its paper is {ph:.0f}px tall but the text ends at {used:.0%} of it — half-empty paper",
                    "size the paper to what has printed (grow it per row), or fewer/bigger rows", key=("emptypaper", sid))
                break
    # late content: what the viewer sees settled vs. what the shot ends on — a receipt header alone for 2 s while
    # its rows print late reads as an empty frame (the reviewer had to catch it by eye)
    last_area: dict[str, tuple[float, float]] = {}
    for smp in data["samples"]:
        if in_transition(smp["t"]) or smp["stage"] not in ("none", "matrix(1, 0, 0, 1, 0, 0)"):
            continue
        for c in smp["clips"]:
            if c["track"] != 1 or c["id"] not in shots:
                continue
            bx = [p["box"] for p in c["painted"] if p["op"] >= 0.5] + [x["box"] for x in c["texts"] if x["op"] >= 0.5]
            if bx and smp["t"] >= last_area.get(c["id"], (-1, 0))[0]:
                u = [min(b[0] for b in bx), min(b[1] for b in bx), max(b[2] for b in bx), max(b[3] for b in bx)]
                last_area[c["id"]] = (smp["t"], area(u))
    for sid, s_ in shots.items():
        sc = scenes[sid]
        end_t, end_a = last_area.get(sid, (0, 0))
        if sc["duration"] >= LATE_MIN_SHOT and end_a > 0 and end_t > s_["t"] and area(s_["box"]) < LATE_SHARE * end_a:
            add("warn", "late-content", s_["t"], f"{sid} ({s_['comp']})", f"director|component:{s_['comp']}",
                f"{s_['t'] - sc['start']:.1f}s after its cut it shows {area(s_['box']) / end_a:.0%} of what it ends on "
                "— the frame reads empty while the rest arrives",
                "show the first rows/parts on the cut (smaller step, earlier start), or cut in later", key=("late", sid))
    # late number: the voice says it, the live shot shows it at some point — but not yet LATE_NUM_ERR s later
    # (the reviewer's "₹1 lakh is said while the Bonus bar is still missing")
    shown: dict[str, list[tuple[float, set[float]]]] = {}
    for smp in data["samples"]:
        for c in smp["clips"]:
            sc = scenes.get(c["id"])
            if not sc or c["track"] not in (1, 2) or c["id"] == "outro":
                continue
            vis = set()
            for x in c["texts"]:
                if x["op"] >= 0.5:
                    vis |= values(x["text"])
            shown.setdefault(c["id"], []).append((smp["t"], vis))
    for v, st, as_said in said:
        if v < 10:          # "2 minute", "1 card": too common to mean a figure on screen
            continue
        t_chk = round(min(st + LATE_NUM_ERR, spec["duration"] - 0.05), 3)
        for cid, seen_at in shown.items():
            sc = scenes[cid]
            if not (sc["start"] <= st < sc["start"] + sc["duration"]):
                continue
            later = [t for t, vis in seen_at if v in vis and t > t_chk]
            now = [t for t, vis in seen_at if v in vis and t <= t_chk]
            if later and not now:
                add("error", "late-number", st, f"{cid} ({sc['component']})", f"director|component:{sc['component']}",
                    f"the voice says “{as_said}” at {st:.1f}s but the shot shows it only at {min(later):.1f}s",
                    "reveal that row/bar/number on its word (smaller stagger, earlier start)", key=("latenum", cid, v))
    # late text: a paper up with (almost) none of its words — chat card with typing dots, a receipt header alone
    chars_at: dict[str, list[tuple[float, int]]] = {}
    for smp in data["samples"]:
        if in_transition(smp["t"]):
            continue
        for c in smp["clips"]:
            if c["track"] == 1 and c["id"] in scenes:
                chars_at.setdefault(c["id"], []).append(
                    (smp["t"], sum(len(x["text"]) for x in c["texts"] if x["op"] >= 0.5)))
    for cid, seq_ in chars_at.items():
        sc = scenes[cid]
        if sc["duration"] < LATE_MIN_SHOT:
            continue
        final = max(n for _, n in seq_)
        t_set = sc["start"] + min(sc["duration"] * 0.5, 1.2) if cid != "outro" else sc["start"] + 0.6
        settled_ = [n for t, n in seq_ if abs(t - t_set) < 0.05]
        if final < LATE_TEXT_MIN or not settled_:
            continue
        share = settled_[0] / final
        if share < LATE_TEXT_WARN:
            add("error" if share < LATE_TEXT_ERR else "warn", "late-text", t_set, f"{cid} ({sc['component']})",
                f"director|component:{sc['component']}",
                f"{t_set - sc['start']:.1f}s after its cut it shows {share:.0%} of its words — an empty card on screen",
                "print the first message/line on the cut (stagger ≤ 0.2 s), or cut in later", key=("latetext", cid))
    cw = 1080 - SAFE["left"] - SAFE["right"]                       # content width  (≈ 880)
    ch = SAFE["captionBand"][0] - SAFE["top"]                       # content height above the captions (≈ 930)
    for sid, s in shots.items():
        b = s["box"]
        w, h = b[2] - b[0], b[3] - b[1]
        if w < NARROW_W * cw and h < NARROW_H * ch:
            add("warn", "narrow-frame", s["t"], f"{sid} ({s['comp']})", "director",
                f"content is {w:.0f}×{h:.0f}px in an {cw}×{ch} zone — small object, dead field",
                "span the content width (≈ 860–880 px) or make the object/number the hero", key=("narrow", sid))
        if 0 < s["paper_w"] < SMALL_OBJ * cw:
            add("warn", "small-object", s["t"], f"{sid} ({s['comp']})", f"director|component:{s['comp']}",
                f"its paper spans {s['paper_w']:.0f}px (content width {cw}) — small and busy, not big and calm",
                "objects span the content width (≈ 860–880 px): width/wide param, or a bigger component", key=("smallobj", sid))
        if s["small"]:
            add("warn", "small-text", s["t"], f"{sid} ({s['comp']})", f"director|component:{s['comp']}",
                f"text at {', '.join(map(str, s['small']))} px — hard to read at phone size",
                f"main text ≥ {SMALL_FONT} px (printout rows included)", key=("small", sid))
    seq = sorted(shots.items(), key=lambda kv: kv[1]["start"])
    run: list[str] = []
    def similar(a, b):
        return all(abs(a[i] - b[i]) <= SAME_TOL for i in range(4))
    for i, (sid, s) in enumerate(seq):
        if run and similar(shots[run[-1]]["box"], s["box"]):
            run.append(sid)
        else:
            run = [sid]
        if len(run) == SAME_RUN:
            add("warn", "same-layout", shots[run[0]]["start"], " → ".join(run), "director",
                f"{SAME_RUN} shots in a row share the same composition (box ≈ {s['box']}) — reads as a template",
                "vary scale/position: a full-bleed number, an object low or right, a big Chillar beat", key=("same", run[0]))

    # captions are known exactly: a number word never shows before it is spoken
    for g in spec.get("captions", []):
        for w in g["words"]:
            if len(digits(w["text"])) >= 1 and w["start"] - g["start"] > 0.15:
                add("error", "early-number", g["start"], f"caption “{' '.join(x['text'] for x in g['words'])[:40]}”", "editor",
                    f"“{w['text']}” is captioned {w['start'] - g['start']:.1f}s before the voice says it",
                    "start a new caption chunk on the number", key=("early", "cap", w["text"], round(w["start"], 2)))

    # short shots
    for s in spec["scenes"]:
        if s["track"] not in (1, 2) or s["id"] in NO_PROBE:
            continue
        md = component_meta(s["component"]).get("minDuration", 0)
        if s["duration"] + 1e-6 < md:
            add("warn", "short-shot", s["start"], f"{s['id']} ({s['component']})", "editor",
                f"{s['duration']:.2f}s on screen, minDuration {md}s", "hold it longer or cut it")
        elif s["track"] == 1 and s["duration"] < 0.8 and s["id"] != "outro":
            add("warn", "short-shot", s["start"], f"{s['id']} ({s['component']})", "editor",
                f"{s['duration']:.2f}s shot — under 0.8s reads as a glitch unless it's a deliberate smash cut", "merge or hold")

    aud = audio_check(ep, issues) if audio else {"checked": False}
    issues.sort(key=lambda i: (i["sev"] != "error", i["t"] if i["t"] is not None else -1))
    errors = [i for i in issues if i["sev"] == "error"]
    look = sorted({i["t"] for i in issues if i["t"] is not None})[:12]
    report = {"episode": ep.name, "samples": len(data["samples"]), "errors": len(errors),
              "warnings": len(issues) - len(errors), "audio": aud, "issues": issues,
              "frames_to_check": look,
              "layout": {sid: {"t": round(v["start"], 2), "box": v["box"]} for sid, v in sorted(shots.items(), key=lambda kv: kv[1]["start"])}}
    (ep.cache / "qa.json").write_text(json.dumps(report, indent=1, ensure_ascii=False))
    return report


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("episode")
    ap.add_argument("--at", default="", help="extra comma-separated times to sample")
    ap.add_argument("--no-audio", action="store_true")
    ap.add_argument("--strict", action="store_true", help="exit 1 on warnings too")
    ap.add_argument("--for", dest="role", default="", help="print only issues routed to this role (e.g. director); "
                    ".cache/qa.json still holds all of them")
    a = ap.parse_args()
    extra = [float(x) for x in a.at.split(",") if x.strip()]
    r = qa(a.episode, extra, audio=not a.no_audio)
    shown = [i for i in r["issues"] if not a.role or a.role in i["route"]]
    for i in shown:
        t = f"t={i['t']:.2f}" if i["t"] is not None else "t=–"
        print(f"  {'✗' if i['sev'] == 'error' else '!'} [{i['route']}] {t} {i['kind']}: {i['where']} — {i['msg']} → {i['fix']}")
    au = r["audio"]
    if au.get("checked"):
        print(f"  audio: {au['lufs']} LUFS, {au['true_peak_dbtp']} dBTP" + (" (final.mp4 is older than scenes.json)" if au["stale"] else ""))
    hidden = f" ({len(r['issues']) - len(shown)} for other roles not shown)" if a.role else ""
    print(f"qa: {r['samples']} samples, {r['errors']} error(s), {r['warnings']} warning(s) → .cache/qa.json{hidden}")
    return 1 if r["errors"] or (a.strict and r["warnings"]) else 0


if __name__ == "__main__":
    sys.exit(main())
