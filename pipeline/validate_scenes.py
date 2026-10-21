#!/usr/bin/env python3
"""Resolve + validate episodes/<ep>/scenes/scenes.json against the brand bible.

scenes.json (written by the director in /render, refined by the editor, editable by you):
{
  "scenes": [
    {"id": "hook", "component": "hook-card", "at": 0, "params": {...}},
    {"id": "mdr",  "component": "statement", "at": "w8", "params": {...}, "fact": "F2"},
    {"id": "bill", "component": "odometer-number", "at": "w15", "cut": "whip", "params": {...}, "fact": "F3"},
    {"id": "st1",  "component": "stamp", "at": "w19", "until": "w26", "params": {...}},
    {"id": "react","component": "mascot-reaction", "at": "w33", "duration": 2.0, "params": {...}}
  ],
  "effects": [{"type": "punch", "at": "w38"}],
  "theme": "pastel",          // pastel | calm | night — chosen for the script's mood
  "outro": {"cut": "cut", "params": {}},     // duration is fixed by the brand (OUTRO_S), not planned
  "music": {"track": "", "under_voice_db": -22}
}
Times: seconds, "w12" (start of word 12), "w12.end", or "+0.4" offsets like "w12+0.2".
Scenes (layer "scene") last until the next scene starts. Overlays need "until" or "duration".

Cuts: every scene enters on a hard cut unless it says "cut": "whip" | "zoom" | "wipe" | "page".
Those are real editor moves on the shots themselves (components/transition) and never carry text.
Chapters: each script chapter is one rupee-note field (brand/tokens.json "fields"); the field
hard-cuts on the chapter's first scene, so a scene must start on every chapter's first word.
Chapter names are for the writer — they never appear on screen.
Format (30/60/90 from script.md target_seconds) sets duration, stamps, re-hook cadence, cut budget.

  validate_scenes.py episodes/<ep>  -> .cache/scenes.resolved.json, exit 1 on errors
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_composition import component_meta, merged_params  # noqa: E402
from lib.common import ROOT  # noqa: E402
from lib.episode import load  # noqa: E402
import memes  # noqa: E402

TOK = json.loads((ROOT / "brand" / "tokens.json").read_text())
M = TOK["motion"]
SAFE = TOK["safeZone"]
TR = TOK["transitions"]
FIELDS = TOK["fieldSlots"]
# action foley (printer on a printing slip, whoosh on a styled cut, typing) beats the reaction coin: the 2026-10-26→31
# reels lost 1–3 printers/whooshes each to a decorative coin, so receipts printed and transitions moved in silence
PRIORITY = {"meme": 4, "stamp": 5, "scratch": 4, "ding": 3, "glitch": 3, "printer": 3, "typing": 2, "whoosh": 2, "coin": 1}
FOLEY_PRIORITY = 4    # a one-off sound (brand/sfx/<name>.wav: cough, slurp, knock) was placed on purpose for a line
OVERRIDE_BONUS = 1    # a scene's own "sfx" beats a component default at the same rank
SHORT_BLOCK = 0.7     # a shot under 70 % of its component's minDuration is an error, not a warning
CHAPTER_SNAP = 0.35   # a scene must start this close to a chapter's first word
# The outro cuts in on the last word and is short (2026-10-21): the old 0.35 s gap + 3.2 s receipt was ~10 % of a 30 s
# reel after the voice stopped, where viewers swipe and never "finish" the reel. The disclaimer still prints by ~0.35 s.
OUTRO_GAP, OUTRO_S = 0.12, 1.9
# script-structure words that must never be shown as a label/title card
STRUCTURE = re.compile(r"^(the\s+)?(setup|set-up|set up|escalation|payoff|pay-off|hook|intro|introduction|outro|"
                       r"conclusion|twist|plot twist|context|recap|summary|chapter\s*\d*|part\s*\d+|page\s*\d+|"
                       r"step\s*\d+|act\s*\d+|section\s*\d+|last page)$", re.I)
HEADLINE_KEYS = {"question", "title", "text"}
TEXT_FREE_LAYERS = {"transition", "background"}


class Ctx:
    def __init__(self, words):
        self.words = {w["id"]: w for w in words}

    def t(self, v) -> float:
        if isinstance(v, (int, float)):
            return float(v)
        m = re.fullmatch(r"\s*(w\d+)(\.end)?\s*([+-]\s*[\d.]+)?\s*", str(v))
        if not m:
            return float(v)
        w = self.words[m.group(1)]
        base = w["end"] if m.group(2) else w["start"]
        return base + (float(m.group(3).replace(" ", "")) if m.group(3) else 0.0)


def chapter_starts(words) -> list[tuple[str, float]]:
    out, cur = [], None
    for w in words:
        if w["chapter"] != cur:
            out.append((w["chapter"], w["start"]))
            cur = w["chapter"]
    return out


def caption_groups(words, end_limit: float, max_words=4, max_chars=22) -> list[dict]:
    groups, cur = [], []
    is_num = lambda t: bool(re.search(r"[\d₹]", t))  # noqa: E731
    for i, w in enumerate(words):
        nxt = words[i + 1] if i + 1 < len(words) else None
        # a number never appears before it is spoken: it always opens its own caption chunk
        if cur and is_num(w["text"]):
            groups.append(cur)
            cur = []
        cur.append(w)
        text = " ".join(x["text"] for x in cur)
        brk = (len(cur) >= max_words or len(text) >= max_chars or w["text"][-1:] in ".?!," or
               nxt is None or nxt["line"] != w["line"] or (nxt and nxt["start"] - w["end"] > 0.45))
        if brk:
            groups.append(cur)
            cur = []
    out = []
    for i, g in enumerate(groups):
        start = g[0]["start"]
        end = groups[i + 1][0]["start"] if i + 1 < len(groups) else min(g[-1]["end"] + 0.4, end_limit)
        end = min(end, g[-1]["end"] + 0.8)
        out.append({"start": round(start, 3), "end": round(end, 3),
                    "words": [{"text": w["text"], "start": w["start"], "end": w["end"]} for w in g]})
    return out


def strings(o):
    """Every string a viewer could read in a params tree."""
    if isinstance(o, dict):
        for v in o.values():
            yield from strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from strings(v)
    elif isinstance(o, str):
        yield o


def resolve(ep_dir: str, demo: bool | None = None) -> tuple[dict, list[str], list[str]]:
    ep = load(ep_dir)
    errors, warns = [], []
    sp = ep.dir / "scenes" / "scenes.json"
    wp = ep.cache / "words.json"
    if not sp.exists():
        return {}, [f"missing {sp.relative_to(ep.dir)} — run /render so the director plans the scenes"], []
    if not wp.exists():
        return {}, ["missing .cache/words.json — run align first"], []
    plan = json.loads(sp.read_text())
    words = json.loads(wp.read_text())
    ctx = Ctx(words)
    voice_end = words[-1]["end"] + OUTRO_GAP
    outro_d = OUTRO_S
    if "duration" in plan.get("outro", {}) and abs(float(plan["outro"]["duration"]) - OUTRO_S) > 0.01:
        warns.append(f"outro duration {plan['outro']['duration']} ignored — the brand outro is {OUTRO_S}s "
                     "(a long tail after the voice is where viewers swipe)")
    total = round(voice_end + outro_d, 3)
    fmt_key = ep.format
    FMT = TOK["formats"][fmt_key]
    demo = demo if demo is not None else bool(ep.meta.get("demo", False))
    if ep.theme not in TOK["themes"]:
        errors.append(f"theme '{ep.theme}' unknown — one of {sorted(TOK['themes'])}")
    soft = warns if demo else errors

    # real memes: fetched now (build time), cached in .cache/memes — pipeline/memes.py
    got, merrs = memes.ensure(ep_dir, memes.wanted(plan)) if memes.wanted(plan) else ({}, [])
    errors.extend(merrs)

    scenes, overlays = [], []
    for raw in plan.get("scenes", []):
        name = raw.get("component")
        if not (ROOT / "components" / str(name) / "component.json").exists():
            errors.append(f"{raw.get('id')}: unknown component '{name}'")
            continue
        meta = component_meta(name)
        if name == "wordmark":
            errors.append(f"{raw.get('id')}: the wordmark is inserted automatically on every frame — remove it from scenes.json")
            continue
        if meta.get("layer") in TEXT_FREE_LAYERS:
            errors.append(f"{raw.get('id')}: '{name}' is placed automatically — use a scene's \"cut\" key for transitions")
            continue
        try:
            start = ctx.t(raw.get("at", 0))
        except (KeyError, ValueError) as e:
            errors.append(f"{raw.get('id')}: bad time {raw.get('at')!r} ({e})")
            continue
        s = {"id": raw["id"], "component": name, "params": merged_params(name, raw.get("params", {})),
             "start": round(start, 3), "layer": meta.get("layer", "scene"), "fact": raw.get("fact"),
             "rehook": raw.get("rehook", meta.get("rehook", False)), "sfx_override": raw.get("sfx"),
             "raw_params": raw.get("params", {}), "cut": raw.get("cut", TR["default"])}
        if name == "meme":
            mp = s["params"]
            m = got.get(memes.key(mp["kind"], mp["meme"], int(mp["pick"]))) if mp.get("meme") else None
            if m:
                mp["kind"] = m.get("as", mp["kind"])    # an "image" template that is really animated plays as a GIF
                mp.update({"_file": m["path"], "_w": m["w"], "_h": m["h"],
                           **({"_" + k: m[k] for k in ("frames", "cols", "rows", "fps")} if mp["kind"] == "video" else {})})
            elif mp.get("meme"):
                errors.append(f"{s['id']}: meme '{mp['meme']}' not fetched")
            snd = got.get(memes.key("sound", mp["sound"], int(mp["soundPick"]))) if mp.get("sound") else None
            if snd:
                s["sfx_override"] = [{"at": float(mp["soundAt"]), "sound": "meme:" + snd["path"]}]
        elif name == "mascot-reaction" and s["params"].get("sound"):
            mp = s["params"]
            snd = got.get(memes.key("sound", mp["sound"], int(mp.get("soundPick", 0))))
            if snd:   # the meme sound replaces the arrival coin
                s["sfx_override"] = [{"at": float(mp.get("soundAt", 0)), "sound": "meme:" + snd["path"]}]
            else:
                errors.append(f"{s['id']}: meme sound '{mp['sound']}' not fetched")
        unknown = set(raw.get("params", {})) - set(meta.get("params", {}))
        if unknown:
            warns.append(f"{s['id']}: params not declared by {name}: {sorted(unknown)}")
        if s["cut"] not in TR["styles"]:
            errors.append(f"{s['id']}: cut '{s['cut']}' — use one of {TR['styles']}")
            s["cut"] = "cut"
        if s["layer"] == "overlay":
            if "until" in raw:
                s["end"] = ctx.t(raw["until"])
            else:
                s["end"] = start + float(raw.get("duration", meta.get("minDuration", 1.2) + 0.6))
            if s["cut"] != "cut":
                warns.append(f"{s['id']}: overlays don't take a cut style — ignored")
            overlays.append(s)
        else:
            scenes.append(s)

    scenes.sort(key=lambda s: s["start"])
    outro_start = round(voice_end, 3)
    for i, s in enumerate(scenes):
        s["end"] = scenes[i + 1]["start"] if i + 1 < len(scenes) else outro_start
    if scenes and scenes[0]["start"] > 0.001:
        errors.append(f"first scene starts at {scenes[0]['start']}s — frame 1 must show the stakes (start a scene at 0)")
    if scenes and scenes[0]["component"] not in ("hook-card", "receipt-list", "passbook-page", "odometer-number", "marker-highlight", "mithai-dabba"):
        warns.append(f"frame 1 is '{scenes[0]['component']}' — hook-card or a printed receipt/passbook shows stakes best")
    if scenes and scenes[0]["component"] in ("receipt-list", "passbook-page") and not scenes[0]["params"].get("printed"):
        warns.append(f"frame-1 {scenes[0]['component']} is not printed:true — frame 1 will be nearly empty")

    outro_params = {"follow": f"Follow {TOK['brand']['handle']}", **plan.get("outro", {}).get("params", {})}
    outro = {"id": "outro", "component": "outro", "params": merged_params("outro", outro_params),
             "start": outro_start, "end": total, "layer": "scene", "rehook": False, "sfx_override": None,
             "raw_params": plan.get("outro", {}).get("params", {}), "cut": plan.get("outro", {}).get("cut", "cut")}

    # ---------------- chapter fields: one rupee-note colour per chapter, hard cut on its first scene
    seq = TOK["fieldSequence"]
    chs = chapter_starts(words)
    field_cuts = []
    for n, (name, t0) in enumerate(chs):
        f = ep.chapter_fields.get(name) or seq[min(n, len(seq) - 1)]
        if f not in FIELDS:
            errors.append(f"chapter '{name}': unknown field '{f}' — one of {sorted(FIELDS)}")
            f = "bone"
        if n == 0:
            field_cuts.append({"start": 0.0, "field": f, "chapter": name})
            continue
        near = [s for s in scenes if abs(s["start"] - t0) <= CHAPTER_SNAP]
        if not near:
            errors.append(f"chapter '{name}' starts at {t0:.2f}s but no scene cuts there — start a scene on its first word "
                          f"(the field changes on that cut)")
            continue
        sc = min(near, key=lambda s: abs(s["start"] - t0))
        if field_cuts and field_cuts[-1]["field"] == f:
            warns.append(f"chapter '{name}' uses the same field as the chapter before it ({f}) — the chapter change won't read")
        field_cuts.append({"start": sc["start"], "field": f, "chapter": name})
    outro_field = plan.get("outro", {}).get("field", "bone")
    field_cuts.append({"start": outro_start, "field": outro_field if outro_field in FIELDS else "bone", "chapter": "(outro)"})
    n_ch = len(chs)
    lo_c, hi_c = FMT["chapters"]
    if not lo_c <= n_ch <= hi_c:
        warns.append(f"{n_ch} chapters — a {fmt_key}s reel wants {lo_c}" + (f"–{hi_c}" if hi_c != lo_c else ""))

    # ---------------- transitions: real cuts on the shots themselves, never title cards
    field_at = lambda t: [c for c in field_cuts if c["start"] <= t + 1e-6][-1]["field"]  # noqa: E731
    styles = component_meta("transition")["styles"]
    trans, prev_style, prev_t = [], None, -99.0
    ordered = scenes + [outro]
    for i, s in enumerate(ordered):
        if s["cut"] == "cut":
            continue
        if i == 0:
            errors.append(f"{s['id']}: frame 1 can't enter on a '{s['cut']}' — it must be fully drawn at t=0")
            continue
        if s["cut"] == prev_style:
            errors.append(f"{s['id']}: two '{s['cut']}' transitions in a row read as a preset — vary it or hard-cut")
        if s["start"] - prev_t < TR["minSecondsBetweenNonCut"]:
            errors.append(f"{s['id']}: '{s['cut']}' {s['start'] - prev_t:.1f}s after the last one — keep ≥ "
                          f"{TR['minSecondsBetweenNonCut']:.0f}s between styled transitions (hard cuts are the default)")
        st = styles[s["cut"]]
        trans.append({"id": f"tr-{s['id']}", "component": "transition", "start": round(s["start"] - st["pre"], 3),
                      "end": round(s["start"] + st["post"], 3), "layer": "transition", "rehook": False,
                      "sfx_override": None, "raw_params": {},
                      "params": merged_params("transition", {"style": s["cut"], "from": ordered[i - 1]["id"], "to": s["id"],
                                                             "field": field_at(s["start"]), "cut": s["start"]})})
        prev_style, prev_t = s["cut"], s["start"]
    budget = TR["maxNonCutPerVideo"][fmt_key]
    if len(trans) > budget:
        errors.append(f"{len(trans)} styled transitions — a {fmt_key}s reel gets at most {budget}; the rest are hard cuts")

    # the channel wordmark: every frame until the outro (which carries the handle itself)
    wordmark = {"id": "wordmark", "component": "wordmark", "start": 0.0, "end": outro_start, "layer": "overlay",
                "rehook": False, "sfx_override": [], "raw_params": {},
                "params": merged_params("wordmark", {"handle": TOK["brand"]["handle"]})}
    allv = scenes + [outro] + overlays + trans + [wordmark]
    for s in allv:
        s["duration"] = round(max(0.05, s["end"] - s["start"]), 3)
        md = component_meta(s["component"]).get("minDuration", 0)
        if s["duration"] + 1e-6 < md and s["layer"] != "transition" and s["id"] != "wordmark":
            msg = f"{s['id']}: {s['duration']:.2f}s is shorter than {s['component']} minDuration {md}s"
            if s["duration"] < SHORT_BLOCK * md:     # it can't finish its own entrance/print — reads as a glitch
                errors.append(msg + f" (< {SHORT_BLOCK:.0%}: hold it to the next word, or merge it into the shot before)")
            else:
                warns.append(msg)

    # ---------------- on-screen text: no structure labels, short headlines
    chapter_names = {re.sub(r"\W+", " ", c).strip().lower() for c, _ in chs}
    for s in scenes + overlays + [outro]:
        for txt in strings(s.get("raw_params", {})):
            plain = re.sub(r"[*_#:.!?\-–—]+", " ", txt).strip()
            if STRUCTURE.match(plain) or plain.lower() in chapter_names:
                errors.append(f"{s['id']}: shows '{txt}' — script structure (chapter names, setup/escalation/payoff, "
                              f"part/page/step numbers) never appears on screen; show the content instead")
        for k in HEADLINE_KEYS & set(s.get("raw_params", {})):
            v = s["raw_params"][k]
            if isinstance(v, str) and len(v.replace("*", "").split()) > 7:
                warns.append(f"{s['id']}: {k} is {len(v.split())} words — a headline reads in one beat at ≤ 6")

    # ---------------- visual change cadence (scene/overlay starts + component beats + effects)
    beats = sorted({round(s["start"], 2) for s in allv} |
                   {round(s["start"] + float(e["at"]), 2) for s in allv
                    for e in component_meta(s["component"]).get("sfx", [])} |
                   {round(ctx.t(f["at"]), 2) for f in plan.get("effects", [])})
    beats = [b for b in beats if b < outro_start] + [outro_start]
    for a, b in zip(beats, beats[1:]):
        if b - a > M["maxSecondsBetweenVisualChanges"] + 0.05:
            errors.append(f"no visual change between {a:.2f}s and {b:.2f}s ({b - a:.1f}s > {M['maxSecondsBetweenVisualChanges']}s)")

    # ---------------- re-hooks (cadence depends on format)
    every = FMT["rehookEvery"]
    rh = sorted([s["start"] for s in allv if s.get("rehook")] +
                [s["start"] + float(e["at"]) for s in allv for e in component_meta(s["component"]).get("sfx", [])
                 if e["sound"] in ("scratch", "glitch")])
    # the first re-hook comes early: 3–15 s (hook over, explaining starts) was the swipe zone on 5 of 6 reels
    first_by = FMT.get("firstRehookBy", every)
    first = next((r for r in rh if r > 1.0), None)
    if first is None or first > first_by + 0.5:
        errors.append(f"first re-hook at {first or outro_start:.1f}s — a {fmt_key}s reel needs one by {first_by:.0f}s "
                      "(stamp, reveal, meme, Chillar beat: the 3–15 s stretch is where viewers swipe)")
    prev = 0.0
    for r in rh + [outro_start]:
        if r - prev > every + 0.5:
            errors.append(f"no re-hook between {prev:.1f}s and {r:.1f}s (> {every:.0f}s for a {fmt_key}s reel)")
        prev = r

    # ---------------- overlays should not bleed into the next scene (muddles the message)
    for o in overlays:
        for sc in scenes[1:] + [outro]:
            if o["start"] < sc["start"] - 0.05 and o["end"] > sc["start"] + 0.15:
                warns.append(f"{o['id']}: runs {o['end'] - sc['start']:.2f}s into '{sc['id']}' — end it at the cut (until: that scene's 'at')")
                break

    # ---------------- stamps (count depends on format; never more than 3)
    # a component that inks a red stamp on its own paper (receipt-list stampTotal) is a stamp on screen too
    n_st = sum(1 for s in overlays if s["component"] == "stamp") + \
        sum(1 for s in scenes if (s.get("params") or {}).get("stampTotal"))
    lo_s, hi_s = FMT["stamps"]
    if n_st > hi_s:
        errors.append(f"{n_st} stamps — a {fmt_key}s reel gets at most {hi_s}")
    if n_st < lo_s:
        soft.append(f"{n_st} stamp(s) — a {fmt_key}s reel wants {lo_s}–{hi_s}")

    # ---------------- duration + word count for the format
    lo, hi = FMT["seconds"]
    if not lo <= total <= hi:     # creator accepted the length (produce.py --accept-length) → a warning, not a block
        (warns if ep.config.get("render", {}).get("length_accepted") else soft).append(f"duration {total:.1f}s outside {lo}–{hi}s for the {fmt_key}s format")
    lo_w, hi_w = FMT["words"]
    if not lo_w <= len(words) <= hi_w:
        warns.append(f"{len(words)} spoken words — the {fmt_key}s format reads best at {lo_w}–{hi_w}")

    # ---------------- facts: on-screen numbers must be covered by a cited fact
    DATA_KEYS = {"value", "amount", "principal", "rate", "years", "bars", "tiers", "rows", "opening"}

    def on_screen(o, key=""):
        """Text a viewer can read (strings anywhere) + numeric data fields; not layout numbers."""
        if isinstance(o, dict):
            return " ".join(on_screen(v, k) for k, v in o.items())
        if isinstance(o, list):
            return " ".join(on_screen(v, key) for v in o)
        if isinstance(o, str):
            return o
        return str(o) if key in DATA_KEYS else ""

    for s in scenes + overlays:
        txt = on_screen(s.get("raw_params", {}))
        if re.search(r"\d|₹|%", txt) and not s.get("fact"):
            spoken = [w for w in words if s["start"] - 0.5 <= w["start"] <= s["end"] + 0.5]
            lines = {w["line"] for w in spoken}
            if not any(l.facts for l in ep.lines if l.id in lines):
                errors.append(f"{s['id']}: shows numbers but no 'fact' id and no cited line is spoken during it")
        if s.get("fact") and s["fact"] not in ep.facts:
            errors.append(f"{s['id']}: fact {s['fact']} not in facts.md")

    # ---------------- safe zones for positioned overlays
    for s in overlays:
        p = s["params"]
        if s["component"] == "stamp":
            w = len(str(p.get("text", ""))) * 0.6 * p["size"] + 0.9 * p["size"]
            box = (p["x"] - w / 2, p["y"] - p["size"] * 0.8, p["x"] + w / 2, p["y"] + p["size"] * 0.8)
        elif s["component"] == "mascot-reaction":
            box = (p["x"] - p["size"] / 2, p["y"] - p["size"] * 1.1, p["x"] + p["size"] / 2, p["y"])
        else:
            continue
        if box[0] < SAFE["left"] or box[2] > 1080 - SAFE["right"] or box[1] < SAFE["top"] or box[3] > 1920 - SAFE["bottom"]:
            errors.append(f"{s['id']}: {s['component']} box {tuple(round(v) for v in box)} leaves the safe zone")
        wm = TOK["wordmark"]["box"]
        if box[0] < wm["x"] + wm["w"] and box[2] > wm["x"] and box[1] < wm["y"] + wm["h"] and box[3] > wm["y"]:
            warns.append(f"{s['id']}: covers the @handle wordmark (y {wm['y']}–{wm['y'] + wm['h']}) — move it up")
        cb = SAFE["captionBand"]
        if box[3] > cb[0] + 30 and box[1] < cb[1]:
            warns.append(f"{s['id']}: overlaps the caption band (y {cb[0]}–{cb[1]})")

    # ---------------- real memes: budget per format, never back to back
    mm = [s for s in scenes if s["component"] == "meme"]
    # a mascot-reaction carrying a meme sound is a meme beat too: budget + freshness
    mb = mm + [s for s in allv if s["component"] == "mascot-reaction" and s["params"].get("sound")]
    cap = {"30": 3, "60": 5, "90": 7}.get(fmt_key, 5)
    if len(mb) > cap:
        errors.append(f"{len(mb)} meme beats — {fmt_key} s allows ≤ {cap} (CLAUDE.md §3)")
    for a, b in zip(scenes, scenes[1:]):
        if a["component"] == b["component"] == "meme":
            warns.append(f"{a['id']} → {b['id']}: two memes in a row — cut back to the story between them")
    # freshness: Gen Z has to recognise it from this week, not from 2015 (CLAUDE.md §3)
    try:
        classics = []
        for s in mb:
            p = s["params"]
            checks = [(p.get("kind", "image"), p.get("meme"), int(p.get("pick", 0)))] if p.get("meme") and s["component"] == "meme" else []
            checks += [("sound", p["sound"], int(p.get("soundPick", 0)))] if p.get("sound") else []
            for kind, q, pick in checks:
                m = got.get(memes.key(kind, q, pick))
                if not m:
                    continue
                state, why = memes.freshness(m["title"], kind, m.get("hit", {}).get("tid"), ep)
                if state == "stale":
                    errors.append(f"{s['id']}: {kind} meme '{m['title']}' is stale — {why}. Use `memes.py trending` "
                                  "or facts.md '## Culture now'")
                elif state == "classic":
                    classics.append(f"{s['id']} ('{m['title']}', {why})")
        if len(classics) > memes.CLASSICS_PER_REEL:
            errors.append(f"{len(classics)} classic (old but still-everywhere) memes — ≤ {memes.CLASSICS_PER_REEL} per reel, "
                          f"the rest must be this week's: {'; '.join(classics)}")
    except Exception as ex:                     # offline: can't prove freshness, don't block on the network
        warns.append(f"meme freshness not checked ({ex})")
    tpl = [(s["params"].get("meme") or "").lower() for s in mm]
    if len(set(tpl)) < len(tpl):
        warns.append("the same meme template is used twice")
    # no repeats across reels: followers saw last week's meme (CLAUDE.md §3 — fresh only)
    recent = memes.recent_use(ep_dir)
    for s in mb:
        p = s["params"]
        uses = [(p.get("kind", "image"), p["meme"], int(p.get("pick", 0)))] if s["component"] == "meme" and p.get("meme") else []
        uses += [("sound", p["sound"], int(p.get("soundPick", 0)))] if p.get("sound") else []
        for kind, q, pick in uses:
            m = got.get(memes.key(kind, q, pick))
            for n in {memes.norm_title(q), memes.norm_title((m or {}).get("title", ""))} - {""}:
                if n in recent:
                    errors.append(f"{s['id']}: meme '{q}' was used in {recent[n]} (one of the last {memes.RECENT_REELS} "
                                  "reels) — pick another from facts.md '## Culture now' or "
                                  f"`memes.py trending --episode episodes/{ep.name}`")
                    break

    # ---------------- SFX: component defaults (or scene override), thinned to ≥2 s apart by priority
    cand = []
    for s in allv:
        own = s["sfx_override"] is not None
        evs = s["sfx_override"] if own else component_meta(s["component"]).get("sfx", [])
        for e in evs:
            if e.get("skipIf") and s["params"].get(e["skipIf"]):
                continue
            t = s["start"] + float(e["at"])
            if t < total:
                base = e["sound"].split(":")[0]
                rank = PRIORITY.get(base, FOLEY_PRIORITY) + (OVERRIDE_BONUS if own else 0)
                if base not in PRIORITY and not (ROOT / "brand" / "sfx" / f"{e['sound']}.wav").exists() \
                        and not list((ROOT / "brand" / "sfx" / "custom").glob(f"{e['sound']}.*")):
                    errors.append(f"{s['id']}: sfx '{e['sound']}' has no file — `fetch_assets.py foley {e['sound']} "
                                  f"\"<search words>\"` makes brand/sfx/{e['sound']}.wav")
                cand.append({"t": round(t, 3), "sound": e["sound"], "from": s["id"], "rank": int(e.get("priority", rank))})
    keep, dropped = [], []
    for c in sorted(cand, key=lambda c: (-c["rank"], c["t"])):
        near = [k for k in keep if abs(c["t"] - k["t"]) < M["minSecondsBetweenSfx"]]
        if not near:
            keep.append(c)
        else:
            dropped.append({**c, "lost_to": f"{near[0]['sound']}@{near[0]['t']:.1f} ({near[0]['from']})"})
    keep.sort(key=lambda c: c["t"])
    if dropped:      # expected thinning, one line (agents re-read this output every validate loop)
        warns.append(f"{len(dropped)} sfx dropped (within 2 s of a higher-priority sound): "
                     + ", ".join(f"{d['sound']}@{d['t']:.1f}" for d in sorted(dropped, key=lambda d: d["t"])))
    for d in dropped:   # a sound the plan asked for by hand that will never play is a decision, not noise
        if any(s["id"] == d["from"] and s["sfx_override"] for s in allv):
            warns.append(f"{d['from']}: its own sfx '{d['sound']}'@{d['t']:.1f} loses to {d['lost_to']} — move one ≥ 2 s "
                         "apart, or silence the other with \"sfx\": []")

    tracks = {"scene": 1, "overlay": 2, "transition": 3}
    out_scenes = [{"id": "bg", "component": "chapter-field", "start": 0, "duration": total, "track": 0,
                   "params": merged_params("chapter-field", {"chapters": [{"start": c["start"], "field": c["field"]}
                                                                          for c in field_cuts]})}]
    for s in sorted(allv, key=lambda s: (tracks[s["layer"]], s["start"])):
        out_scenes.append({"id": s["id"], "component": s["component"], "params": s["params"],
                           "start": s["start"], "duration": s["duration"], "track": tracks[s["layer"]]})
    effects = [{"type": f["type"], "at": round(ctx.t(f["at"]), 3), "amount": f.get("amount", 1.06)}
               for f in plan.get("effects", [])]
    resolved = {"episode": ep.name, "title": ep.meta.get("title", ep.name), "duration": total, "format": fmt_key,
                "theme": ep.theme,
                "voice_end": round(voice_end, 3), "outro_start": outro_start,
                "scenes": out_scenes, "effects": effects, "sfx": keep,
                "sfx_dropped": sorted(dropped, key=lambda d: d["t"]),
                "captions": caption_groups(words, outro_start),
                "fields": field_cuts,
                "music": {**ep.config["music"], **plan.get("music", {})},
                "stats": {"stamps": n_st, "visual_beats": len(beats), "rehooks": len(rh), "sfx": len(keep),
                          "transitions": [f"{t['params']['style']}@{t['params']['cut']:.2f}" for t in trans]}}
    return resolved, errors, warns


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    a = ap.parse_args()
    ep = load(a.episode)
    res, errors, warns = resolve(a.episode)
    if res:
        (ep.cache / "scenes.resolved.json").write_text(json.dumps(res, indent=1, ensure_ascii=False))
        st = res["stats"]
        print(f"scenes: {len(res['scenes'])} clips, {res['duration']:.1f}s ({res['format']}s format), {st['stamps']} stamps, "
              f"{st['rehooks']} re-hooks, {st['sfx']} sfx, transitions: {', '.join(st['transitions']) or 'all hard cuts'}")
        print("fields: " + " → ".join(f"{c['field']}@{c['start']:.2f}" for c in res["fields"]))
    for w in warns:
        print(f"  ! {w}")
    for e in errors:
        print(f"  ✗ {e}")
    print("  ✓ scenes valid" if not errors else f"  {len(errors)} error(s) — fix scenes.json")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
