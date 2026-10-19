---
description: Full Chillar production line — research → writers' room (scriptwriter ⇄ script-reviewer) → fact-check → voice → director → editor → render → video-reviewer loop → delivery, run by pipeline/produce.py
argument-hint: <topic> [30|60|90]
---

Make a Chillar Reel about **$ARGUMENTS** (format = the number given, default 60). You are the producer,
but the routing is done by `pipeline/produce.py`: it runs every agent in `.claude/agents/` headless and
fresh each round (lean context, pinned models, real cost logged), passes files not contents, and stops
when a decision is the creator's. CLAUDE.md is law; the loops and their limits are unchanged.

**Keep this session thin — it costs more than the agents.** Ideally run it on Sonnet (`/model sonnet`;
the writer, reviewer and director keep Opus — their model is pinned in produce.py). Don't read agent
outputs, scripts or frames unless a step below says so. Note `npx ccusage@latest session` at the start.

1. Slug `YYYY-MM-<short-topic>`. Run in the background (it takes 30–60 min):
   `.venv/bin/python pipeline/produce.py episodes/<slug> --topic "<topic>" --format <30|60|90>`
   and wait for it to finish — don't poll its output.
2. **Exit 0** → it printed the summary (cover, hook, words/seconds, fact-check) and the usage table.
   **Exit 3** → read `notes/STOP.md` only, tell me the reason in two lines plus the options it lists, and
   ask me. Then resume with `--from <stage>` (e.g. `--from deliver` after I accept a draft,
   `--from edit` for one more round). Any other exit → read the last 30 lines of its output and fix.
3. After `deliver`: look at `output/contact_sheet.png` **once** yourself (CLAUDE.md §8 — never claim a render
   is done without it). If something is clearly broken (overlapping text, empty frame, off-palette), fix
   it surgically in scenes.json, `--from deliver` again, look again.
4. Append the ccusage end figure to `notes/usage.md` (the agent table is already there).
5. Report: duration, format, stamps, transitions, review rounds (script + video), LUFS, agent cost +
   session cost, and paths to final.mp4, cover.png, post.md, contact sheet.

Manual step-by-step still works: `/new-reel` → `/package` → `/fact-check` → `/voiceover` → `/render`,
or one stage at a time with `produce.py episodes/<slug> --only <stage>`.
