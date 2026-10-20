# Production line — how work is routed, and what it costs

## Agents (`.claude/agents/`), one job each; `pipeline/produce.py` routes them
| agent | model · effort | does | loop |
|---|---|---|---|
| `researcher` | sonnet · medium | library facts first, then primary-source gaps → `facts.md` (+ library) | |
| `scriptwriter` | opus · high | writes/rewrites script.md (jokes, puns, meme refs, facts cited) | ⇄ script-reviewer, ≤ 3 rounds |
| `script-reviewer` | opus · high | scores + line notes → `notes/script-review-<n>.md`, PASS/REVISE | |
| `fact-checker` | sonnet · medium | verifies claims → `notes/fact-check.md`, PASS/BLOCK | BLOCK → scriptwriter |
| `director` | opus · high | script + words.json → `scenes/scenes.json` (visuals, fields, stamps, cuts) | ⇄ video-reviewer |
| `editor` | sonnet · medium | rhythm, cut points, comedic timing, transitions, SFX in scenes.json | ⇄ video-reviewer |
| `video-reviewer` | sonnet · medium | judges taste/comedy/retention on top of `qa.py` → `notes/video-review-<n>.md` | ≤ 3 rounds |
| `component-dev` | sonnet · medium | fixes `[component:<name>]` review notes in `components/` (only when routed) | in the edit loop |
| `voice` | sonnet · medium | `voice/tts.txt` → Sunny voice → pronunciation check | |
| `packager` | sonnet · medium | `output/post.md` (caption, pinned math, sources) | |
Quality is decided by the writer, the script reviewer and the director — they keep the strongest
model. The others do lookup, arithmetic and checking. Simple file chores and graphify extraction: haiku.
After 3 rounds without PASS, stop and ask the creator.

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
- **Real cost per run** (`total_cost_usd`) → `notes/usage.jsonl` → `notes/usage.md`; `--max-budget-usd`
  caps per agent (BUDGET in produce.py) are safety nets, not targets.
- **Cost and quality together:** `usage.md` reports prompt characters, cached-read tokens and stage cost beside
  the latest script scores, video swipe-risk/blocker/polish counts and final mechanical QA. Lower cost is not a
  win if quality signals regress.
- **Fewer wasted rounds:** fact_lint's script self-check (spoken length with numbers in full at the measured
  3.2 words/s + outro, laugh margin, first laugh, absolutes on cited lines, long lines); qa's layout warnings
  (`narrow-frame`, `small-text`, `same-layout`) + `layout` boxes in qa.json; frames.py deletes stale frames;
  the reviewer measures from qa, not half-size frames; align pads 1 s so the last line can't collapse.

Target per reel: agents ≈ $2.5–4, producer session ≤ $1 → **$3–5**. Check it in `notes/usage.md`; if a stage
runs over its share twice, fix the cause (a missing component, a vague note), not the cap.

