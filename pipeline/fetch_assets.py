#!/usr/bin/env python3
"""Find, license-check, download and log assets. Allowed sources only.

  fetch_assets.py search "<query>" --kind sfx|music|image|video|icon [--source freesound,...]
  fetch_assets.py get "<query>" --kind sfx -n 2 [--dest episodes/<ep>/assets] [--source ...]
  fetch_assets.py starter-kit            # 3 options per signature SFX + 5 lo-fi tracks -> audition page
  fetch_assets.py audition               # rebuild brand/_audition/index.html
  fetch_assets.py lock stamp=2 coin=1 music=1,4 ...
  fetch_assets.py ingest <file> --url <source page> --source mixkit|pixabay --kind sfx
  fetch_assets.py prune                  # drop ledger rows whose files are gone
  fetch_assets.py foley cough "man cough" # one-off action sound, first hit only -> brand/sfx/cough.wav

Every download: license re-checked on the source at download time, refused unless on the
allow-list, logged in assets/licenses.json with a saved snapshot.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib import licenses  # noqa: E402
from lib.common import BRAND, ROOT, Candidate, slug  # noqa: E402
from lib.sources import freesound, icons, kenney, mixkit, pexels, pixabay  # noqa: E402

SOURCES = {"freesound": freesound, "mixkit": mixkit, "pixabay": pixabay, "kenney": kenney,
           "pexels": pexels, "lucide": icons, "tabler": icons, "noto": icons}
DEFAULT_ORDER = {
    "sfx": ["freesound", "mixkit", "pixabay", "kenney"],
    "music": ["pixabay", "mixkit", "freesound"],
    "image": ["pixabay", "pexels"],
    "video": ["pixabay", "pexels"],
    "icon": ["lucide"],
}
AUDITION = BRAND / "_audition"

# Signature + accent SFX. trim = max length kept when locking (seconds).
SLOTS = {
    "stamp":   {"queries": ["rubber stamp", "stamp"], "max_dur": 3, "trim": 1.2},
    "printer": {"queries": ["receipt printer", "dot matrix printer", "printer"], "max_dur": 8, "trim": 2.5},
    "ding":    {"queries": ["cash register", "cash register bell", "register"], "max_dur": 5, "trim": 2.0},
    "coin":    {"queries": ["coin clink", "coins", "coin"], "max_dur": 3, "trim": 1.0},
    "scratch": {"queries": ["record scratch", "vinyl scratch", "scratch"], "max_dur": 3, "trim": 0.5},  # the hit; 1.2 s ran over the next words
    "glitch":  {"queries": ["glitch", "digital glitch"], "max_dur": 2.5, "trim": 0.9},
    "typing":  {"queries": ["keyboard typing", "typing"], "max_dur": 10, "trim": 3.0},
    "whoosh":  {"queries": ["whoosh", "swoosh"], "max_dur": 2.5, "trim": 1.0},
}
MUSIC = {"queries": ["lofi tabla", "indian lofi", "lofi chill", "lo-fi beats", "lofi"], "min_dur": 60, "n": 5}


# --------------------------------------------------------------------------- core
def search(query: str, kind: str, n: int, sources: list[str] | None = None, **kw) -> list[Candidate]:
    out: list[Candidate] = []
    for name in sources or DEFAULT_ORDER[kind]:
        try:
            kwargs = dict(kw)
            if name in ("lucide", "tabler", "noto"):
                kwargs["icon_set"] = name
            got = SOURCES[name].search(query, kind=kind, n=n, **kwargs)
            out.extend(got)
        except Exception as e:  # one broken source must not kill the run
            print(f"  ! {name}: {e}")
    return out


def fetch(c: Candidate, dest_stem: Path, **ledger_extra) -> Path | None:
    """License-check on the source page right now, download, log. Returns file or None."""
    try:
        licenses.check_policy(c)
        snapshot_text = SOURCES[c.source].verify(c)
        snap = licenses.save_snapshot(c, snapshot_text)
        dest_stem.parent.mkdir(parents=True, exist_ok=True)
        path = SOURCES[c.source].download(c, dest_stem)
        licenses.record(c, path, snap, **ledger_extra)
        print(f"  ✓ {c.key:28s} {c.license_name:34s} -> {path.relative_to(ROOT)}")
        return path
    except licenses.LicenseRefused as e:
        print(f"  ✗ refused {e}")
    except Exception as e:
        print(f"  ✗ {c.key}: {e}")
    return None


def duration_of(path: Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                        "default=nw=1:nk=1", str(path)], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


def waveform(path: Path) -> Path:
    png = path.with_suffix(".wave.png")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(path), "-filter_complex",
                    "aformat=channel_layouts=mono,showwavespic=s=640x90:colors=#141414:scale=sqrt",
                    "-frames:v", "1", str(png)], check=False)
    return png


def _diverse(cands: list[Candidate], n: int, exclude: set[str]) -> list[Candidate]:
    """Round-robin across sources; skip Pixabay mirrors of Freesound sounds."""
    by_src: dict[str, list[Candidate]] = {}
    for c in cands:
        if c.key in exclude or c.extra.get("mirror_of_freesound"):
            continue
        by_src.setdefault(c.source, []).append(c)
    picked: list[Candidate] = []
    while len(picked) < n and any(by_src.values()):
        for src in list(by_src):
            if by_src[src] and len(picked) < n:
                picked.append(by_src[src].pop(0))
    return picked


# --------------------------------------------------------------------------- starter kit
def starter_kit(only: list[str] | None = None) -> None:
    files_dir = AUDITION / "files"
    slots = {k: v for k, v in SLOTS.items() if not only or k in only}
    for slot, spec in slots.items():
        print(f"\n▶ {slot}")
        have = sorted(p for p in (files_dir / slot).glob("*.*") if not p.name.endswith(".png")) \
            if (files_dir / slot).exists() else []
        if len(have) >= 3:
            print("  already have 3 options")
            continue
        # keys already downloaded for this slot (so a resumed run never duplicates)
        done = {f"{e['source']}:{e['source_id']}" for e in licenses.load() if e.get("slot") == slot}
        idx = len(have) + 1
        for q in spec["queries"]:
            if idx > 3:
                break
            cands = search(q, "sfx", 4, max_dur=spec["max_dur"])
            for c in _diverse(cands, 3 - idx + 1, done):
                done.add(c.key)
                p = fetch(c, files_dir / slot / f"{idx}-{c.source}-{slug(c.title, 30)}",
                          status="audition", slot=slot)
                if p:
                    waveform(p)
                    idx += 1
                if idx > 3:
                    break
    if not only or "music" in only:
        print("\n▶ music")
        mdir = files_dir / "music"
        idx = len([p for p in mdir.glob("*") if not p.name.endswith(".png")]) + 1 if mdir.exists() else 1
        done = {f"{e['source']}:{e['source_id']}" for e in licenses.load() if e.get("slot") == "music"}
        for q in MUSIC["queries"]:
            if idx > MUSIC["n"]:
                break
            for c in _diverse(search(q, "music", 3, min_dur=MUSIC["min_dur"]), 2, done):
                done.add(c.key)
                p = fetch(c, mdir / f"{idx}-{c.source}-{slug(c.title, 30)}", status="audition", slot="music")
                if p:
                    waveform(p)
                    idx += 1
                if idx > MUSIC["n"]:
                    break
    build_audition()


def build_audition() -> Path:
    files_dir = AUDITION / "files"
    ledger = {e["file"]: e for e in licenses.load()}
    sections = []
    for slot in list(SLOTS) + ["music"]:
        d = files_dir / slot
        if not d.exists():
            continue
        rows = []
        for f in sorted(p for p in d.iterdir() if not p.name.endswith(".png")):
            e = ledger.get(str(f.relative_to(ROOT)), {})
            n = f.name.split("-")[0]
            wave = f.with_suffix(".wave.png")
            rows.append(f"""
      <div class="opt chillar-card">
        <div class="num t-mono">{html.escape(n)}</div>
        <div class="meta">
          <div class="t-body title">{html.escape(e.get('name', f.stem))}</div>
          <div class="t-sub small">{html.escape(e.get('source', '?'))} · {html.escape(e.get('license', '?'))}
            · <span class="t-mono">{duration_of(f):.1f}s</span>
            · <a href="{html.escape(e.get('url', '#'))}" target="_blank">source</a></div>
          {'<img src="files/' + html.escape(slot + '/' + wave.name) + '" alt="">' if wave.exists() else ''}
          <audio controls preload="none" src="files/{html.escape(slot + '/' + f.name)}"></audio>
        </div>
      </div>""")
        trim = SLOTS.get(slot, {}).get("trim")
        sections.append(f"""
    <section>
      <h2 class="t-head">{slot}{' <span class="t-sub small">(trimmed to ' + str(trim) + 's on lock)</span>' if trim else ''}</h2>
      {''.join(rows) or '<p class="t-sub">no options found</p>'}
    </section>""")
    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Chillar sound audition</title>
<link rel="stylesheet" href="../colors.css">
<style>
  body {{ margin:0; font-family: var(--font-body); color: var(--ink); }}
  main {{ max-width: 860px; margin: 0 auto; padding: 32px 16px 80px; }}
  h1 {{ font-size: 56px; margin: 0 0 8px; }} h2 {{ font-size: 34px; margin: 36px 0 12px; }}
  .opt {{ display:flex; gap:16px; padding:14px 16px; margin: 0 0 14px; }}
  .num {{ font-size: 40px; width: 40px; }}
  .meta {{ flex:1; min-width:0; }} .title {{ font-size: 20px; }}
  .small {{ font-size: 14px; font-weight: 700; }}
  img {{ display:block; width:100%; max-width:640px; height:56px; object-fit:fill; margin:8px 0; }}
  audio {{ width:100%; }} a {{ color: var(--ink); }}
  code {{ font-family: var(--font-mono); background: var(--card); border: 2px solid var(--ink); padding: 2px 6px; }}
</style></head>
<body class="chillar-paper"><main>
  <h1 class="t-head">Sound audition</h1>
  <p class="t-body">Pick one per slot (two or more for music), then run:<br>
  <code>.venv/bin/python pipeline/fetch_assets.py lock stamp=1 printer=2 ding=1 coin=3 scratch=1 glitch=2 typing=1 whoosh=1 music=1,3</code></p>
  <p class="t-sub small">Files in brand/sfx/custom/&lt;slot&gt;.* always override the locked pick.</p>
  {''.join(sections)}
</main></body></html>"""
    out = AUDITION / "index.html"
    out.write_text(page)
    print(f"\naudition page: {out}")
    return out


# --------------------------------------------------------------------------- lock
def _peak_db(path: Path) -> float:
    r = subprocess.run(["ffmpeg", "-v", "info", "-i", str(path), "-af", "volumedetect", "-f", "null", "-"],
                       capture_output=True, text=True)
    for line in r.stderr.splitlines():
        if "max_volume" in line:
            return float(line.split(":")[1].replace("dB", ""))
    return 0.0


def lock(picks: list[str]) -> None:
    files_dir = AUDITION / "files"
    for p in picks:
        slot, _, nums = p.partition("=")
        for i, n in enumerate(nums.split(",")):
            src = next((f for f in (files_dir / slot).glob(f"{n}-*") if not f.name.endswith(".png")), None)
            if not src:
                print(f"  ✗ {slot}={n}: no such option")
                continue
            e = licenses.entry_for(src)
            if not e:
                print(f"  ✗ {src.name}: not in licenses.json — refusing to lock an unlogged file")
                continue
            if slot == "music":
                dest = BRAND / "music" / f"{i + 1:02d}-{slug(e['name'], 30)}.mp3"
                af = "loudnorm=I=-16:TP=-1.5:LRA=11"
                codec = ["-c:a", "libmp3lame", "-b:a", "320k"]
            else:
                trim = SLOTS[slot]["trim"]
                dest = BRAND / "sfx" / f"{slot}.wav"
                gain = -2.0 - _peak_db(src)
                af = (f"silenceremove=start_periods=1:start_threshold=-50dB,atrim=0:{trim},"
                      f"afade=t=out:st={max(trim - 0.15, 0)}:d=0.15,volume={gain:.2f}dB")
                codec = ["-c:a", "pcm_s16le"]
            dest.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-af", af, "-ar", "48000",
                            "-ac", "2", *codec, str(dest)], check=True)
            c = Candidate(e["source"], e["source_id"], e["name"], e["kind"], e["url"], e["download_url"],
                          e["license"], e["license_url"], e["attribution_needed"] == "y", e.get("author", ""),
                          extra={"attribution": e.get("attribution_text", "")})
            licenses.record(c, dest, e["license_snapshot"], status="locked", slot=slot,
                            derived_from=e["file"], processing=af)
            print(f"  ✓ locked {slot}: {src.name} -> {dest.relative_to(ROOT)}")


# --------------------------------------------------------------------------- foley
def _first_hit(path: Path, max_len: float) -> tuple[float, float]:
    """(start, end) of the first sound burst: one cough, one knock — not the whole take."""
    r = subprocess.run(["ffmpeg", "-v", "info", "-i", str(path), "-af", "silencedetect=n=-35dB:d=0.12", "-f", "null", "-"],
                       capture_output=True, text=True)
    marks = [(k, float(v)) for k, v in re.findall(r"silence_(start|end): ([\d.]+)", r.stderr)]
    start = next((v for k, v in marks if k == "end"), 0.0) if marks and marks[0] == ("start", 0.0) else 0.0
    end = next((v for k, v in marks if k == "start" and v > start + 0.05), start + max_len)
    return max(0.0, start - 0.02), min(end + 0.06, start + max_len)


def foley(name: str, query: str, max_len: float = 0.8, pick: int = 0) -> Path | None:
    """One-off sound for a described action in a script line ("Star khansa" → cough) → brand/sfx/<name>.wav.
    Fetched from the allowed sources (license re-checked, logged), cut to its first hit, peak −2 dB."""
    if name in SLOTS:
        sys.exit(f"'{name}' is a signature slot — use starter-kit/lock for it")
    dest = BRAND / "sfx" / f"{name}.wav"
    if dest.exists():
        print(f"  = {dest.relative_to(ROOT)} already exists (delete it to fetch another)")
        return dest
    cands = search(query, "sfx", 6, max_dur=10)
    for c in cands[pick:]:
        src = fetch(c, ROOT / "assets" / "downloads" / "foley" / f"{c.source}-{slug(c.title, 30)}-{slug(c.source_id, 12)}")
        if not src:
            continue
        a, b = _first_hit(src, max_len)
        if b - a < 0.08:
            continue
        gain = -2.0 - _peak_db(src)
        af = (f"atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.01,"
              f"afade=t=out:st={max(b - a - 0.08, 0):.3f}:d=0.08,volume={gain:.2f}dB")
        dest.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-af", af, "-ar", "48000", "-ac", "2",
                        "-c:a", "pcm_s16le", str(dest)], check=True)
        e = licenses.entry_for(src)
        licenses.record(c, dest, e["license_snapshot"] if e else "", status="locked", slot=f"foley:{name}",
                        derived_from=str(src.relative_to(ROOT)), processing=af)
        print(f"  ✓ foley {name}: {b - a:.2f}s from {c.key} -> {dest.relative_to(ROOT)}  (use \"sfx\": "
              f"[{{\"sound\": \"{name}\", \"at\": …}}] on the scene)")
        return dest
    print(f"  ✗ no usable CC0 hit for '{query}' — try other words")
    return None


# --------------------------------------------------------------------------- ingest / prune
def ingest(file: Path, url: str, source: str, kind: str) -> None:
    """Log a file you downloaded by hand. The license is re-checked on the source page."""
    if source == "pixabay":
        sid = url.rstrip("/").split("-")[-1]
        c = Candidate("pixabay", sid, file.stem, kind, url, url, pixabay.LICENSE, pixabay.LICENSE_URL, False)
    elif source == "mixkit":
        name, lic_url, _ = mixkit.LIC["music" if kind == "music" else "sfx"]
        c = Candidate("mixkit", file.stem, file.stem, kind, url, url, name, lic_url, False, "Mixkit")
    else:
        sys.exit("ingest supports --source pixabay|mixkit (others have APIs: use `get`)")
    licenses.check_policy(c)
    snap = licenses.save_snapshot(c, SOURCES[source].verify(c))
    dest = ROOT / "assets" / "ingested" / file.name
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(file, dest)
    licenses.record(c, dest, snap, status="ingested")
    print(f"  ✓ ingested {dest.relative_to(ROOT)}")


def prune() -> None:
    entries = licenses.load()
    keep = [e for e in entries if (ROOT / e["file"]).exists()]
    licenses.save(keep)
    print(f"pruned {len(entries) - len(keep)} rows; {len(keep)} remain")


# --------------------------------------------------------------------------- cli
def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("search", "get"):
        s = sub.add_parser(name)
        s.add_argument("query")
        s.add_argument("--kind", default="sfx", choices=list(DEFAULT_ORDER))
        s.add_argument("--source", help="comma list: " + ",".join(SOURCES))
        s.add_argument("-n", type=int, default=3)
        s.add_argument("--max-dur", type=float)
        s.add_argument("--min-dur", type=float)
        if name == "get":
            s.add_argument("--dest", default="assets/downloads", help="folder (repo-relative)")
    k = sub.add_parser("starter-kit")
    k.add_argument("--only", help="comma list of slots (and/or 'music')")
    sub.add_parser("audition")
    lk = sub.add_parser("lock")
    lk.add_argument("picks", nargs="+")
    ing = sub.add_parser("ingest")
    ing.add_argument("file", type=Path)
    ing.add_argument("--url", required=True)
    ing.add_argument("--source", required=True)
    ing.add_argument("--kind", default="sfx")
    sub.add_parser("prune")
    fo = sub.add_parser("foley", help="one-off action sound -> brand/sfx/<name>.wav (cut to its first hit)")
    fo.add_argument("name")
    fo.add_argument("query")
    fo.add_argument("--max-len", type=float, default=0.8)
    fo.add_argument("--pick", type=int, default=0, help="skip the first N candidates (a different take)")
    a = ap.parse_args()

    if a.cmd in ("search", "get"):
        srcs = a.source.split(",") if a.source else None
        kw = {k: v for k, v in (("max_dur", a.max_dur), ("min_dur", a.min_dur)) if v}
        cands = search(a.query, a.kind, a.n, srcs, **kw)
        if a.cmd == "search":
            for c in cands:
                d = f"{c.duration:.1f}s" if c.duration else ""
                print(f"{c.key:30s} {d:>7s}  {c.license_name:34s} {c.title[:50]}  {c.page_url}")
        else:
            for c in cands[: a.n]:
                fetch(c, ROOT / a.dest / f"{c.source}-{slug(c.title, 30)}-{slug(c.source_id, 12)}")
    elif a.cmd == "starter-kit":
        starter_kit(a.only.split(",") if a.only else None)
    elif a.cmd == "audition":
        build_audition()
    elif a.cmd == "lock":
        lock(a.picks)
    elif a.cmd == "ingest":
        ingest(a.file, a.url, a.source, a.kind)
    elif a.cmd == "foley":
        foley(a.name, a.query, a.max_len, a.pick)
    elif a.cmd == "prune":
        prune()


if __name__ == "__main__":
    main()
