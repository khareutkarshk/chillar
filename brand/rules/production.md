# Production line — how work is routed, and what it costs

## Agents (`.claude/agents/`), one job each; `pipeline/produce.py` routes them
| agent | model · effort | does | loop |
|---|---|---|---|
| `researcher` | sonnet · medium | library facts first, then primary-source gaps → `facts.md` (+ library) | fact_lint row problems → researcher once, before the writer |
| `scriptwriter` | opus · high | writes/rewrites script.md (jokes, puns, meme refs, facts cited) | ⇄ script-reviewer, ≤ 3 rounds |
| `script-reviewer` | opus · high | scores + line notes → `notes/script-review-<n>.md`, PASS/REVISE | |
| `fact-checker` | sonnet · medium | verifies claims → `notes/fact-check.md`, PASS/BLOCK; makes ≤ 3-word hedge fixes + facts.md housekeeping itself (🔧) | script-line BLOCK → scriptwriter; facts.md-only BLOCK → fact-checker again |
| `director` | opus · medium | script + words.json → `scenes/scenes.json` (visuals, fields, stamps, cuts) | ⇄ video-reviewer |
| `editor` | sonnet · medium | rhythm, cut points, comedic timing, transitions, SFX in scenes.json | ⇄ video-reviewer |
| `video-reviewer` | sonnet · medium | judges taste/comedy/retention on top of `qa.py` → `notes/video-review-<n>.md` | ≤ 3 rounds |
| `component-dev` | sonnet · medium | fixes `[component:<name>]` review notes in `components/` (only when routed) | in the edit loop |
| `voice` | sonnet · medium | `voice/tts.txt` → Sunny voice → pronunciation check | |
| `packager` | sonnet · medium | `output/post.md` (caption, pinned math, sources) | |
Quality is decided by the writer, the script reviewer and the director — they keep the strongest
model. The others do lookup, arithmetic and checking. Simple file chores and graphify extraction: haiku.
After 3 rounds without PASS the pipeline stops; the producer decides by the table in `.claude/commands/make-reel.md` (asks only for a fact-check BLOCK, a §3 conflict or cost > $12).

## Hand-offs: fresh agents, files carry the state
- **Every round spawns a new agent.** Never resume/SendMessage an earlier director, editor or reviewer:
  resuming replays its whole history (the first reel's director replay cost ~200k tokens).
- The prompt names only the files to read; scoped edit agents get a bounded brief assembled by
  `pipeline/agent_context.py`. Revision briefs contain the current artifact, routed notes and QA, not the
  episode's full history. The notes files must stand alone.
- The producer (main session) passes paths, not file contents, and doesn't re-read what an agent
  just wrote unless it must decide something from it.

## Mechanical QA before taste
`make_reel.py` runs `qa` after `build` (no render needed): empty cut frames, text outside safe zones,
text over text, captions/numbers before they're spoken, wrong odometer values, short shots; after `mix`
it adds true peak / LUFS. Errors block the render. The director/editor fix qa errors **before** the
first render; the video-reviewer reads `.cache/qa.json` and never re-checks what it covers.

## Bounded edit briefs
`pipeline/agent_context.py` builds the per-run source packet for scriptwriter, script-reviewer, director,
editor, video-reviewer and component-dev. First-pass director briefs cap at 32k chars; other briefs cap at 24k and include
only current scenes, routed notes, QA and role-specific references. Images stay as paths: the video-reviewer
may inspect the contact sheet and up to 12 selected frames; component-dev may inspect one component preview.
`produce.py` removes Grep/Glob from these runs and restricts Bash to `.venv/bin/python`; do not broaden a role's
context or tools unless its task cannot be completed from the brief, and record that missing input explicitly.
Each run logs `prompt_chars` beside token usage so brief-size changes can be compared against actual cost.
The first director brief also includes `brand/shot-patterns.json`: optional recipes for hooks, comparisons,
reveals, myths, reactions and callbacks. Adapt them only where they improve clarity; preserve stronger original
visual metaphors and vary compositions across chapters.

## Image budget (a full 1080×1920 frame ≈ 1.5k tokens every time it's viewed)
- Per review round: **one contact sheet** (`output/contact_sheet.png`) + at most **12 single frames**,
  pulled at 540×960 with `pipeline/frames.py episodes/<ep> <t>… | --qa` (only flagged timestamps
  and punchlines). `--full` only to read small text, and rarely.
- Don't open `contact_sheet_guides.png` unless qa reports a safe-zone issue you need to see.
- The director reads `components/_catalog.md`, not the gallery PNGs or every component.json.

## Facts
New episodes copy recurring facts from `brand/facts-library.md` (`pipeline/facts_library.py copy`).
The fact-checker re-verifies only stale library entries (`facts_library.py fresh episodes/<ep>`) and
episode-specific facts, reading cached sources in `brand/sources/` before fetching the web.
Cached source PDFs/HTML are searchable through `pipeline/source_index.py` (SQLite FTS5, rebuildable
under `.cache/`). Research and fact-check agents should retrieve exact cited passages before opening
large files; page/URL provenance stays with each excerpt. Search volume is logged per episode and shown
in `notes/usage.md` so context reduction can be measured.

## Session hygiene
- One episode per session: start `/make-reel` in a fresh session; `/compact` after the fact-check
  (stage 3) and again after the first video-review round if the session is long.
- Track cost per episode: `npx ccusage@latest daily` (or `session`) before and after; note the total in
  `episodes/<ep>/notes/usage.md` so each process change can be measured.

## The cheap way to run it: `pipeline/produce.py` (since 2026-10-19)
Baseline: the EPF reel made by a producer session routing in-session subagents cost **≈ $11.4**
(≈ 26M tokens); ~95 % of that was the producer session re-reading its own growing context.
`produce.py` moves the routing into a script:
- **Headless, lean agents:** `claude -p --agent <name>` with no MCP servers, no skills, no hooks and only the
  agent's own tools — per-run overhead ≈ $0.006 instead of ≈ $0.026 (measured), and a stable, cacheable prefix.
- **Pinned models:** frontmatter aliases map to full ids in `MODELS` (opus → claude-opus-5-5). Aliases follow
  the CLI version — the old global CLI (2.1.76) silently served opus-4-6. produce.py picks the newest Claude
  Code binary (≥ 2.1.280) and logs the model every run actually used; a mismatch is flagged.
- **CLAUDE.md is auto-loaded** into every agent — agent files must not tell it to read CLAUDE.md again.
- **Reports ≤ 8 lines**; detail lives in notes files. The script reads only verdict lines.
- **Rounds only for routed roles:** round ≥ 2 runs director / editor / component-dev only if the review
  routed notes to them.
- **Targeted script revisions:** rewrites read only the latest review, preserve unmentioned lines and address
  exact actionable notes. Reviewers separate blockers from polish and avoid repeating resolved or subjective
  preferences. Routine component fixes use Sonnet; use Opus when a new component needs creative design.
- **(2026-10-20) Cost fixes after chai-vs-phone ($7.83, 4/4 reels stuck at 3 video rounds):**
  `FORCE_PROMPT_CACHING_5M` on every agent (1-hour cache writes billed 2× input; runs are < 6 min) — a run that
  still writes 1-hour cache is flagged. Routing reads every owner in a note tag (`[director|component:x]` used to
  skip component-dev). The director's own `[component:*]` requests go to component-dev (existing components) or
  `notes/component-wishlist.md` (new ones, the creator's call). Director revisions and fix passes run at medium
  effort (`REVISE_EFFORT`). The video-reviewer marks notes `blocker|polish`, passes with no blockers, and adds
  only new blockers after round 1.
- **(2026-10-21) Cost fixes after diwali-bonus-tax ($4.48; director = 33 % of all agent spend):** the director's
  first pass runs at medium (was high; watch video rounds on the next reels). It reads `qa.py --for director` (only
  its own issues) and never opens review frames or meme images. `package` skips when post.md is newer than
  script/facts/cover/fact-check (re-deliveries reran it). The backlog keeps one open line per component.
- **Real cost per run** (`total_cost_usd`) → `notes/usage.jsonl` → `notes/usage.md`; `--max-budget-usd`
  caps per agent (BUDGET in produce.py) are safety nets, not targets.
- **Cost and quality together:** `usage.md` reports prompt characters, cached-read tokens and stage cost beside
  the latest script scores, video swipe-risk/blocker/polish counts and final mechanical QA. Lower cost is not a
  win if quality signals regress.
- **Fewer wasted rounds:** fact_lint's script self-check (spoken length with numbers in full at the measured
  3.2 words/s + outro, laugh margin, first laugh, absolutes on cited lines, long lines); qa's layout warnings
  (`narrow-frame`, `small-text`, `same-layout`) + `layout` boxes in qa.json; frames.py deletes stale frames;
  the reviewer measures from qa, not half-size frames; align pads 1 s so the last line can't collapse.

- **(2026-10-21) Quality at the same cost** — every recurring review blocker of the first 9 reels moved to code, and
  the writers' room got memory:
  - qa.py: `hidden-text` (Chillar/an object on or under words, by hit-testing — the mascot SVG is no longer
    exempt), `clipped-text`, `broken-word`, `late-number` (the voice says a number its shot shows only later —
    found in 5 shipped reels), `late-text` (an empty card at the settled frame). The outro now prints on the cut.
  - Voice: `{beat}` / `{slow}` / `{fast}` direction tags in tts.txt for comic timing; per-line cached takes, so a
    re-take (`tts.py --retake L6`) pays only for that line; voice_check always runs before the video review.
  - Script: `brand/joke-log.md` (`joke_log.py`, rebuilt before each first draft: games taken, landed, fell flat,
    overused props, audience drops) goes to the writer + reviewer on round 1. The writer may add `{alt: "…"}` to
    its weakest lines; the reviewer's `picks:` line is applied by `script_picks.py` — a punch-up, no extra round.
    fact_lint flags label-colon openers ("Hisaab: …").
  - Audience: `retention.py` maps a posted reel's Instagram retention points to the lines being said.
  - memes.py refuses unsafe titles (and templates whose own printed text is unsafe, by name).

- **Batches (`/batch-reels <first> <last> --pct-now N`, 2026-10-21):** one master session runs every scheduled reel
  in a date range (≤ 2 produce.py at once), decides stops like the creator via helper subagents, then analyses and
  optimises. `pipeline/budget.py` is the hard stop: armed with the weekly % now and a stop %, it converts ccusage
  dollars (every Claude session on the machine) to weekly % (cautious $4.5/%), and produce.py halts before any
  agent once the cap is spent.

Target per reel: agents ≈ $2.5–4, producer session ≤ $1 → **$3–5**. Check it in `notes/usage.md`; if a stage
runs over its share twice, fix the cause (a missing component, a vague note), not the cap.


**Quality gates (2026-10-21, from the 6-reel analysis):** a Culture now row that peaked ≤ 1 month ago is "now"; older
is an evergreen classic (creator's call: Bas karo bhai, Waiting Skeleton etc. are fine), ≤ 2 per reel
(CLAUDE.md §3); `fact_lint` sends a draft planning 3+ classics back to the writer before the review.
The polish pass also fixes qa's `late-text` / `empty-paper` warnings (blank paper fired on 5 of 6 reels and was
never routed). The script reviewer scores against anchors and writes an `evidence:` line (best / weakest line).
