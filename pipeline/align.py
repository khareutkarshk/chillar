#!/usr/bin/env python3
"""Word timestamps by FORCED ALIGNMENT of script.md to the cleaned voice (stable-ts on a
faster-whisper model). Hinglish ASR is unreliable; alignment uses the words you wrote.

A second free transcription pass flags ad-libs (spoken words not in the script).

  align.py episodes/<ep> [--no-adlib]   -> .cache/words.json, .cache/adlibs.md
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.episode import load, norm, tokenize  # noqa: E402


def _model(name: str):
    import stable_whisper
    return stable_whisper.load_faster_whisper(name, device="cpu", compute_type="int8")


def align(ep_dir: str, adlib: bool = True) -> Path:
    ep = load(ep_dir)
    audio = ep.cache / "voice_clean.wav"
    if not audio.exists():
        sys.exit("run audio_clean first")
    cfg = ep.config["align"]
    model = _model(cfg["model"])

    # script tokens, remembering which line each belongs to
    toks = []
    for line in ep.lines:
        for i, t in enumerate(tokenize(line.spoken)):
            toks.append({"text": t, "line": line.id, "chapter": line.chapter, "i": i})
    text = " ".join(t["text"] for t in toks)

    # pad 1 s of silence: without it the aligner can run out of audio on the last line and
    # collapse its words onto the final sample (seen on 2026-10-epf-explained)
    import subprocess, tempfile
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(audio)],
                               capture_output=True, text=True).stdout or 0)
    padded = Path(tempfile.mkdtemp()) / "voice_pad.wav"
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(audio), "-af", "apad=pad_dur=1",
                    str(padded)], check=True)
    res = model.align(str(padded), text, language=cfg["language"], vad=False)
    aligned = [w for seg in res.segments for w in seg.words]
    a_norm = [norm(w.word) for w in aligned]
    s_norm = [norm(t["text"]) for t in toks]

    # map aligned words onto script tokens (they should match 1:1; be robust anyway)
    sm = difflib.SequenceMatcher(a=s_norm, b=a_norm, autojunk=False)
    times: list[tuple[float, float] | None] = [None] * len(toks)
    for blk in sm.get_matching_blocks():
        for k in range(blk.size):
            w = aligned[blk.b + k]
            times[blk.a + k] = (min(float(w.start), dur), min(float(w.end), dur)) if dur else (float(w.start), float(w.end))
    # interpolate any unmatched tokens between neighbours
    for i, t in enumerate(times):
        if t is None:
            prev = next((times[j][1] for j in range(i - 1, -1, -1) if times[j]), 0.0)
            nxt = next((times[j][0] for j in range(i + 1, len(times)) if times[j]), prev + 0.3)
            times[i] = (prev, max(prev + 0.05, nxt))
    words = []
    for i, (t, (s, e)) in enumerate(zip(toks, times)):
        words.append({"id": f"w{i}", "text": t["text"], "start": round(s, 3), "end": round(e, 3),
                      "line": t["line"], "chapter": t["chapter"], "i": t["i"]})
    # enforce monotonic, non-overlapping
    for a, b in zip(words, words[1:]):
        if b["start"] < a["start"]:
            b["start"] = a["start"]
        if a["end"] > b["start"]:
            a["end"] = b["start"]
        if b["end"] < b["start"]:
            b["end"] = b["start"] + 0.05
    out = ep.cache / "words.json"
    out.write_text(json.dumps(words, indent=1, ensure_ascii=False))
    matched = sum(blk.size for blk in sm.get_matching_blocks())
    print(f"align: {len(words)} words, {matched}/{len(words)} matched directly → {out.relative_to(ep.dir)}")

    if adlib:
        # stable-ts wraps transcribe() and returns a WhisperResult
        r2 = model.transcribe(str(audio), language=cfg["language"], word_timestamps=True,
                              initial_prompt=text[:800], verbose=None)
        segs = r2[0] if isinstance(r2, tuple) else r2.segments
        heard = [(norm(w.word), w.start, w.word) for s in segs for w in (s.words or [])]
        sm2 = difflib.SequenceMatcher(a=s_norm, b=[h[0] for h in heard], autojunk=False)
        notes = []
        for op, a1, a2, b1, b2 in sm2.get_opcodes():
            if op in ("insert", "replace") and b2 - b1 >= 2:
                said = " ".join(h[2].strip() for h in heard[b1:b2])
                scripted = " ".join(t["text"] for t in toks[a1:a2]) or "—"
                if re.sub(r"\W", "", said.lower()) == re.sub(r"\W", "", scripted.lower()):
                    continue  # same words, different tokenisation ("0 .90 %" vs "0.90%")
                notes.append(f"- {heard[b1][1]:.1f}s heard “{said}” | script: “{scripted}”")
        (ep.cache / "adlibs.md").write_text(
            "# Possible ad-libs / misreads (ASR is approximate for Hinglish — use your ears)\n\n"
            + ("\n".join(notes) or "none detected") + "\n")
        print(f"adlibs: {len(notes)} possible → .cache/adlibs.md")
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    ap.add_argument("--no-adlib", action="store_true")
    a = ap.parse_args()
    align(a.episode, not a.no_adlib)
