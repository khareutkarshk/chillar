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
  narrow-frame    a shot's content covers < 65 % of the content width and < 30 % of its height
  small-text      a shot shows text under 36 px (one warning per shot)
  same-layout     4 shots in a row with the same content box (template feel)
  short-shot      a shot shorter than its component's minDuration (or < 0.8 s)
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


def area(b) -> float:
    return max(b[2] - b[0], 0) * max(b[3] - b[1], 0)


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
            shots[c["id"]] = {"t": t, "start": sc["start"], "box": u, "comp": c["comp"], "small": small}
    cw = 1080 - SAFE["left"] - SAFE["right"]                       # content width  (≈ 880)
    ch = SAFE["captionBand"][0] - SAFE["top"]                       # content height above the captions (≈ 930)
    for sid, s in shots.items():
        b = s["box"]
        w, h = b[2] - b[0], b[3] - b[1]
        if w < NARROW_W * cw and h < NARROW_H * ch:
            add("warn", "narrow-frame", s["t"], f"{sid} ({s['comp']})", "director",
                f"content is {w:.0f}×{h:.0f}px in an {cw}×{ch} zone — small object, dead field",
                "span the content width (≈ 860–880 px) or make the object/number the hero", key=("narrow", sid))
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
    a = ap.parse_args()
    extra = [float(x) for x in a.at.split(",") if x.strip()]
    r = qa(a.episode, extra, audio=not a.no_audio)
    for i in r["issues"]:
        t = f"t={i['t']:.2f}" if i["t"] is not None else "t=–"
        print(f"  {'✗' if i['sev'] == 'error' else '!'} [{i['route']}] {t} {i['kind']}: {i['where']} — {i['msg']} → {i['fix']}")
    au = r["audio"]
    if au.get("checked"):
        print(f"  audio: {au['lufs']} LUFS, {au['true_peak_dbtp']} dBTP" + (" (final.mp4 is older than scenes.json)" if au["stale"] else ""))
    print(f"qa: {r['samples']} samples, {r['errors']} error(s), {r['warnings']} warning(s) → .cache/qa.json")
    return 1 if r["errors"] or (a.strict and r["warnings"]) else 0


if __name__ == "__main__":
    sys.exit(main())
