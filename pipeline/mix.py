#!/usr/bin/env python3
"""Mix voice + SFX (placed on component events) + sidechain-ducked music, loudnorm to -14 LUFS,
and mux with the silent render.

  mix.py episodes/<ep> [--video .cache/video.mp4]  -> output/final.mp4, .cache/mix.wav

Sound resolution order (per slot): brand/sfx/custom/<slot>.* → brand/sfx/<slot>.wav (locked)
→ brand/_audition/files/<slot>/1-* (PROVISIONAL, until you lock picks).
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fetch_assets import SLOTS  # noqa: E402
from lib.common import BRAND  # noqa: E402
from lib.episode import load  # noqa: E402

SFX_GAIN_DB = {"stamp": -3, "printer": -12, "ding": -8, "coin": -9, "scratch": -7,
               "glitch": -10, "typing": -13, "whoosh": -12}
AUDIO_EXT = (".wav", ".mp3", ".ogg", ".flac", ".m4a", ".aiff")


def ff(*a: str) -> subprocess.CompletedProcess:
    return subprocess.run(["ffmpeg", "-hide_banner", "-y", *a], capture_output=True, text=True, check=True)


def resolve_sound(slot: str) -> tuple[Path | None, str]:
    for p in sorted((BRAND / "sfx" / "custom").glob(f"{slot}.*")):
        if p.suffix.lower() in AUDIO_EXT:
            return p, "custom"
    p = BRAND / "sfx" / f"{slot}.wav"
    if p.exists():
        return p, "locked"
    prov = sorted((BRAND / "_audition" / "files" / slot).glob("1-*"))
    prov = [x for x in prov if x.suffix.lower() in AUDIO_EXT]
    return (prov[0], "PROVISIONAL") if prov else (None, "missing")


def resolve_music(track: str) -> tuple[Path | None, str]:
    if track:
        p = BRAND / "music" / track
        return (p, "locked") if p.exists() else (None, "missing")
    locked = sorted(x for x in (BRAND / "music").glob("*") if x.suffix.lower() in AUDIO_EXT)
    if locked:
        return locked[0], "locked"
    prov = sorted((BRAND / "_audition" / "files" / "music").glob("1-*"))
    prov = [x for x in prov if x.suffix.lower() in AUDIO_EXT]
    return (prov[0], "PROVISIONAL") if prov else (None, "missing")


def lufs(path: Path) -> float:
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(path), "-af", "ebur128=framelog=quiet", "-f", "null", "-"],
                       capture_output=True, text=True)
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)
    return float(m[-1]) if m else -70.0


def loudnorm_2pass(src: Path, dst: Path, target: float, tp: float = -1.0) -> None:
    r = ff("-i", str(src), "-af", f"loudnorm=I={target}:TP={tp}:LRA=11:print_format=json", "-f", "null", "-")
    m = json.loads(re.findall(r"\{[^{}]+\}", r.stderr)[-1])
    ff("-i", str(src), "-af",
       f"loudnorm=I={target}:TP={tp}:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
       f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true",
       "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(dst))


def mix(ep_dir: str, video: Path | None = None) -> Path:
    ep = load(ep_dir)
    res = json.loads((ep.cache / "scenes.resolved.json").read_text())
    total = float(res["duration"])
    voice = ep.cache / "voice_clean.wav"
    target = float(ep.config["voice"]["lufs"])
    under = float(res.get("music", {}).get("under_voice_db", -22))
    report = {"sfx": [], "music": None}

    inputs = ["-i", str(voice)]
    graph = [f"[0:a]aformat=sample_rates=48000:channel_layouts=stereo,apad=whole_dur={total},asplit=2[vox][vsc]"]
    mixins = ["[vox]"]
    idx = 1

    mpath, mstate = resolve_music(res.get("music", {}).get("track", ""))
    if mpath:
        g = target + under - lufs(mpath)
        inputs += ["-stream_loop", "-1", "-i", str(mpath)]
        graph.append(f"[{idx}:a]aformat=sample_rates=48000:channel_layouts=stereo,atrim=0:{total},asetpts=N/SR/TB,"
                     f"volume={g:.2f}dB,afade=t=in:d=0.6,afade=t=out:st={max(0, total - 1.8):.2f}:d=1.8[mus]")
        graph.append("[mus][vsc]sidechaincompress=threshold=0.03:ratio=4:attack=20:release=320:makeup=1[musd]")
        mixins.append("[musd]")
        report["music"] = {"file": str(mpath), "state": mstate, "gain_db": round(g, 2), "under_voice_db": under}
        idx += 1
    else:
        graph.append("[vsc]anullsink")

    for i, s in enumerate(res.get("sfx", [])):
        path, state = resolve_sound(s["sound"])
        if not path:
            print(f"  ! no sound for '{s['sound']}' — skipped")
            continue
        trim = SLOTS.get(s["sound"], {}).get("trim", 2.0)
        ms = int(round(s["t"] * 1000))
        inputs += ["-i", str(path)]
        graph.append(f"[{idx}:a]aformat=sample_rates=48000:channel_layouts=stereo,"
                     f"silenceremove=start_periods=1:start_threshold=-50dB,atrim=0:{trim},"
                     f"afade=t=out:st={max(trim - 0.15, 0):.2f}:d=0.15,volume={SFX_GAIN_DB.get(s['sound'], -10)}dB,"
                     f"adelay={ms}|{ms}[s{i}]")
        mixins.append(f"[s{i}]")
        report["sfx"].append({**s, "file": str(path), "state": state})
        idx += 1

    graph.append(f"{''.join(mixins)}amix=inputs={len(mixins)}:normalize=0:duration=longest,atrim=0:{total}[out]")
    pre = ep.cache / "mix_pre.wav"
    ff(*inputs, "-filter_complex", ";".join(graph), "-map", "[out]", "-ar", "48000", "-c:a", "pcm_s24le", str(pre))
    out_wav = ep.cache / "mix.wav"
    loudnorm_2pass(pre, out_wav, target, -1.0)
    report["final_lufs"] = round(lufs(out_wav), 2)
    (ep.cache / "mix_report.json").write_text(json.dumps(report, indent=2))

    prov = [x["sound"] for x in report["sfx"] if x["state"] == "PROVISIONAL"]
    if report["music"] and report["music"]["state"] == "PROVISIONAL":
        prov.append("music")
    print(f"mix: {len(report['sfx'])} sfx, music {'on' if mpath else 'off'}, {report['final_lufs']} LUFS"
          + (f"  [PROVISIONAL sounds: {', '.join(sorted(set(prov)))} — lock your picks]" if prov else ""))

    video = video or ep.cache / "video.mp4"
    final = ep.output / "final.mp4"
    ff("-i", str(video), "-i", str(out_wav), "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy",
       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", "-movflags", "+faststart", str(final))
    print(f"final: {final}")
    return final


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("episode")
    ap.add_argument("--video", type=Path)
    a = ap.parse_args()
    mix(a.episode, a.video)
