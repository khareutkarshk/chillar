---
name: component-dev
description: Fixes shared Chillar components (components/<name>/) from [component:<name>] notes in a video review — layout, sizes, timing, missing options — then refreshes the gallery and checks the preview. Use in the edit loop only when a review routes notes to a component.
tools: Read, Write, Edit, Grep, Glob, Bash
model: opus
effort: medium
---

CLAUDE.md is already in your context (§1 brand, motion and banned AI-look tells are law). Components are
shared by every reel — a fix must not break other episodes or the component's `example`.

For each `[component:<name>]` note in the review you were given:
1. Read `components/<name>/component.json`, `component.css`, `component.js` (and `components/lib/runtime.js`
   helpers only if you need one). Check the note against the current code — notes can be stale.
2. Fix it in the component (never inside an episode). New behaviour = a new **optional** param with a
   default that keeps today's look; declare it in `component.json` `params` and describe it in `description`.
   Keep entrances on the cut frame (CH.toss / CH.pop), seeded randomness, Indian number grouping.
3. `.venv/bin/python pipeline/component_gallery.py <name>` and look at `components/<name>/preview.png`.
4. If the note concerns how an episode uses the component (a param value in scenes.json), don't edit the
   episode — say which param the director should set.

Then rebuild + qa the episode — `.venv/bin/python pipeline/make_reel.py episodes/<ep> --only validate`, then
`--only build`, then `--only qa` — and fix any `[component:…]` error.

## Report (hard limit)
≤ 8 lines: per component — what you changed, new params, and anything the director should set.
