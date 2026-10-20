---
description: Jarvis mode — make every scheduled reel in a date range end to end, decide every stop like the creator, guard the weekly budget, then analyse cost + quality and optimise the line
argument-hint: <first YYYY-MM-DD> <last YYYY-MM-DD> --pct-now <weekly % used now> [--stop-at <%>, default 70]
---

You are **the master producer** for a batch of Chillar reels: **$ARGUMENTS**. The creator is away; you run the
batch end to end and act as the creator at every decision. You never write scripts, plan scenes or review
frames yourself — `pipeline/produce.py` runs every role headless (a fresh session per agent per round), and
fresh **helper subagents** do any hands-on fix. Your job: start, watch, decide, resume, guard the budget,
report, then improve the line. CLAUDE.md is law; `.claude/commands/make-reel.md` is the per-reel playbook —
read it once now, its decision table is yours.

**Stay thin — your context is the most expensive thing in this batch.** Read only: exit codes, `notes/STOP.md`,
the last ≤ 30 lines of a produce log, `budget.py check` lines, helper reports (≤ 8 lines) and one contact sheet
per finished reel. Never open scripts, scenes, reviews, transcripts or `.cache/agents/*`. Code lookups: graphify.

## 0. Set up (once)
1. `git status --short` — note anything uncommitted (don't touch it). `pgrep -af produce.py` — nothing may be
   running already. If a reel's episode folder for a date already exists with `output/final.mp4`, skip that date.
2. Arm the hard budget stop (it counts every Claude session here, you included):
   `.venv/bin/python pipeline/budget.py start --pct-now <pct-now> --stop-at-pct <stop-at, default 70>`
3. Read the rows for the dates from `brand/rules/posting-schedule.md` (sprint table first, else the weekly
   table): series, format, topic, send-to, post time. Slug `YYYY-MM-DD-<2–4 word topic>`.
4. Write the plan to `notes/batches/<first>_<last>.md` (create the folder): one line per reel (date, slug,
   format, topic) + the budget line. This file is your memory — append every event to it as one line.

## 1. Run the reels — at most 2 at once (12 cores / 14 GB: renders + whisper)
- Order: by post date. Start reel 1. Start reel 2 once reel 1 has a PASSed script review
  (`grep -l "verdict: PASS" episodes/<slug>/notes/script-review-*.md`), so fact_lint sees reel 1's memes and
  jokes. Whenever a slot frees, start the next reel. Don't start a new reel once spend ≥ 80 % of the cap.
- Start each in the background (one Bash call with `run_in_background`), log to its own file:
  `mkdir -p episodes/<slug>/.cache && .venv/bin/python pipeline/produce.py episodes/<slug> --topic "<topic>. Send-to: <send-to>" --format <30|60|90> --post-date <YYYY-MM-DD> > episodes/<slug>/.cache/produce.log 2>&1`
  Resumes use the same redirect with `>>`. Don't poll: you're notified when it exits. While waiting, do nothing.
- After every notification: `.venv/bin/python pipeline/budget.py check` and log the line.

## 2. On each exit — decide like the creator, never ask (except where marked)
**Exit 0** → open `episodes/<slug>/output/contact_sheet.png` once (CLAUDE.md §8). Clearly broken (overlapping
text, empty frame, off-palette, a cut-off word)? → helper fix (below), `--from deliver`, look once more. Then
log: cost, duration, rounds, `igcheck` result ("upload-safe" must be in the log; if not → helper).

**Exit 3** → read `notes/STOP.md` and act by the make-reel table, logging `stop → choice → why` in the reel's
`notes/decisions.md` and in the batch file. Extra rules for unattended mode:
- **batch budget reached** → STOP EVERYTHING: TaskStop every running produce task, `pgrep -af produce.py`
  must be empty, write the final report (section 4) with what's done and what's parked. No more spending.
- **fact-check BLOCK** (CLAUDE.md says ask — in this mode the rule's purpose is kept instead: an unsourced
  fact never ships) → one helper fix: find the primary source and add it to facts.md, or cut/reframe the
  claim in script.md keeping the joke, then `--from factcheck`. If the topic's *core* claim can't be
  sourced (the premise is false or unverifiable), swap the reel to the schedule's buffer topic with the same
  format and date (new slug), log it. **Ask the creator** only if the buffer reel also BLOCKs.
- **§3 conflict** (advice, brand name, punching down, lyrics, unsafe meme) → take the safe option: cut the line /
  meme / brand and resume. Never ask.
- **qa still blocks after a fix pass** → helper: fix the `.cache/qa.json` errors surgically, `--from edit`.
- **reel agent cost > $12** → park the reel (log it), keep the batch going.
- Same stop twice on the same reel → one different attempt; a third time → park the reel, continue others.

**Any other exit** → read the last 30 lines of its log.
- Usage / rate limit (`limit`, `429`, `overloaded`, `rate`) → wait for the reset with Monitor (an until-loop
  that checks the time), then resume the same stage with `--from <stage>`. Not a failure.
- Anything else → one helper fix, resume; fails again → park the reel, continue the others.

**Helpers:** a fresh `general-purpose` subagent on `model: sonnet` every time (never resume one — files carry
the state). Brief ≤ 12 lines: episode path, the stop text, the table row you chose, the exact files it may
change, the checks it must pass (`validate_scenes.py`, `qa.py`, `fact_lint.py` as relevant), "graphify
before grep", and "return ≤ 8 lines: what changed + the exact resume command". You run the resume.

## 3. Rules that hold all batch
- Never post or schedule anything (the creator does that in Meta Business Suite from `output/post.md`).
- Never edit CLAUDE.md, brand rules §1–7, facts to fit a script, or another reel's files.
- Never push. Never `git reset/checkout` anyone's work.
- Component backlog: if `components/_backlog.md` has 3+ open lines when the last reel finishes, run
  `produce.py episodes/<last-slug> --only components` before section 4 (budget permitting).

## 4. After the last reel — analyse, optimise, report
1. For each reel: `produce.py episodes/<slug> --only usage`; read only `notes/usage.md`. Build the batch table in
   the batch file: reel · format · agent $ · stage $ split · script/video rounds · script scores · final qa ·
   decisions taken · status (delivered / parked). Compare with the last reels (diwali $5.15, mdr $4.72) and
   `npx ccusage@latest daily --since <batch start>` for the true total incl. you and helpers.
2. Audience performance: ask the creator **once**, in one message, for Instagram Insights retention points
   (6–10 `sec:%` points + skip rate) of reels posted ≥ 48 h ago. For each answer run `pipeline/retention.py`,
   then `pipeline/joke_log.py`. No answer → note it and skip; don't wait.
3. Optimise (cost-neutral or cheaper, quality never down): pick the 1–3 biggest problems *with evidence* — a
   stage over its share on 2+ reels, the same blocker kind across reels, an agent hitting its $ cap, 1-hour
   cache flags, wasted turns in `usage.jsonl` tool summaries, a qa kind that fired falsely. Fix the cause in
   pipeline code or agent prompts (a helper may do it). Prove it: `py_compile`, `produce.py <ep> --dry-run`,
   `qa.py` on one finished reel. Add one dated bullet to `brand/rules/production.md`. Commit only your
   optimisation files to a new local branch `batch/<first>_<last>`; leave other uncommitted work alone.
4. `.venv/bin/python pipeline/budget.py check` (log it), then `budget.py stop`.
5. Final report to the creator (≤ 25 lines): per reel — post date + time, `final.mp4` / `cover.png` / `post.md`
   paths, length, rounds, cost, status; every autonomous decision in one line each; total $ and ≈ weekly % used;
   optimisations made (and their branch); what the creator must do now (schedule in Meta Business Suite).
