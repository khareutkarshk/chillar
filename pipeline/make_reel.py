#!/usr/bin/env python3
"""Full pipeline for one episode.

  make_reel.py episodes/<ep> [--from STAGE] [--only STAGE] [--quality draft|looks|delivery]
                            [--allow-unsourced]

Stages:  facts → clean → align → validate → build → render → mix → cover → sheet
  facts     fact_lint.py — blocks the render if any number/claim is unsourced
  clean     audio_clean.py — voice/voice.* → .cache/voice_clean.wav (-14 LUFS)
  align     align.py — forced alignment → .cache/words.json (+ adlibs.md)
  validate  validate_scenes.py — scenes/scenes.json → .cache/scenes.resolved.json
            (scenes.json is written by Claude in /render; this stage stops if it's missing)
  build     build_composition.py → episodes/<ep>/build/index.html (HyperFrames project) + lint
  render    npx hyperframes render → .cache/video.mp4 (silent)
  mix       mix.py → output/final.mp4
  cover     cover.py → output/cover.png
  sheet     contact_sheet.py → output/contact_sheet.png (+ palette check)
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import align as align_mod  # noqa: E402
import audio_clean  # noqa: E402
import contact_sheet  # noqa: E402
import cover as cover_mod  # noqa: E402
import fact_lint  # noqa: E402
import mix as mix_mod  # noqa: E402
import validate_scenes  # noqa: E402
from build_composition import build  # noqa: E402
from lib.common import ROOT  # noqa: E402
from lib.episode import load  # noqa: E402

STAGES = ["facts", "clean", "align", "validate", "build", "render", "mix", "cover", "sheet"]


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    print("  $ " + " ".join(cmd))
    return subprocess.run(cmd, cwd=ROOT, text=True)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("episode")
    ap.add_argument("--from", dest="start", choices=STAGES, default="facts")
    ap.add_argument("--only", choices=STAGES)
    ap.add_argument("--quality", choices=["draft", "looks", "delivery"])
    ap.add_argument("--allow-unsourced", action="store_true")
    a = ap.parse_args()
    ep = load(a.episode)
    stages = [a.only] if a.only else STAGES[STAGES.index(a.start):]
    quality = a.quality or ep.config["render"]["quality"]
    t0 = time.time()

    for st in stages:
        print(f"\n▶ {st}")
        if st == "facts":
            r = fact_lint.lint(a.episode)
            for p in r["problems"]:
                print(f"  ✗ {p}")
            for w in r["warnings"]:
                print(f"  ! {w}")
            if not r["ok"] and not a.allow_unsourced:
                print("  RENDER BLOCKED: unsourced facts (fix facts.md / script.md or pass --allow-unsourced)")
                return 1
        elif st == "clean":
            audio_clean.clean(a.episode)
        elif st == "align":
            align_mod.align(a.episode)
        elif st == "validate":
            res, errors, warns = validate_scenes.resolve(a.episode)
            for w in warns:
                print(f"  ! {w}")
            for e in errors:
                print(f"  ✗ {e}")
            if errors:
                return 1
            (ep.cache / "scenes.resolved.json").write_text(json.dumps(res, indent=1, ensure_ascii=False))
            print(f"  ✓ {len(res['scenes'])} clips, {res['duration']:.1f}s, {len(res['sfx'])} sfx")
        elif st == "build":
            res = json.loads((ep.cache / "scenes.resolved.json").read_text())
            idx = build(res, ep.dir / "build", "reel")
            lint = subprocess.run(["npx", "--no-install", "hyperframes", "lint", str(idx.parent)], cwd=ROOT,
                                  capture_output=True, text=True)
            errs = [l for l in lint.stdout.splitlines() if "✗" in l]
            print("\n".join(errs) or "  ✓ lint: 0 errors")
            if errs:
                return 1
        elif st == "render":
            out = ep.cache / "video.mp4"
            r = run(["npx", "--no-install", "hyperframes", "render", str(ep.dir / "build"), "--output", str(out),
                     "--quality", quality, "--fps", "30", "--quiet"])
            if r.returncode != 0 or not out.exists():
                print("  ✗ render failed")
                return 1
        elif st == "mix":
            mix_mod.mix(a.episode)
        elif st == "cover":
            cover_mod.cover(a.episode)
        elif st == "sheet":
            contact_sheet.sheet(a.episode)
    print(f"\ndone in {time.time() - t0:.0f}s → {ep.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
