#!/usr/bin/env python3
"""Instagram Reels export spec + checker (CLAUDE.md §9). Spec: brand/tokens.json "instagram".

  ig_export.py check <file.mp4> [--cover cover.jpg]   exit 1 if anything would break on upload

encode_args() is used by mix.py for output/final.mp4 so every export is encoded to the spec,
never stream-copied from the renderer.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.common import BRAND  # noqa: E402

IG = json.loads((BRAND / "tokens.json").read_text())["instagram"]
E, L = IG["export"], IG["metaLimits"]


def encode_args() -> list[str]:
    """ffmpeg output args: H.264 High 4:2:0, 30 fps CFR, 1 s closed GOP, capped VBR, BT.709, AAC 128k/48k stereo."""
    return [
        "-vf", f"scale={E['width']}:{E['height']}:flags=lanczos,fps={E['fps']},format={E['pixFmt']}",
        "-c:v", "libx264", "-profile:v", E["profile"], "-level:v", E["level"], "-preset", "slow", "-tune", "animation",
        "-crf", str(E["crf"]), "-maxrate", f"{E['maxrateMbps']}M", "-bufsize", f"{E['bufsizeMbps']}M",
        "-g", str(E["gopFrames"]), "-keyint_min", str(E["gopFrames"]), "-flags", "+cgop", "-x264-params", "open-gop=0",
        "-fps_mode", "cfr", "-r", str(E["fps"]),
        "-colorspace", E["color"], "-color_primaries", E["color"], "-color_trc", E["color"], "-color_range", "tv",
        "-c:a", E["audioCodec"], "-b:a", f"{E['audioBitrateKbps']}k", "-ar", str(E["audioSampleRate"]), "-ac", str(E["audioChannels"]),
        "-movflags", "+faststart", "-use_editlist", "0", "-map_metadata", "-1",
    ]


def probe(path: Path) -> dict:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
                       capture_output=True, text=True, check=True)
    return json.loads(r.stdout)


def atoms(path: Path) -> list[str]:
    """Top-level MP4 atoms in file order."""
    out, data = [], path.read_bytes()
    i = 0
    while i + 8 <= len(data):
        size = int.from_bytes(data[i:i + 4], "big")
        kind = data[i + 4:i + 8].decode("latin-1")
        if size == 1:
            size = int.from_bytes(data[i + 8:i + 16], "big")
        out.append(kind)
        if size < 8:
            break
        i += size
    return out


def keyframe_gap(path: Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-skip_frame", "nokey", "-show_entries",
                        "frame=pts_time", "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    ts = sorted(float(x.strip(",")) for x in r.stdout.split() if x.strip(", "))
    return max((b - a for a, b in zip(ts, ts[1:])), default=0.0)


def check(path: Path, cover: Path | None = None) -> list[str]:
    errs = []
    if path.suffix.lower().lstrip(".") not in L["container"]:
        errs.append(f"container {path.suffix} — use .mp4")
    info = probe(path)
    v = next((s for s in info["streams"] if s["codec_type"] == "video"), None)
    a = next((s for s in info["streams"] if s["codec_type"] == "audio"), None)
    fmt = info["format"]
    if not v:
        return ["no video stream"]
    if v["codec_name"] != E["videoCodec"]:
        errs.append(f"video codec {v['codec_name']} — export {E['videoCodec']}")
    if v.get("pix_fmt") != E["pixFmt"]:
        errs.append(f"pixel format {v.get('pix_fmt')} — must be {E['pixFmt']} (4:2:0)")
    if (v["width"], v["height"]) != (E["width"], E["height"]):
        errs.append(f"size {v['width']}x{v['height']} — must be {E['width']}x{E['height']} (9:16)")
    if v.get("field_order") not in (None, "progressive", "unknown"):
        errs.append(f"interlaced ({v['field_order']}) — must be progressive")
    r_fps, avg_fps = Fraction(v["r_frame_rate"]), Fraction(v.get("avg_frame_rate") or v["r_frame_rate"])
    if float(r_fps) != E["fps"] or abs(float(avg_fps) - E["fps"]) > 0.05:
        errs.append(f"frame rate {float(r_fps):.3f}/{float(avg_fps):.3f} — must be constant {E['fps']} fps")
    vbr = int(v.get("bit_rate") or 0) / 1e6
    if vbr > L["maxVideoBitrateMbps"]:
        errs.append(f"video bitrate {vbr:.1f} Mbps > {L['maxVideoBitrateMbps']} Mbps")
    if v.get("color_primaries") not in (None, "unknown", E["color"]) or v.get("color_transfer") not in (None, "unknown", E["color"]):
        errs.append(f"colour tags {v.get('color_primaries')}/{v.get('color_transfer')} — tag {E['color']} or colours shift")
    gap = keyframe_gap(path)
    if gap > 2.05:
        errs.append(f"keyframe gap {gap:.1f}s — keep ≤ 2 s (closed 1 s GOP)")
    if not a:
        errs.append("no audio stream — IG mutes/flags silent uploads oddly; always mux audio")
    else:
        if a["codec_name"] != "aac":
            errs.append(f"audio codec {a['codec_name']} — must be AAC")
        if int(a["sample_rate"]) > L["audioMaxSampleRate"]:
            errs.append(f"audio {a['sample_rate']} Hz > 48 kHz")
        if int(a["channels"]) not in L["audioChannels"]:
            errs.append(f"audio has {a['channels']} channels — mono or stereo only")
        abr = int(a.get("bit_rate") or 0) / 1000
        if abr > L["audioBitrateKbps"] * 1.1:
            errs.append(f"audio bitrate {abr:.0f} kbps — Meta spec is {L['audioBitrateKbps']} kbps")
    dur = float(fmt["duration"])
    if not L["durationSec"][0] <= dur <= L["durationSec"][1]:
        errs.append(f"duration {dur:.1f}s outside {L['durationSec'][0]}–{L['durationSec'][1]} s")
    mb = int(fmt["size"]) / 1e6
    if mb > L["maxFileMB"]:
        errs.append(f"file {mb:.0f} MB > {L['maxFileMB']} MB")
    at = atoms(path)
    if "moov" in at and "mdat" in at and at.index("moov") > at.index("mdat"):
        errs.append("moov atom after mdat — re-mux with -movflags +faststart")
    if b"elst" in path.read_bytes()[:2_000_000] and "moov" in at and at.index("moov") < 3:
        errs.append("edit list present — re-mux with -use_editlist 0")
    if cover:
        from PIL import Image
        im = Image.open(cover)
        if im.format != "JPEG":
            errs.append(f"cover is {im.format} — upload a JPEG")
        if cover.stat().st_size > L["cover"]["maxMB"] * 1e6:
            errs.append(f"cover > {L['cover']['maxMB']} MB")
        if abs(im.width / im.height - 9 / 16) > 0.01:
            errs.append(f"cover {im.width}x{im.height} is not 9:16")
    return errs


def report(path: Path, cover: Path | None = None) -> bool:
    errs = check(path, cover)
    info = probe(path)
    v = next(s for s in info["streams"] if s["codec_type"] == "video")
    print(f"instagram check: {path.name} {v['width']}x{v['height']} {v['codec_name']} {v.get('pix_fmt')} "
          f"{float(Fraction(v['r_frame_rate'])):.0f}fps {int(v.get('bit_rate') or 0) / 1e6:.1f}Mbps "
          f"{float(info['format']['duration']):.1f}s {int(info['format']['size']) / 1e6:.1f}MB")
    for e in errs:
        print(f"  ✗ {e}")
    print("  ✓ upload-safe for Reels" if not errs else "  NOT upload-safe — fix before posting")
    return not errs


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["check"])
    ap.add_argument("file", type=Path)
    ap.add_argument("--cover", type=Path)
    a = ap.parse_args()
    sys.exit(0 if report(a.file, a.cover) else 1)
