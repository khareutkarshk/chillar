#!/usr/bin/env python3
"""Assemble a standalone HyperFrames composition from a resolved scene spec.

  spec = {"duration": s, "scenes": [{id, component, params, start, duration, track}],
          "captions": [{start, end, words:[{text,start,end}]}], "effects": [...]}

Everything is inlined or copied next to index.html (fonts, gsap, components) so the render has
no network access needs.
"""
from __future__ import annotations

import html
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.common import BRAND, ROOT  # noqa: E402

COMP = ROOT / "components"
POST = {"wordmark"}       # composited after the camera (static on screen)
TOK = json.loads((BRAND / "tokens.json").read_text())
GSAP = ROOT / "node_modules" / "gsap" / "dist" / "gsap.min.js"


def component_meta(name: str) -> dict:
    return json.loads((COMP / name / "component.json").read_text())


def all_components() -> list[str]:
    return sorted(p.parent.name for p in COMP.glob("*/component.json"))


def merged_params(name: str, params: dict) -> dict:
    out = dict(component_meta(name).get("params", {}))
    out.update(params or {})
    return out


def attr(v) -> str:
    return html.escape(str(v), quote=True)


def build(spec: dict, out: Path, comp_id: str = "reel") -> Path:
    out.mkdir(parents=True, exist_ok=True)
    (out / "fonts").mkdir(exist_ok=True)
    for f in (BRAND / "fonts").glob("*.ttf"):
        shutil.copy2(f, out / "fonts" / f.name)
    shutil.copy2(GSAP, out / "gsap.min.js")

    used = sorted({s["component"] for s in spec["scenes"]} | {"captions"} if spec.get("captions") else
                  {s["component"] for s in spec["scenes"]})
    css = [(BRAND / "colors.css").read_text(), (COMP / "lib" / "base.css").read_text()]
    js = [(BRAND / "mascot" / "chillar.js").read_text(), (COMP / "lib" / "runtime.js").read_text()]
    for name in used:
        for fn, bucket in (("component.css", css), ("component.js", js)):
            p = COMP / name / fn
            if p.exists():
                bucket.append(f"/* ---- {name}/{fn} ---- */\n" + p.read_text())

    scenes = []
    for s in spec["scenes"]:
        s = dict(s)
        s["params"] = merged_params(s["component"], s.get("params", {}))
        if s["params"].get("_file"):            # fetched media (memes): copied next to index.html
            src = Path(s["params"].pop("_file"))
            (out / "media").mkdir(exist_ok=True)
            shutil.copy2(src, out / "media" / src.name)
            s["params"]["_src"] = f"media/{src.name}"
        scenes.append(s)
    dur = round(float(spec["duration"]), 3)

    clips, post = [], []
    for s in scenes:
        # added in post, like a real edit: the handle never rides the handheld camera
        (post if s["component"] in POST else clips).append(f'    <div id="{attr(s["id"])}" class="clip scene" data-start="{s["start"]:.3f}" '
                     f'data-duration="{s["duration"]:.3f}" data-track-index="{int(s.get("track", 1))}"></div>')
    caps = []
    for i, g in enumerate(spec.get("captions") or []):
        caps.append(f'    <div id="cap{i}" class="clip cap-group" data-start="{g["start"]:.3f}" '
                    f'data-duration="{max(g["end"] - g["start"], 0.05):.3f}" data-track-index="9"></div>')

    mount = {"scenes": scenes, "effects": spec.get("effects", []), "captions": spec.get("captions", []),
             "duration": dur, "episode": spec.get("episode", ""), "human": spec.get("human", True)}
    # scene data is LLM-written: "</script>" or "<!--" in a string must not end the inline script
    spec_js = json.dumps(mount, ensure_ascii=False).replace("<", "\\u003c")
    cid_js = json.dumps(comp_id).replace("<", "\\u003c")
    page = f"""<!doctype html>
<html lang="en" data-theme="{attr(spec.get('theme') or TOK['theme'])}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=1080, height=1920">
<title>{html.escape(str(spec.get('title', 'Chillar reel')))}</title>
<script src="gsap.min.js"></script>
<style>
{chr(10).join(css).replace('url("fonts/', 'url("fonts/')}
</style>
</head>
<body>
<div id="root" data-composition-id="{attr(comp_id)}" data-start="0" data-width="1080" data-height="1920" data-duration="{dur}">
  <svg width="0" height="0" style="position:absolute" aria-hidden="true"><filter id="ch-boil" x="-5%" y="-5%" width="110%" height="110%">
    <feTurbulence type="fractalNoise" baseFrequency="0.032" numOctaves="2" seed="1"/>
    <feDisplacementMap in="SourceGraphic" scale="1.4" xChannelSelector="R" yChannelSelector="G"/></filter>
    <filter id="ch-ink" x="-2%" y="-10%" width="104%" height="120%"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="1" seed="3"/>
    <feDisplacementMap in="SourceGraphic" scale="1.3" xChannelSelector="R" yChannelSelector="G"/></filter></svg>
  <div id="camera"><div id="rig"><div id="stage">
{chr(10).join(clips)}
  </div></div></div>
  <div id="light"></div>
  <div id="overlay">
{chr(10).join(post)}
  </div>
  <div id="captions">
{chr(10).join(caps)}
  </div>
</div>
<script>
{chr(10).join(js)}
</script>
<script>
const SPEC = {spec_js};
document.fonts.ready.then(() => {{
  if (window.CHCaptions) CHCaptions.build(SPEC.captions);
  const tl = gsap.timeline({{ paused: true }});
  CH.mount(SPEC, {{ tl }});
  if (window.CHCaptions) CHCaptions.animate(tl, SPEC.captions);
  window.__timelines[{cid_js}] = tl;   // register only after the build is complete
  window.__hfForceTimelineRebind && window.__hfForceTimelineRebind();
}});
</script>
</body>
</html>
"""
    (out / "index.html").write_text(page)
    (out / "spec.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False))
    return out / "index.html"


if __name__ == "__main__":
    spec = json.loads(Path(sys.argv[1]).read_text())
    print(build(spec, Path(sys.argv[2])))
