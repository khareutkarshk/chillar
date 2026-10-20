#!/usr/bin/env python3
"""Real (global) memes, fetched per episode at build time — never a library up front.

  memes.py search "<query>" --kind image|video|sound [-n 8]   titles to pick from (for the director)
  memes.py trending [--kind image|video|sound]                 what's hot today (cached a day)
  memes.py fetch episodes/<ep>                                 download every meme scenes.json asks for

Sources (no API keys): imgflip templates (image), imgflip GIF templates (video, silent mp4),
myinstants (sound). Files land in episodes/<ep>/.cache/memes/ (gitignored, re-fetched if missing)
with a manifest (memes.json) keyed by kind + query + pick, so a rebuild reuses the same file.
A video meme becomes a sprite sheet (12 fps, ≤ 48 frames) the `meme` component steps through
on the master timeline — seek-safe, no <video> element. Every file is logged in
assets/licenses.json as "Meme (uncleared, creator-approved)" with its source page (CLAUDE.md §6).
Images may be global or Indian (Bollywood/TV/desi templates). Video and sound memes are global only:
titles that look Indian are refused for those. No politician memes in either (finance channel, not politics).
Fresh only: validate blocks a meme that isn't trending today (imgflip new & rising / myinstants trending)
or listed in facts.md `## Culture now`, and allows one old-but-everywhere classic (imgflip top-30-days).
"""
from __future__ import annotations

import argparse
import html
import json
import math
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import licenses  # noqa: E402
from lib.common import ROOT, Candidate, session, slug  # noqa: E402
from lib.episode import load  # noqa: E402

LICENSE = "Meme (uncleared, creator-approved)"
FPS, MAX_FRAMES, SPRITE_W, COLS = 12, 48, 480, 8
SOUND_MAX_S = 3.0
# the creator's rule: Indian memes as images only — video/sound must be global
INDIAN = re.compile(r"\b(bollywood|tollywood|hindi|indian?|desi|bharat|hera ?pheri|phir hera|babu ?bhaiya|"
                    r"raju|shyam|akshay|salman|shah ?rukh|srk|amitabh|bachchan|aamir|ranveer|ranbir|rajinikanth|"
                    r"kapil|modi|rahul gandhi|kejriwal|paresh|johny lever|sacred games|mirzapur|panchayat|"
                    r"cid|tmkoc|jethalal|daya|bhabhi|bhai|beta|yaar|arey|arre|diwali|holi|navratri|ganpati|"
                    r"bappa|chhath|punjabi|bhojpuri|tamil|telugu|marathi|gujarati|bengali)\b", re.I)
POLITICS = re.compile(r"\b(modi|rahul gandhi|kejriwal|yogi|amit shah|owaisi|bjp|congress|aap|mamata|trump|biden|"
                      r"obama|putin|election)\b", re.I)
# brand safety (CLAUDE.md §3: no sexual jokes, punch up): titles that are, or templates whose own printed text is,
# sexual / drug / gore. Template text isn't visible to a title filter, so known offenders are listed by name.
UNSAFE = re.compile(r"\b(sex\w*|nsfw|porn\w*|nude\w*|naked|virgin\w*|horny|boob\w*|dick|thicc|onlyfans|"
                    r"weed|stoned|cocaine|drunk|suicid\w*|gore|corpse|hentai|waifu|"
                    r"peak life events)\b", re.I)
HINGLISH = re.compile(r"\b(hai|hain|kya|nahi|bhai|bhaiya|mere|mujhe|kar|raha|tha|aur|ko|ka|ki|ke|bhi|ye|wo|"
                      r"kaun|kidhar|abhi|yaar|arre|are|beta|ji|baap|yaad|aya|aaya|re|accha|achha|chal|bas|haan|"
                      r"matlab|kuch|sab|bohot|bahut|paisa|paise|kaise|kyun|kyu|tum|tu|mera|meri|tera|teri|"
                      r"hoga|gaya|gayi|karo|bolo|dekh|dekho|chalo|chal|arey|oye|abey|abe)\b|[\u0900-\u097f]", re.I)
# imgflip template ids are one global counter (same base-36 as every image it makes) — dated anchors, so a
# template's id gives its upload month. An old film still uploaded last month still reads "new": that's why
# freshness = proven current (trending today / the researcher's Culture now), and age is only a second check.
ANCHORS = [(112126428, 2017 + 7 / 12), (222403160, 2020 + 1 / 12), (309868304, 2021 + 5 / 12), (371619279, 2022 + 2 / 12)]
CLASSICS_PER_REEL = 1          # a still-everywhere classic (imgflip top-30-days) — at most one per reel
MAX_TEMPLATE_MONTHS = 36       # older uploads need the researcher's proof that they're everywhere this week
TREND = ROOT / ".cache" / "memes_trending.json"
DELAY = 1.5     # seconds between requests to one site (low volume, polite)
_last: dict[str, float] = {}


def _get(url: str, **kw):
    host = url.split("/")[2]
    wait = DELAY - (time.time() - _last.get(host, 0))
    if wait > 0:
        time.sleep(wait)
    r = session.get(url, timeout=kw.pop("timeout", 30), **kw)
    _last[host] = time.time()
    r.raise_for_status()
    return r


# ------------------------------------------------------------------ search
def _imgflip(query: str, gifs: bool) -> list[dict]:
    page = _get("https://imgflip.com/memesearch", params={"q": query, **({"gifs_only": 1} if gifs else {})}).text
    out, seen = [], set()
    for m in re.finditer(r'<a title="([^"]+)" href="(/meme/[^"]+)">\s*<img class="shadow"[^>]*'
                         r'src="//i\.imgflip\.com/\d/(\w+)\.jpg"', page):
        title, href, iid = html.unescape(m.group(1)).removesuffix(" Meme"), m.group(2), m.group(3)
        if iid in seen:
            continue
        seen.add(iid)
        out.append({"title": title, "page": "https://imgflip.com" + href,
                    "url": f"https://i.imgflip.com/{iid}.{'mp4' if gifs else 'jpg'}", "id": iid,
                    "tid": str(int(iid, 36))})      # template id == the image's base-36 id
    return out


def _myinstants(query: str) -> list[dict]:
    page = _get("https://www.myinstants.com/en/search/", params={"name": query}).text
    out = []
    for m in re.finditer(r"play\('(/media/sounds/[^']+)'[^)]*\)[\s\S]*?href=\"(/en/instant/[^\"]+)\"[^>]*>([^<]+)<", page):
        out.append({"title": html.unescape(m.group(3)).strip(), "page": "https://www.myinstants.com" + m.group(2),
                    "url": "https://www.myinstants.com" + m.group(1), "id": m.group(2).rstrip("/").split("/")[-1]})
    return out


def allowed(title: str, kind: str) -> bool:
    return not POLITICS.search(title) and not UNSAFE.search(title) \
        and (kind == "image" or not (INDIAN.search(title) or HINGLISH.search(title)))


def search(query: str, kind: str, n: int = 8) -> list[dict]:
    got = _myinstants(query) if kind == "sound" else _imgflip(query, kind == "video")
    return [g for g in got if allowed(g["title"], kind)][:n]


def _templates(sort: str) -> list[dict]:
    t = _get("https://imgflip.com/memetemplates", params={"sort": sort}).text
    out = {}       # id from the thumbnail (base-36) — named classics link /meme/Drake-Hotline-Bling, no number
    for m in re.finditer(r'<a title="([^"]+)" href="/meme/[^"]+">\s*<img class="shadow"[^>]*src="//i\.imgflip\.com/\d/(\w+)\.', t):
        title = html.unescape(m.group(1)).removesuffix(" Meme")
        out.setdefault(norm_title(title), {"title": title, "id": str(int(m.group(2), 36))})
    return list(out.values())


def _sounds_trending() -> list[dict]:
    out = []
    for u in ("https://www.myinstants.com/en/trending/", "https://www.myinstants.com/en/index/us/"):
        t = _get(u).text
        out += [{"title": html.unescape(x).strip()} for x in re.findall(r'class="instant-link link-secondary">([^<]+)<', t)]
    return list({x["title"].lower(): x for x in out}.values())


def lists() -> dict:
    """Today's hot lists (cached a day): new = imgflip's newest rising templates, best = most captioned in the
    last 30 days (still everywhere), sound = myinstants trending (global + US)."""
    cache = json.loads(TREND.read_text()) if TREND.exists() else {}
    if cache.get("date") != time.strftime("%Y-%m-%d"):
        cache = {"date": time.strftime("%Y-%m-%d"), "new": _templates("top-new"), "best": _templates("top-30-days")[:40],
                 "sound": [x for x in _sounds_trending() if allowed(x["title"], "sound")]}
        TREND.parent.mkdir(exist_ok=True)
        TREND.write_text(json.dumps(cache, indent=1, ensure_ascii=False))
    return cache


def year_of(tid: str | int) -> float:
    """Upload date of an imgflip template from its id (≈ ±3 months)."""
    tid = int(tid) if str(tid).isdigit() else int(str(tid), 36)
    now_id = max([int(x["id"]) for x in lists()["new"]] or [ANCHORS[-1][0]])
    t = time.localtime()
    pts = ANCHORS + [(now_id, t.tm_year + (t.tm_mon - 1) / 12)]
    for (i0, y0), (i1, y1) in zip(pts, pts[1:]):
        if tid <= i1 or (i1, y1) == pts[-1]:
            return y0 + (tid - i0) * (y1 - y0) / (i1 - i0)
    return pts[0][1]


def months_old(tid) -> int:
    t = time.localtime()
    return max(0, round((t.tm_year + (t.tm_mon - 1) / 12 - year_of(tid)) * 12))


def norm_title(t: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", t.lower()).strip()


def culture_rows(ep) -> dict[str, str]:
    """facts.md `## Culture now` → {"M1": exact title} (what a script's `{meme: M1}` means)."""
    p = ep.dir / "facts.md"
    txt = p.read_text() if p.exists() else ""
    m = re.search(r"^## Culture now.*?$(.*?)(?=^## |\Z)", txt, re.S | re.M)
    out = {}
    for row in (m.group(1).splitlines() if m else []):
        r = re.match(r"\s*-\s*(M\d+)\s*·\s*(image|video|sound|ref)\s*·\s*\"([^\"]+)\"", row)
        if r:
            out[r.group(1).upper()] = r.group(3)
    return out


def culture_now(ep) -> dict[str, str]:
    """facts.md `## Culture now` rows → {normalised exact title: kind}. Row: `- M1 · image · "Title" · why · date · url`."""
    p = ep.dir / "facts.md"
    txt = p.read_text() if p.exists() else ""
    m = re.search(r"^## Culture now.*?$(.*?)(?=^## |\Z)", txt, re.S | re.M)
    out = {}
    for row in (m.group(1).splitlines() if m else []):
        r = re.match(r"\s*-\s*(M\d+)\s*·\s*(image|video|sound|ref)\s*·\s*\"([^\"]+)\"", row)
        if r:
            out[norm_title(r.group(3))] = r.group(2)
    return out


RECENT_REELS = 4               # a meme used in any of the last 4 reels is off-limits — followers notice repeats


def _born(d: Path) -> float:
    """When an episode was started: its first agent run (usage.jsonl), else facts.md's mtime."""
    u = d / "notes" / "usage.jsonl"
    try:
        first = json.loads(u.read_text().splitlines()[0])["at"]
        return time.mktime(time.strptime(first[:19], "%Y-%m-%dT%H:%M:%S"))
    except Exception:
        f = d / "facts.md"
        return f.stat().st_mtime if f.exists() else 0.0


def recent_use(ep_dir, n: int = RECENT_REELS) -> dict[str, str]:
    """{normalised meme title/query: episode} for every meme in the n reels started before this one."""
    here = Path(ep_dir).resolve()
    born = _born(here)
    others = [p.parent.parent for p in (ROOT / "episodes").glob("*/scenes/scenes.json")
              if p.parent.parent.resolve() != here and not p.parent.parent.name.startswith("_")]
    others = sorted((d for d in others if _born(d) < born), key=_born, reverse=True)[:n]
    out: dict[str, str] = {}
    for d in others:
        try:
            plan = json.loads((d / "scenes" / "scenes.json").read_text())
        except (OSError, json.JSONDecodeError):
            continue
        used = wanted(plan)
        try:                                                  # the fetched titles, when a query differed
            man = json.loads((d / ".cache" / "memes" / "memes.json").read_text())
        except (OSError, json.JSONDecodeError):
            man = {}
        for kind, q, pick in used:
            out.setdefault(norm_title(q), d.name)
            out.setdefault(norm_title((man.get(key(kind, q, pick)) or {}).get("title", "")), d.name)
    out.pop("", None)
    return out


def freshness(title: str, kind: str, tid: str | None, ep) -> tuple[str, str]:
    """('now' | 'classic' | 'stale', why). now = this week (trending new / sound trending / Culture now)."""
    L, cn, n = lists(), culture_now(ep), norm_title(title)
    if n in cn:
        return "now", "facts.md Culture now"
    if kind == "sound":
        return ("now", "myinstants trending") if any(norm_title(x["title"]) == n for x in L["sound"]) else \
            ("stale", "not in myinstants trending or Culture now")
    if any(norm_title(x["title"]) == n for x in L["new"]):
        return "now", "imgflip new & rising"
    if any(norm_title(x["title"]) == n for x in L["best"]):
        age = months_old(tid)
        return "classic", f"imgflip top-30-days, template ≈ {age} months old"
    age = months_old(tid) if tid else 999
    return "stale", f"not trending today (template ≈ {age} months old) — not in Culture now"


def trending(kind: str = "image", n: int = 30) -> list[str]:
    L = lists()
    if kind == "sound":
        return [x["title"] for x in L["sound"]][:n]
    rows = [(x, "new") for x in L["new"]] + [(x, "classic") for x in L["best"]]
    return [f"{x['title']}  ({tag}, ≈ {months_old(x['id'])} mo)" for x, tag in rows
            if allowed(x["title"], kind)][:n]


# ------------------------------------------------------------------ fetch
def _ff(*a: str) -> None:
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *a], check=True)


def _probe(p: Path) -> dict:
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                        "-show_entries", "format=duration", "-of", "json", str(p)], capture_output=True, text=True)
    d = json.loads(r.stdout or "{}")
    st = (d.get("streams") or [{}])[0]
    return {"w": st.get("width"), "h": st.get("height"), "dur": float(d.get("format", {}).get("duration") or 0)}


def _sprite(mp4: Path, dest: Path) -> dict:
    info = _probe(mp4)
    frames = max(1, min(MAX_FRAMES, math.floor(info["dur"] * FPS)))
    cols = min(COLS, frames)
    rows = math.ceil(frames / cols)
    fh = round(SPRITE_W * info["h"] / info["w"] / 2) * 2
    _ff("-i", str(mp4), "-vf", f"fps={FPS},scale={SPRITE_W}:{fh},tile={cols}x{rows}", "-frames:v", "1",
        "-q:v", "3", str(dest))
    return {"w": SPRITE_W, "h": fh, "frames": frames, "cols": cols, "rows": rows, "fps": FPS}


def _download(url: str, dest: Path) -> None:
    dest.write_bytes(_get(url, timeout=90).content)


def _log(kind: str, hit: dict, file: Path, query: str) -> None:
    c = Candidate(source={"sound": "myinstants"}.get(kind, "imgflip"), source_id=hit["id"], title=hit["title"],
                  kind={"sound": "sfx"}.get(kind, kind), page_url=hit["page"], download_url=hit["url"],
                  license_name=LICENSE, license_url="", attribution_required=False)
    licenses.check_policy(c)
    snap = licenses.save_snapshot(c, f"No license. Meme used under the creator's approval (CLAUDE.md §6): "
                                     f"global meme, uncleared. Query '{query}'. Swap it if a rights holder objects.")
    licenses.record(c, file, snap, status="meme", basis="meme (uncleared)")


def key(kind: str, query: str, pick: int) -> str:
    return f"{kind}:{query.strip().lower()}:{pick}"


def ensure(ep_dir: str, want: list[tuple[str, str, int]]) -> tuple[dict, list[str]]:
    """Download what's missing. want = [(kind, query, pick)] → ({key: entry}, errors)."""
    ep = load(ep_dir)
    d = ep.cache / "memes"
    d.mkdir(parents=True, exist_ok=True)
    man_p = d / "memes.json"
    man = json.loads(man_p.read_text()) if man_p.exists() else {}
    errors = []
    for kind, query, pick in want:
        k = key(kind, query, pick)
        e = man.get(k)
        if e and (d / e["file"]).exists():
            continue
        try:
            hit = None
            if e:                                   # same source file as last build (manifest url)
                hit = e["hit"]
            else:
                hits = search(query, kind, pick + 1)
                if len(hits) <= pick:
                    errors.append(f"meme {kind} '{query}': {len(hits)} global result(s), pick {pick} — try "
                                  f"`memes.py search \"{query}\" --kind {kind}`")
                    continue
                hit = hits[pick]
            stem = f"{kind}-{slug(hit['title'], 32)}-{hit['id'][:12]}"
            f = None
            if kind == "image":                     # user-uploaded templates are often .png; some are animated (.mp4)
                for ext in ("jpg", "png"):
                    try:
                        f = d / f"{stem}.{ext}"
                        _download(hit["url"].rsplit(".", 1)[0] + "." + ext, f)
                        meta = _probe(f)
                        break
                    except Exception:
                        f = None
                if f is None:
                    hit = {**hit, "url": hit["url"].rsplit(".", 1)[0] + ".mp4"}
            if kind == "video" or (kind == "image" and f is None):
                raw = d / f"{stem}.mp4"
                _download(hit["url"], raw)
                f = d / f"{stem}.sprite.jpg"
                meta = {**_sprite(raw, f), "src_dur": _probe(raw)["dur"], "as": "video"}
            elif kind == "sound":
                raw = d / f"{stem}.src.mp3"
                _download(hit["url"], raw)
                f = d / f"{stem}.wav"
                _ff("-i", str(raw), "-af", f"silenceremove=start_periods=1:start_threshold=-50dB,atrim=0:{SOUND_MAX_S}",
                    "-ar", "48000", "-ac", "2", str(f))
                meta = {"dur": _probe(f)["dur"]}
            _log(kind, hit, f, query)
            man[k] = {"file": f.name, "title": hit["title"], "page": hit["page"], "hit": hit, **meta}
            print(f"  ✓ meme {kind:5s} '{query}' → {hit['title']} ({f.name})")
        except Exception as ex:                     # a dead link must not kill validation
            errors.append(f"meme {kind} '{query}': {ex}")
    man_p.write_text(json.dumps(man, indent=1, ensure_ascii=False))
    return {k: {**v, "path": str(d / v["file"])} for k, v in man.items()}, errors


def wanted(plan: dict) -> list[tuple[str, str, int]]:
    out = []
    for s in plan.get("scenes", []):
        if s.get("component") not in ("meme", "mascot-reaction"):   # mascot-reaction: optional meme sound only
            continue
        p = s.get("params", {})
        if s.get("component") == "meme" and p.get("meme"):
            out.append((p.get("kind", "image"), p["meme"], int(p.get("pick", 0))))
        if p.get("sound"):
            out.append(("sound", p["sound"], int(p.get("soundPick", 0))))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search")
    s.add_argument("query")
    s.add_argument("--kind", choices=["image", "video", "sound"], default="image")
    s.add_argument("-n", type=int, default=8)
    tr = sub.add_parser("trending")
    tr.add_argument("--kind", choices=["image", "video", "sound"], default="image")
    tr.add_argument("-n", type=int, default=40)
    tr.add_argument("--episode", help="mark (and drop) memes used in the last few reels before this one")
    f = sub.add_parser("fetch")
    f.add_argument("episode")
    a = ap.parse_args()
    if a.cmd == "search":
        for i, h in enumerate(search(a.query, a.kind, a.n)):
            age = f"  · template ≈ {months_old(h['tid'])} mo" if h.get("tid") else ""
            print(f"  pick {i}: {h['title']}{age}")
        return 0
    if a.cmd == "trending":
        recent = recent_use(a.episode) if a.episode else {}
        for t in trending(a.kind, a.n):
            if norm_title(t.rsplit("  (", 1)[0]) not in recent:
                print(f"  {t}")
        if recent:
            print(f"  (left out — used in the last {RECENT_REELS} reels: "
                  + "; ".join(f"{k} [{v}]" for k, v in sorted(recent.items())) + ")")
        print("  (Indian + this week's: facts.md '## Culture now', from the researcher)")
        return 0
    ep = load(a.episode)
    plan = json.loads((ep.dir / "scenes" / "scenes.json").read_text())
    _, errs = ensure(a.episode, wanted(plan))
    for e in errs:
        print(f"  ✗ {e}")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
