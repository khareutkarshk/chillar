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

Settings ([tts] in episode.toml): provider, model, speaker, pace, temperature, language.
"""
from __future__ import annotations

import argparse
import base64
import datetime as dt
import json
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.common import ROOT, env, session  # noqa: E402
from lib.episode import load  # noqa: E402

SARVAM_URL = "https://api.sarvam.ai/text-to-speech"
DEFAULTS = {"provider": "sarvam", "model": "bulbul:v4-flash", "speaker": "sunny_hi_reels",
            "pace": 1.2, "temperature": 0.6, "language": "hi-IN"}
MAX_CHARS = 2400  # API limit is 2500 for v3 / v4-flash


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


def sarvam(text: str, cfg: dict, dest: Path) -> dict:
    key = env("SARVAM_API_KEY")
    if not key:
        sys.exit("SARVAM_API_KEY missing in .env")
    parts = []
    for i, chunk in enumerate(chunks(text)):
        body = {"text": chunk, "language_code": cfg["language"], "model": cfg["model"],
                "speaker": cfg["speaker"], "pace": float(cfg["pace"]),
                "temperature": float(cfg["temperature"]), "speech_sample_rate": 48000,
                "output_audio_codec": "wav"}
        r = session.post(SARVAM_URL, json=body, headers={"api-subscription-key": key}, timeout=120)
        if r.status_code != 200:
            sys.exit(f"Sarvam {r.status_code}: {r.text[:400]}")
        p = dest.with_suffix(f".part{i}.wav")
        p.write_bytes(base64.b64decode(r.json()["audios"][0]))
        parts.append(p)
    concat(parts, dest)
    return {"request_chars": len(text)}


def kokoro(text: str, cfg: dict, dest: Path) -> dict:
    spoken = re.sub(r"[^\x00-\x7F₹]", "", text)  # Kokoro can't read Devanagari
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
    a = ap.parse_args()

    ep = load(a.episode)
    cfg = {**DEFAULTS, **ep.config.get("tts", {})}
    for k in ("provider", "speaker", "model", "pace"):
        if getattr(a, k) is not None:
            cfg[k] = getattr(a, k)
    if a.probe:
        dest = ep.cache / "probe.wav"
        dest.parent.mkdir(parents=True, exist_ok=True)
        (sarvam if cfg["provider"] == "sarvam" else kokoro)(ep.spoken_text, cfg, dest)
        print(f"probe: {duration(dest):.1f} s of voice")
        return
    text, mixed = tts_text(ep)
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
        info = (sarvam if c["provider"] == "sarvam" else kokoro)(text, c, dest)
        meta = {"provider": c["provider"], "model": c["model"] if c["provider"] == "sarvam" else "kokoro-82m",
                "speaker": c["speaker"], "pace": c["pace"], "language": c["language"],
                "text_file": "voice/tts.txt" if mixed else "script.md", "date": dt.date.today().isoformat(),
                "seconds": round(duration(dest), 2), "ai_generated": True, **info}
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
