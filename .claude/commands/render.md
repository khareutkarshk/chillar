---
description: Edit suite — director plans scenes, editor tightens, render, video-reviewer loop until PASS, then mix, cover, contact sheet
argument-hint: <episode folder or slug> [draft|delivery]
---

Render episode **$ARGUMENTS**. Quality defaults to `episode.toml` (draft while iterating).

1. **Gates.** `fact_lint.py` must be clean (run /fact-check if anything is doubtful). A voice file must
   exist in `voice/` — if not, run /voiceover (Sunny, CLAUDE.md §7) first; don't ask.

2. **Audio + words.** `.venv/bin/python pipeline/make_reel.py episodes/<slug> --only clean`,
   then `--only align`. Read `.cache/words.json` and `.cache/adlibs.md` (tell me about real ad-libs).

3. **Director.** Spawn the `director` agent: "Plan scenes for episodes/<slug>." It writes
   `scenes/scenes.json` and gets `validate_scenes.py` and `qa.py` to pass.

4. **Editor.** Spawn the `editor` agent: "Edit episodes/<slug>/scenes/scenes.json." Rhythm, cut
   points, comedic timing, transitions (real cuts only — never text cards), SFX.

5. **Render a draft** `.venv/bin/python pipeline/make_reel.py episodes/<slug> --from validate --quality draft`.
   The `qa` stage runs before the render and blocks it on errors: route each one by its tag
   (`[director]` / `[editor]` → a fresh agent with "fix the qa errors in .cache/qa.json";
   `[component:x]` → fix it yourself) and re-run. Mechanical bugs never reach the reviewer.

6. **Video review** (loop, max 3 rounds). Spawn a **new** `video-reviewer` each round: "Review
   episodes/<slug>, round <n>." Route its notes, always to **fresh** agents (never resume one — the notes
   file is the hand-off): `[director]` → new director agent "Revise episodes/<slug>/scenes/scenes.json
   from the [director] notes in notes/video-review-<n>.md"; `[editor]` → new editor agent, same pattern;
   `[component:<name>]` → fix the component yourself and run `pipeline/component_gallery.py <name>`.
   Re-render and review again until PASS. Don't open frames yourself while routing — the notes say enough.
   After round 3, show me the remaining notes and the contact sheet and ask.

7. **Deliver.** `--from validate --quality delivery` (ends with `igcheck` — must print "upload-safe", CLAUDE.md §9). Look at `output/contact_sheet.png` yourself
   (CLAUDE.md §8). Report: duration + format, fields per chapter, transitions, stamps / re-hooks / SFX
   counts, mix LUFS (`.cache/mix_report.json`), PROVISIONAL sounds, review rounds, paths to
   `output/final.mp4`, `output/cover.png`, and show me the contact sheet.
