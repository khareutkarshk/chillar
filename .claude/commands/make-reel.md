---
description: Full Chillar production line — research → writers' room (scriptwriter ⇄ script-reviewer) → fact-check → voice → director → editor → render → video-reviewer loop → delivery
argument-hint: <topic> [30|60|90]
---

Make a Chillar Reel about **$ARGUMENTS** (format = the number given, default 60). You are the
producer: you run the room, pass work between the subagents in `.claude/agents/`, and keep the loops
honest. CLAUDE.md is law. Never skip a review because a draft "looks fine".

**Stage 1 — Research + packaging** (you). Do steps 1–3 of `/new-reel` (folder, sourced facts.md,
cover.md). Set `target_seconds` in script.md frontmatter to the format.

**Stage 2 — Writers' room** (loop, max 3 rounds).
1. `scriptwriter` agent: "Write episodes/<ep>/script.md, <format> s format." (later rounds: "Rewrite
   from notes/script-review-<n>.md.")
2. `script-reviewer` agent: "Review episodes/<ep>/script.md, round <n>."
3. REVISE → back to 1 with the notes file. PASS → continue. After round 3 without PASS, stop and show
   me the last review + script and ask how to proceed.

**Stage 3 — Fact-check.** `fact-checker` agent. BLOCK → send the blocking rows to `scriptwriter` for a
fix, re-review only the changed lines with `script-reviewer`, re-check. Show me: cover text, hook
line, word count, the best 3 jokes, and the fact table.

**Stage 4 — Voice (no stop).** Run `/voiceover <ep>` — the channel voice is Sarvam `sunny_hi_reels`
at pace 1.2 (CLAUDE.md §7). Check the duration fits the format, then continue. Only use a creator
recording if I explicitly said so for this episode.

**Stage 5 — Edit suite** (loop, max 3 rounds). Run clean + align (`make_reel.py … --only clean`,
then `--only align`). Then:
1. `director` agent → scenes.json (later rounds: "address the [director] notes in notes/video-review-<n>.md").
2. `editor` agent → tightens scenes.json (later rounds: "[editor] notes in …").
3. Render a draft: `.venv/bin/python pipeline/make_reel.py episodes/<ep> --from validate --quality draft`.
4. `video-reviewer` agent → notes/video-review-<n>.md. `[component:<name>]` notes are yours to fix in
   `components/` (then re-run `pipeline/component_gallery.py <name>` and look at it).
5. REVISE → loop. PASS → delivery render `--from validate --quality delivery`, then look at the contact
   sheet yourself one last time (CLAUDE.md §8: never claim a render is done without looking).

**Stage 6 — Ship.** `/package` for post.md if not done. Report: duration, format, stamps, transitions,
review rounds used (script + video), LUFS, and paths to final.mp4, cover.png, post.md, contact sheet.
