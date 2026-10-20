#!/usr/bin/env python3
"""AI voiceover from the script (for drafts, timing tests or fully AI-voiced reels).

  tts.py episodes/<ep>                         -> voice/voice.wav  (+ voice/voice.json provenance)
  tts.py episodes/<ep> --audition a,b,c        -> voice/audition/<speaker>.wav (pick by ear)
  tts.py episodes/<ep> --provider kokoro       -> local Kokoro (offline test voice, poor Hinglish)
  tts.py episodes/<ep> --probe                 -> .cache/probe.wav: real Sunny length of script.md before the
                                                  voice stage (Roman text; for timing only, never the voiceover)

Text: voice/tts.txt if present, else the spoken lines of script.md.
Sarvam quality drops a lot on romanised Hindi: tts.txt should have Hindi words in Devanagari
and English words in Latin ("UPI free है। फिर bill कौन भरता है?"). /voiceover writes it for you.
Captions and alignment still use the Roman script.md — only the voice reads tts.txt.

Settings ([tts] in episode.toml): provider, model, speaker, pace, temperature, language, per_line.

Direction tags in tts.txt (comic timing; stripped before anything is sent, never spoken):
  {beat} / {beat:0.6}   a pause of 0.45 s (or the given seconds, 0.15–1.2) at that spot — before a
                        punchline, mid-line or at the start of a line
  {slow} / {fast}       this line at 0.9× / 1.1× the channel pace (a stamped number, a rushed aside)
Each line is its own request (Sarvam bills characters, so the cost is the same) and is cached in
.cache/tts_takes/ by text + settings: a re-run pays only for lines whose text changed.
  tts.py episodes/<ep> --retake L6,L8          -> re-roll only those lines (same text, a new take)
voice.json records the beats so audio_clean keeps them (it caps every other pause at max_gap_s).
"""
from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import io
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.common import ROOT, env, session  # noqa: E402
from lib.episode import load  # noqa: E402

SARVAM_URL = "https://api.sarvam.ai/text-to-speech"
DEFAULTS = {"provider": "sarvam", "model": "bulbul:v4-flash", "speaker": "sunny_hi_reels",
            "pace": 1.2, "temperature": 0.6, "language": "hi-IN"}
MAX_CHARS = 2400  # API limit is 2500 for v3 / v4-flash
TAG = re.compile(r"\{\s*(beat|slow|fast)(?:\s*:\s*([\d.]+))?\s*\}")
BEAT_S, BEAT_MIN, BEAT_MAX = 0.45, 0.15, 1.2
PACE_TAG = {"slow": 0.9, "fast": 1.1}   # × the channel pace — the channel pace itself never changes
LINE_GAP = 0.25    # between untagged lines (under audio_clean's 0.28 s cap, so it survives as is)
EDGE = 0.03        # silence kept at each end of a take before the gap is added


LEXICON = ROOT / "brand" / "pronunciations.tsv"
_WORD = r"\wऀ-ॿ"            # Devanagari matras aren't \w — count them as part of a word


def lexicon() -> list[tuple[str, str]]:
    rows = []
    for line in (LEXICON.read_text().splitlines() if LEXICON.exists() else []):
        if line.strip() and not line.startswith("#"):
            cells = line.split("\t")
            if len(cells) >= 2 and cells[0].strip() and cells[1].strip():
                rows.append((cells[0].strip(), cells[1].strip()))
    return rows


def respell(text: str) -> tuple[str, list[str]]:
    """Apply brand/pronunciations.tsv (whole words). Returns (text, ['खाँसा→खान्सा', …])."""
    hits = []
    for w, s in lexicon():
        new, n = re.subn(rf"(?<![{_WORD}]){re.escape(w)}(?![{_WORD}])", s, text)
        if n:
            text = new
            hits.append(f"{w}→{s}")
    return text, hits


def strip_tags(line: str) -> str:
    """The words of a tts.txt line without its direction tags (what voice_check compares)."""
    return re.sub(r"\s{2,}", " ", TAG.sub(" ", line)).strip()


@dataclass
class Seg:
    line: int          # 0-based index of the spoken line (= script.md line order)
    text: str
    pace: float        # multiplier on the channel pace
    beat: float        # seconds of pause before this segment (0 = the natural line gap)


def direction(text: str) -> list[Seg]:
    """tts.txt -> segments. A tag-only line gives its beat to the next line; an unknown {tag} is an error
    (it would be read aloud)."""
    segs, n, pending = [], 0, 0.0
    for raw in text.splitlines():
        if not strip_tags(raw):
            pending = max(pending, sum(_beat(m) for m in TAG.finditer(raw)))
            continue
        left = TAG.sub("", raw)
        if "{" in left or "}" in left:
            sys.exit(f"tts.txt: unknown direction tag in “{raw.strip()}” — use {{beat}}, {{beat:0.6}}, {{slow}} or {{fast}}")
        pace = 1.0
        for m in TAG.finditer(raw):
            if m.group(1) in PACE_TAG:
                pace = PACE_TAG[m.group(1)]
        pos, beat = 0, pending
        for m in list(TAG.finditer(raw)) + [None]:
            piece = strip_tags(raw[pos:m.start() if m else len(raw)])
            if piece:
                segs.append(Seg(n, piece, pace, beat))
                beat = 0.0
            if m is None:
                break
            if m.group(1) == "beat":
                beat = max(beat, _beat(m))
            pos = m.end()
        pending = beat                     # a trailing {beat} pauses before the next line
        n += 1
    return segs


def _beat(m: re.Match) -> float:
    if m.group(1) != "beat":
        return 0.0
    return min(max(float(m.group(2)) if m.group(2) else BEAT_S, BEAT_MIN), BEAT_MAX)


def tts_text(ep) -> tuple[str, bool]:
    p = ep.dir / "voice" / "tts.txt"
    if p.exists():
        return p.read_text().strip(), True
    return ep.spoken_text, False


def chunks(text: str) -> list[str]:
    out, cur = [], ""
    for line in text.splitlines():
        if len(cur) + len(line) + 1 > MAX_CHARS and cur:
            out.append(cur)
            cur = ""
        cur = (cur + "\n" + line).strip()
    if cur:
        out.append(cur)
    return out


def sarvam_request(text: str, cfg: dict, pace: float) -> bytes:
    key = env("SARVAM_API_KEY")
    if not key:
        sys.exit("SARVAM_API_KEY missing in .env")
    body = {"text": text, "language_code": cfg["language"], "model": cfg["model"],
            "speaker": cfg["speaker"], "pace": round(pace, 3),
            "temperature": float(cfg["temperature"]), "speech_sample_rate": 48000,
            "output_audio_codec": "wav"}
    r = session.post(SARVAM_URL, json=body, headers={"api-subscription-key": key}, timeout=120)
    if r.status_code != 200:
        sys.exit(f"Sarvam {r.status_code}: {r.text[:400]}")
    return base64.b64decode(r.json()["audios"][0])


def sarvam(text: str, cfg: dict, dest: Path) -> dict:
    """One take of plain text in MAX_CHARS chunks (the --probe timing path)."""
    parts = []
    for i, chunk in enumerate(chunks(text)):
        p = dest.with_suffix(f".part{i}.wav")
        p.write_bytes(sarvam_request(chunk, cfg, float(cfg["pace"])))
        parts.append(p)
    concat(parts, dest)
    return {"request_chars": len(text)}


def groups(segs: list[Seg], per_line: bool) -> list[list[Seg]]:
    """Segments sent as one request. per_line (default): every segment alone, so each line is cached and
    re-taken on its own. Otherwise neighbours with the same pace and no beat between them share a request."""
    out: list[list[Seg]] = []
    for s in segs:
        g = out[-1] if out else None
        if (g and not per_line and not s.beat and s.pace == g[-1].pace
                and sum(len(x.text) + 1 for x in g) + len(s.text) <= MAX_CHARS):
            g.append(s)
        else:
            out.append([s])
    return out


def take_key(text: str, cfg: dict, pace: float) -> str:
    sig = json.dumps([text, cfg["model"], cfg["speaker"], round(pace, 3), float(cfg["temperature"]), cfg["language"]],
                     ensure_ascii=False)
    return hashlib.sha1(sig.encode()).hexdigest()[:16]


def trim(x, sr: int):
    """Cut a take's leading/trailing silence to EDGE so the gaps between takes are exactly what we set."""
    import numpy as np
    hop = int(sr * 0.01)
    n = len(x) // hop
    if n < 2:
        return x
    mono = x if x.ndim == 1 else x.mean(axis=1)
    db = 20 * np.log10(np.sqrt(np.mean(mono[: n * hop].reshape(n, hop) ** 2, axis=1)) + 1e-9)
    loud = np.flatnonzero(db > -45)
    if not len(loud):
        return x
    a = max(loud[0] * hop - int(EDGE * sr), 0)
    b = min((loud[-1] + 1) * hop + int(EDGE * sr), len(x))
    return x[a:b]


def sarvam_directed(text: str, cfg: dict, dest: Path, cache: Path, retake: set[int] = frozenset()) -> dict:
    """The voiceover from tts.txt: direction tags -> segments -> one cached take each -> joined with set gaps."""
    import numpy as np
    import soundfile as sf
    segs = direction(text)
    if not segs:
        sys.exit("tts.txt has no spoken lines")
    cache.mkdir(parents=True, exist_ok=True)
    per_line = bool(cfg.get("per_line", True))
    audio, beats, sr, paid, reused = [], [], None, 0, 0
    t = 0.0
    for i, g in enumerate(groups(segs, per_line)):
        words = "\n".join(s.text for s in g)
        pace = float(cfg["pace"]) * g[0].pace
        p = cache / f"{take_key(words, cfg, pace)}.wav"
        if p.exists() and not any(s.line in retake for s in g):
            reused += len(words)
        else:
            p.write_bytes(sarvam_request(words, cfg, pace))
            paid += len(words)
        x, r = sf.read(io.BytesIO(p.read_bytes()), dtype="float32")
        if sr is None:
            sr = r
        elif r != sr:
            sys.exit(f"tts: take {p.name} is {r} Hz, the others {sr} Hz")
        x = trim(x, sr)
        if i:
            gap = g[0].beat or LINE_GAP
            if g[0].beat:                  # audio_clean keeps this pause instead of capping it
                beats.append([round(t + gap / 2, 3), round(gap + 2 * EDGE, 3)])
            audio.append(np.zeros((int(gap * sr),) + x.shape[1:], dtype="float32"))
            t += gap
        audio.append(x)
        t += len(x) / sr
    sf.write(dest, np.concatenate(audio), sr, subtype="PCM_16")
    return {"request_chars": paid, "cached_chars": reused, "takes": len(groups(segs, per_line)),
            "per_line": per_line, "beats": beats,
            "paced": sorted({s.line + 1 for s in segs if s.pace != 1.0})}


def kokoro(text: str, cfg: dict, dest: Path) -> dict:
    spoken = re.sub(r"[^\x00-\x7F₹]", "", "\n".join(strip_tags(x) for x in text.splitlines()))  # Kokoro can't read Devanagari
    txt = dest.with_suffix(".txt")
    txt.write_text(spoken)
    e = dict(os.environ, HYPERFRAMES_PYTHON=str(ROOT / ".venv" / "bin" / "python"))
    speaker = cfg["speaker"] if "_" in cfg["speaker"] and len(cfg["speaker"]) < 12 else "am_michael"
    subprocess.run(["npx", "--no-install", "hyperframes", "tts", str(txt), "-v", speaker,
                    "-s", str(cfg["pace"]), "-o", str(dest)], check=True, cwd=ROOT, env=e,
                   capture_output=True)
    txt.unlink()
    return {"speaker": speaker}


def concat(parts: list[Path], dest: Path) -> None:
    if len(parts) == 1:
        parts[0].replace(dest)
        return
    lst = dest.with_suffix(".list")
    lst.write_text("".join(f"file '{p}'\n" for p in parts))
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
                    "-c:a", "pcm_s16le", str(dest)], check=True)
    lst.unlink()
    for p in parts:
        p.unlink()


def duration(p: Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                        "default=nw=1:nk=1", str(p)], capture_output=True, text=True)
    return float(r.stdout.strip() or 0)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("episode")
    ap.add_argument("--provider", choices=["sarvam", "kokoro"])
    ap.add_argument("--speaker")
    ap.add_argument("--model")
    ap.add_argument("--pace", type=float)
    ap.add_argument("--audition", help="comma list of speakers; writes voice/audition/<speaker>.wav")
    ap.add_argument("--probe", action="store_true", help="time script.md with the real voice -> .cache/probe.wav")
    ap.add_argument("--retake", default="", help="comma list of line ids (L6,L8): new takes for only those lines")
    a = ap.parse_args()

    ep = load(a.episode)
    cfg = {**DEFAULTS, **ep.config.get("tts", {})}
    for k in ("provider", "speaker", "model", "pace"):
        if getattr(a, k) is not None:
            cfg[k] = getattr(a, k)
    if a.probe:
        dest = ep.cache / "probe.wav"
        dest.parent.mkdir(parents=True, exist_ok=True)
        (sarvam if cfg["provider"] == "sarvam" else kokoro)(respell(ep.spoken_text)[0], cfg, dest)
        print(f"probe: {duration(dest):.1f} s of voice")
        return
    text, mixed = tts_text(ep)
    text, hits = respell(text)
    if hits:
        print(f"  lexicon: {', '.join(hits)} (brand/pronunciations.tsv)")
    if cfg["provider"] == "sarvam" and not mixed:
        print("! no voice/tts.txt — sending romanised Hinglish; Sarvam quality will suffer "
              "(run /voiceover to write a Devanagari-mixed tts.txt)")
    speakers = a.audition.split(",") if a.audition else [cfg["speaker"]]
    for spk in speakers:
        c = {**cfg, "speaker": spk.strip()}
        if a.audition:
            dest = ep.dir / "voice" / "audition" / f"{c['speaker']}.wav"
        else:
            dest = ep.dir / "voice" / "voice.wav"
        dest.parent.mkdir(parents=True, exist_ok=True)
        if c["provider"] != "sarvam":
            info = kokoro(text, c, dest)
        elif a.audition:
            info = sarvam("\n".join(strip_tags(x) for x in text.splitlines()), c, dest)
        else:
            ids = [ln.id for ln in ep.lines if ln.spoken]
            n = len({s.line for s in direction(text)})
            if n != len(ids):
                print(f"! tts.txt has {n} spoken lines, script.md {len(ids)} — keep one tts line per script line")
            want = {x.strip() for x in a.retake.split(",") if x.strip()}
            if want - set(ids):
                sys.exit(f"--retake: unknown line id(s) {', '.join(sorted(want - set(ids)))}")
            info = sarvam_directed(text, c, dest, ep.cache / "tts_takes", {ids.index(x) for x in want})
            print(f"  {info['takes']} takes: {info['request_chars']} chars sent, {info['cached_chars']} reused from cache"
                  + (f", {len(info['beats'])} beat(s)" if info["beats"] else ""))
        meta = {"provider": c["provider"], "model": c["model"] if c["provider"] == "sarvam" else "kokoro-82m",
                "speaker": c["speaker"], "pace": c["pace"], "language": c["language"],
                "text_file": "voice/tts.txt" if mixed else "script.md", "date": dt.date.today().isoformat(),
                "seconds": round(duration(dest), 2), "ai_generated": True, "lexicon": hits, **info}
        dest.with_suffix(".json").write_text(json.dumps(meta, indent=2, ensure_ascii=False))
        print(f"  ✓ {c['speaker']:28s} {meta['seconds']:5.1f}s -> {dest.relative_to(ep.dir)}")
    if a.audition:
        page = audition_page(ep.dir / "voice" / "audition", text)
        print(f"audition page: {page}")


def audition_page(d: Path, text: str) -> Path:
    import html
    rows = []
    for j in sorted(d.glob("*.json")):
        m = json.loads(j.read_text())
        rows.append(f"""<div class="chillar-card opt"><div class="t-body name">{html.escape(m['speaker'])}</div>
      <div class="t-sub small">{m['model']} · pace {m['pace']} · <span class="t-mono">{m['seconds']}s</span></div>
      <audio controls preload="none" src="{html.escape(j.stem)}.wav"></audio></div>""")
    page = d / "index.html"
    page.write_text(f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Voice audition</title>
<link rel="stylesheet" href="{os.path.relpath(ROOT / 'brand' / 'colors.css', d)}">
<style>body{{margin:0;font-family:var(--font-body)}} main{{max-width:760px;margin:0 auto;padding:32px 16px}}
h1{{font-size:56px;margin:0 0 12px}} .opt{{padding:14px 16px;margin:0 0 14px}} .name{{font-size:22px}}
.small{{font-size:14px;font-weight:700}} audio{{width:100%;margin-top:8px}}
pre{{white-space:pre-wrap;font-family:var(--font-body);font-weight:700;background:var(--card);border:3px solid var(--ink);padding:12px}}
code{{font-family:var(--font-mono)}}</style></head>
<body class="chillar-paper"><main><h1 class="t-head">Voice audition</h1><pre>{html.escape(text)}</pre>
{''.join(rows)}
<p class="t-body">Lock one: set <code>speaker = "..."</code> under <code>[tts]</code> in episode.toml (or tell Claude).</p>
</main></body></html>""")
    return page


if __name__ == "__main__":
    main()
