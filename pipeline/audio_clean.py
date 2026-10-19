#!/usr/bin/env python3
"""Voice cleanup: high-pass 80 Hz → denoise (RNNoise, afftdn fallback) → presence boost 3–5 kHz →
de-ess → compression → tighten silences/breaths → two-pass loudnorm to -14 LUFS.

  audio_clean.py episodes/<ep>   -> .cache/voice_clean.wav, .cache/voice_edl.json
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.common import ROOT  # noqa: E402
from lib.episode import Episode, load  # noqa: E402

RNN = ROOT / "tools" / "rnnoise" / "std.rnnn"
SR = 48000


def ff(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["ffmpeg", "-hide_banner", "-y", *args], capture_output=True, text=True, check=True)


def has_filter(name: str) -> bool:
    out = subprocess.run(["ffmpeg", "-hide_banner", "-filters"], capture_output=True, text=True).stdout
    return f" {name} " in out


def find_voice(ep: Episode) -> Path:
    p = ep.dir / ep.config["voice"]["file"]
    if p.exists():
        return p
    cands = sorted(x for x in (ep.dir / "voice").glob("*") if x.suffix.lower() in
                   (".wav", ".m4a", ".mp3", ".flac", ".aac", ".ogg", ".opus"))
    if not cands:
        sys.exit(f"no voice file in {ep.dir / 'voice'} — record one and drop it there")
    return cands[0]


def tighten(x: np.ndarray, sr: int, thresh_db: float, max_gap: float) -> tuple[np.ndarray, list]:
    """Shorten every pause (silence or breath below thresh) to max_gap, with 8 ms crossfades.
    Returns new audio and an edit list of kept [src_start, src_end] seconds."""
    hop = int(sr * 0.01)
    frames = len(x) // hop
    rms = np.sqrt(np.mean(x[: frames * hop].reshape(frames, hop) ** 2, axis=1) + 1e-12)
    db = 20 * np.log10(rms)
    quiet = db < thresh_db
    # find quiet runs
    runs, i = [], 0
    while i < frames:
        if quiet[i]:
            j = i
            while j < frames and quiet[j]:
                j += 1
            runs.append((i, j))
            i = j
        else:
            i += 1
    keep, cursor = [], 0
    gap = int(max_gap / 0.01)
    for a, b in runs:
        if b - a <= gap:
            continue
        lead = gap // 2 if a > 0 else 2           # leading silence of the file → nearly all cut
        tail = gap - gap // 2 if b < frames else 2
        keep.append((cursor, a + lead))
        cursor = b - tail
    keep.append((cursor, frames))
    fade = int(sr * 0.008)
    out = []
    for a, b in keep:
        seg = x[a * hop: b * hop].copy()
        if len(seg) > 2 * fade:
            ramp = np.linspace(0, 1, fade)
            seg[:fade] *= ramp
            seg[-fade:] *= ramp[::-1]
        out.append(seg)
    edl = [[round(a * 0.01, 3), round(b * 0.01, 3)] for a, b in keep]
    return np.concatenate(out) if out else x, edl


def loudnorm(src: Path, dst: Path, lufs: float) -> dict:
    first = ff("-i", str(src), "-af", f"loudnorm=I={lufs}:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-")
    m = json.loads(re.findall(r"\{[^{}]+\}", first.stderr)[-1])
    ff("-i", str(src), "-af",
       f"loudnorm=I={lufs}:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
       f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true",
       "-ar", str(SR), "-ac", "1", "-c:a", "pcm_s16le", str(dst))
    return m


def clean(ep_dir: str) -> Path:
    ep = load(ep_dir)
    v = ep.config["voice"]
    src = find_voice(ep)
    pre = ep.cache / "voice_pre.wav"
    chain = ["highpass=f=80"]
    if v["denoise"] == "rnnoise" and RNN.exists() and has_filter("arnndn"):
        chain.append(f"arnndn=m={RNN}:mix=0.9")
    elif v["denoise"] != "off":
        chain.append("afftdn=nf=-25")
    chain += [f"equalizer=f=4000:t=q:w=0.9:g={v['presence_db']}",
              "deesser=i=0.35:m=0.5:f=0.5",
              "acompressor=threshold=-21dB:ratio=3:attack=6:release=80:makeup=3"]
    ff("-i", str(src), "-af", ",".join(chain), "-ar", str(SR), "-ac", "1", "-c:a", "pcm_f32le", str(pre))

    x, sr = sf.read(pre, dtype="float32")
    tight, edl = tighten(x, sr, float(v["silence_threshold_db"]), float(v["max_gap_s"]))
    tight_p = ep.cache / "voice_tight.wav"
    sf.write(tight_p, tight, sr, subtype="FLOAT")

    out = ep.cache / "voice_clean.wav"
    m = loudnorm(tight_p, out, float(v["lufs"]))
    info = {"source": str(src.relative_to(ep.dir)), "chain": chain, "edl": edl,
            "in_seconds": round(len(x) / sr, 2), "out_seconds": round(len(tight) / sr, 2),
            "loudnorm_first_pass": m}
    (ep.cache / "voice_edl.json").write_text(json.dumps(info, indent=2))
    print(f"clean: {src.name} {info['in_seconds']}s → {info['out_seconds']}s, -14 LUFS → {out.relative_to(ep.dir)}")
    return out


if __name__ == "__main__":
    clean(sys.argv[1])
