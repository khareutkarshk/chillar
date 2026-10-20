---
description: Full Chillar production line — research → writers' room (scriptwriter ⇄ script-reviewer) → fact-check → voice → director → editor → render → video-reviewer loop → delivery, run by pipeline/produce.py
argument-hint: <topic> [30|60|90] [post-date YYYY-MM-DD]
---

Make a Chillar Reel about **$ARGUMENTS** (format = the number given, default 60). You are the producer,
but the routing is done by `pipeline/produce.py`: it runs every agent in `.claude/agents/` headless and
fresh each round (lean context, pinned models, real cost logged), passes files not contents, and stops
when a decision is the creator's. CLAUDE.md is law; the loops and their limits are unchanged.

**Keep this session thin — it costs more than the agents.** Ideally run it on Sonnet (`/model sonnet`;
the writer, reviewer and director keep Opus — their model is pinned in produce.py). Don't read agent
outputs, scripts or frames unless a step below says so. Note `npx ccusage@latest session` at the start.

1. Resolve the planned posting date from the matching row in `brand/rules/posting-schedule.md`; if this topic is
   not on the calendar, use the next unassigned posting day. An explicit date in the command takes precedence.
   Slug `YYYY-MM-DD-<short-topic>`. Run in the background (it takes 30–60 min):
   `.venv/bin/python pipeline/produce.py episodes/<slug> --topic "<topic>" --format <30|60|90> --post-date YYYY-MM-DD`
   and wait for it to finish — don't poll its output.
2. **Exit 0** → it printed the summary (cover, hook, words/seconds, fact-check) and the usage table.
   **Exit 3** → read `notes/STOP.md` only, **decide like the creator would — don't ask** (creator's call,
   2026-10-20), resume, and log one line per decision (stop → choice → why) in `notes/decisions.md`.
   `--extra-rounds N` counts from the start: N = reviews already in notes/ − 3 + 1.
   | stop | decision |
   |---|---|
   | script: no PASS after the cap | one more round (`--from script --extra-rounds N`); still no PASS → if the last review has facts PASS and no blocker, accept the draft (`--from factcheck`), else ask |
   | script PASSed, length probe misses | one length round (`--from script --extra-rounds N`); still out → accept it (`--from factcheck --accept-length`) — a passed script beats more rounds |
   | voice outside the range at align | `--from align --accept-length` |
   | video: no PASS after 3 rounds | "fix it and ship": `--only fix`, then `--from deliver` |
   | qa still blocks the draft after a fix pass | read `.cache/qa.json` errors, fix them surgically in scenes.json, `--from edit` |
   | fact-check still BLOCK after a fix cycle | **ask** — a wrong or unsourced fact never ships (SEBI/ASCI) |
   Also **ask** when a choice would break a §3 content rule, or the reel's agent cost passes $12.
   The final report lists every autonomous decision.
   Component requests no longer run mid-reel: they collect in `components/_backlog.md`; build them in one
   batch with `produce.py episodes/<any> --only components` (weekly, or when the backlog has 3+ open). Never run a director/editor
   fix as an in-session subagent — `--only fix` does it headless and cheaper. Any other exit → read the last 30
   lines of its output and fix. Code lookups: `graphify query` first; grep only known lines / episode files.
3. After `deliver`: look at `output/contact_sheet.png` **once** yourself (CLAUDE.md §8 — never claim a render
   is done without it). If something is clearly broken (overlapping text, empty frame, off-palette), fix
   it surgically in scenes.json, `--from deliver` again, look again.
4. Append the ccusage end figure to `notes/usage.md` (the agent table is already there).
5. Report: duration, format, stamps, transitions, review rounds (script + video), LUFS, agent cost +
   session cost, and paths to final.mp4, cover.png, post.md, contact sheet.

Manual step-by-step still works: `/new-reel` → `/package` → `/fact-check` → `/voiceover` → `/render`,
or one stage at a time with `produce.py episodes/<slug> --only <stage>`.
