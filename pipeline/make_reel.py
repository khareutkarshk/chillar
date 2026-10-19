#!/usr/bin/env python3
"""Full pipeline for one episode.

  make_reel.py episodes/<ep> [--from STAGE] [--only STAGE] [--quality draft|looks|delivery]
                            [--allow-unsourced] [--allow-qa]

Stages:  facts → clean → align → validate → build → qa → render → mix → cover → sheet → igcheck
  facts     fact_lint.py — blocks the render if any number/claim is unsourced
  clean     audio_clean.py — voice/voice.* → .cache/voice_clean.wav (-14 LUFS)
  align     align.py — forced alignment → .cache/words.json (+ adlibs.md)
  validate  validate_scenes.py — scenes/scenes.json → .cache/scenes.resolved.json
            (scenes.json is written by Claude in /render; this stage stops if it's missing)
  build     build_composition.py → episodes/<ep>/build/index.html (HyperFrames project) + lint
  qa        qa.py — mechanical QA of the built composition (empty cuts, safe zones, text overlap,
            odometer values, numbers before they're spoken, short shots) → .cache/qa.json;
            errors block the render (--allow-qa to override). Re-run after mix for the audio check.
  render    npx hyperframes render → .cache/video.mp4 (silent)
  mix       mix.py → output/final.mp4
  cover     cover.py → output/cover.png
  sheet     contact_sheet.py → output/contact_sheet.png (+ palette check)
  igcheck   ig_export.py — final.mp4 + cover.jpg meet the Instagram Reels upload spec
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
import ig_export  # noqa: E402
import mix as mix_mod  # noqa: E402
import qa as qa_mod  # noqa: E402
import validate_scenes  # noqa: E402
from build_composition import build  # noqa: E402
from lib.common import ROOT  # noqa: E402
from lib.episode import load  # noqa: E402

STAGES = ["facts", "clean", "align", "validate", "build", "qa", "render", "mix", "cover", "sheet", "igcheck"]


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
    ap.add_argument("--allow-qa", action="store_true", help="render even if qa.py finds errors")
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
        elif st == "qa":
            r = qa_mod.qa(a.episode, audio=False)
            for i in r["issues"]:
                t = f"t={i['t']:.2f}" if i["t"] is not None else "t=–"
                print(f"  {'✗' if i['sev'] == 'error' else '!'} [{i['route']}] {t} {i['kind']}: {i['where']} — {i['msg']}")
            print(f"  qa: {r['errors']} error(s), {r['warnings']} warning(s) → .cache/qa.json")
            if r["errors"] and not a.allow_qa:
                print("  RENDER BLOCKED: fix the qa errors (route each to director/editor/component) or pass --allow-qa")
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
            q = ep.cache / "qa.json"
            if q.exists():
                rep = json.loads(q.read_text())
                aud_issues: list = []
                rep["audio"] = qa_mod.audio_check(ep, aud_issues)
                rep["issues"] = [i for i in rep["issues"] if i["kind"] != "audio"] + aud_issues
                q.write_text(json.dumps(rep, indent=1, ensure_ascii=False))
                for i in aud_issues:
                    print(f"  {'✗' if i['sev'] == 'error' else '!'} [editor] audio: {i['msg']} → {i['fix']}")
        elif st == "cover":
            cover_mod.cover(a.episode)
        elif st == "sheet":
            contact_sheet.sheet(a.episode)
        elif st == "igcheck":
            cov = ep.output / "cover.jpg"
            if not ig_export.report(ep.output / "final.mp4", cov if cov.exists() else None):
                return 1
    print(f"\ndone in {time.time() - t0:.0f}s → {ep.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
