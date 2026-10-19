# Graph Report - chillar  (2026-10-20)

## Corpus Check
- 137 files · ~65,736 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 550 nodes · 935 edges · 69 communities (54 shown, 15 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 65 edges (avg confidence: 0.78)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e36e3e07`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Candidate
- CLAUDE.md brand bible
- make_reel.py
- episode.py
- fetch_assets.py
- 12 LPA episode script.md
- package.json
- contact_sheet.py
- tts.py
- audio_clean.py
- setup.sh
- mix.py
- Component catalog (generated — `pipeline/component_catalog.py`, don't edit)
- chillar.js
- glyph_check.py
- chillar-reels
- facts_library.py
- Production line — how work is routed, and what it costs
- component_catalog.py
- qa_probe.mjs
- facts-library.md
- formats.md
- instagram.md
- sound.md
- themes.md
- voice.md
- script.md
- Posting schedule — one Reel every day
- Facts — 2026-10-epf-explained
- cover.md
- produce.py
- component-dev.md
- packager.md
- researcher.md
- agents/voice.md
- Comedy craft — how a Chillar joke is built
- 2026-10-credit-card-myth/script.md
- 2026-10-credit-card-myth/cover.md
- Facts — 2026-10-credit-card-myth
- qa.py

## God Nodes (most connected - your core abstractions)
1. `Candidate` - 39 edges
2. `CLAUDE.md brand bible` - 23 edges
3. `Component catalog (generated — `pipeline/component_catalog.py`, don't edit)` - 22 edges
4. `Line` - 16 edges
5. `qa()` - 16 edges
6. `12 LPA episode script.md` - 16 edges
7. `LicenseRefused` - 13 edges
8. `director agent` - 12 edges
9. `/make-reel command` - 12 edges
10. `12 LPA episode facts.md` - 11 edges

## Surprising Connections (you probably didn't know these)
- `Note Fields design (rupee-note colour fields)` --semantically_similar_to--> `Chapters = rupee-note colour fields (₹10→₹20→₹50→₹500, ₹2000 for twists)`  [INFERRED] [semantically similar]
  README.md → .claude/agents/director.md
- `12 LPA episode script.md` --references--> `Chillar series: Chillar in 60, Chillar Report, Myth vs Math, ₹100 vs ₹1,00,000`  [INFERRED]
  episodes/2026-10-12lpa-in-hand/script.md → CLAUDE.md
- `/new-reel command` --references--> `template cover.md`  [INFERRED]
  .claude/commands/new-reel.md → episodes/_template/cover.md
- `12 LPA episode script.md` --implements--> `Thappa red rubber stamp (2-3 per video)`  [INFERRED]
  episodes/2026-10-12lpa-in-hand/script.md → CLAUDE.md
- `Script review rubric (stop power, laughs, specificity, clarity, escalation, payoff, speakability, facts)` --implements--> `Formats + retention (30/60/90 s)`  [INFERRED]
  .claude/agents/script-reviewer.md → CLAUDE.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Writers' room loop (scriptwriter ⇄ script-reviewer, fact-checker)** — _claude_agents_scriptwriter, _claude_agents_script_reviewer, _claude_agents_fact_checker, _claude_commands_new_reel, _claude_commands_make_reel [EXTRACTED 1.00]
- **Edit suite loop (director → editor → render → video-reviewer)** — _claude_agents_director, _claude_agents_editor, _claude_agents_video_reviewer, _claude_commands_render, _claude_agents_director_scenes_json, pipeline_make_reel [EXTRACTED 1.00]
- **12 LPA CTC → ₹86,468 in-hand computation** — episodes_2026_10_12lpa_in_hand_facts_f9, episodes_2026_10_12lpa_in_hand_facts_f1, episodes_2026_10_12lpa_in_hand_facts_f2, episodes_2026_10_12lpa_in_hand_facts_f4, episodes_2026_10_12lpa_in_hand_facts_f6, episodes_2026_10_12lpa_in_hand_facts_f7, episodes_2026_10_12lpa_in_hand_facts_f8 [EXTRACTED 1.00]

## Communities (69 total, 15 thin omitted)

### Community 0 - "Candidate"
Cohesion: 0.06
Nodes (69): Exception, Candidate, env(), polite_sleep(), Shared paths, env, HTTP session and politeness helpers., One downloadable asset. `verify()` must be called right before download., slug(), text_of() (+61 more)

### Community 1 - "CLAUDE.md brand bible"
Cohesion: 0.06
Nodes (60): director agent, @chillar.ind wordmark (x 72-492, y 1460-1500), Motivated transitions (hard cut default; whip/zoom/wipe/page budgeted), No on-screen structure labels rule, Chapters = rupee-note colour fields (₹10→₹20→₹50→₹500, ₹2000 for twists), scenes/scenes.json shot plan, Show, don't caption, editor agent (+52 more)

### Community 2 - "make_reel.py"
Cohesion: 0.12
Nodes (20): all_components(), build(), component_meta(), merged_params(), Path, demo_captions(), main(), cover() (+12 more)

### Community 3 - "episode.py"
Cohesion: 0.10
Nodes (20): align(), _model(), Path, grab(), main(), Path, Episode, frontmatter() (+12 more)

### Community 4 - "fetch_assets.py"
Cohesion: 0.22
Nodes (18): /fetch-assets command, Asset licensing allow-list (CC0/MIT etc.), build_audition(), _diverse(), duration_of(), fetch(), ingest(), lock() (+10 more)

### Community 5 - "12 LPA episode script.md"
Cohesion: 0.21
Nodes (21): Theme selection: pastel / calm / night, Chillar ₹1 coin mascot (8 expressions), mithai-dabba component (laddoo deductions), 12 LPA episode cover.md, 12 LPA episode facts.md, F1 new-regime tax slabs, F10 EPF partial withdrawal after 12 months, F2 no tax up to ₹12 lakh (₹12.75 lakh salaried) rebate (+13 more)

### Community 6 - "package.json"
Cohesion: 0.14
Nodes (13): gsap, hyperframes, description, devDependencies, gsap, hyperframes, engines, node (+5 more)

### Community 7 - "contact_sheet.py"
Cohesion: 0.24
Nodes (12): Image, frame_at(), guides(), off_palette(), pal_array(), ndarray, Path, sheet() (+4 more)

### Community 8 - "tts.py"
Cohesion: 0.35
Nodes (10): Voiceover policy (Sarvam sunny_hi_reels, pace 1.2, every reel), audition_page(), chunks(), concat(), duration(), kokoro(), main(), Path (+2 more)

### Community 9 - "audio_clean.py"
Cohesion: 0.33
Nodes (10): clean(), ff(), find_voice(), has_filter(), loudnorm(), CompletedProcess, ndarray, Path (+2 more)

### Community 10 - "setup.sh"
Cohesion: 0.33
Nodes (10): can_sudo(), fail(), fetch_font(), have(), pass(), PATH, RESULTS, setup.sh script (+2 more)

### Community 11 - "mix.py"
Cohesion: 0.22
Nodes (17): atoms(), check(), encode_args(), keyframe_gap(), probe(), Path, ffmpeg output args: H.264 High 4:2:0, 30 fps CFR, 1 s closed GOP, capped VBR,…, Top-level MP4 atoms in file order. (+9 more)

### Community 12 - "Component catalog (generated — `pipeline/component_catalog.py`, don't edit)"
Cohesion: 0.07
Nodes (27): avatar, bar-chart, calendar-flip, captions  _(auto — never place in scenes.json)_, chapter-field  _(auto — never place in scenes.json)_, checklist, Component catalog (generated — `pipeline/component_catalog.py`, don't edit), cover (+19 more)

### Community 14 - "chillar.js"
Cohesion: 0.83
Nodes (3): brow(), eye(), svg()

### Community 45 - "facts_library.py"
Cohesion: 0.47
Nodes (9): date, cmd_cache(), cmd_copy(), cmd_fresh(), entries(), main(), next_fid(), Path (+1 more)

### Community 46 - "Production line — how work is routed, and what it costs"
Cohesion: 0.22
Nodes (8): Agents (`.claude/agents/`), one job each; `pipeline/produce.py` routes them, Facts, Hand-offs: fresh agents, files carry the state, Image budget (a full 1080×1920 frame ≈ 1.5k tokens every time it's viewed), Mechanical QA before taste, Production line — how work is routed, and what it costs, Session hygiene, The cheap way to run it: `pipeline/produce.py` (since 2026-10-19)

### Community 47 - "component_catalog.py"
Cohesion: 0.60
Nodes (5): entry(), main(), render(), short(), stale()

### Community 48 - "qa_probe.mjs"
Cohesion: 0.38
Nodes (6): env(), ownBg(), probeClip(), puppeteer, req, require

### Community 55 - "script.md"
Cohesion: 0.40
Nodes (4): Escalation {field: note50}, Hook {field: note10}, Payoff {field: note500}, Setup {field: note20}

### Community 56 - "Posting schedule — one Reel every day"
Cohesion: 0.33
Nodes (5): A production day (one reel, made the day before it posts), Posting schedule — one Reel every day, The week, Topic backlog (starter — education only, no products, no return promises), Weekly rhythm

### Community 57 - "Facts — 2026-10-epf-explained"
Cohesion: 0.50
Nodes (3): Facts — 2026-10-epf-explained, Texture for the writers (not facts — don't put numbers from here on screen), Worked example (F19) — computed with python, rounded to whole rupees

### Community 59 - "produce.py"
Cohesion: 0.21
Nodes (23): draft(), find_cli(), frontmatter(), Line, main(), Path, The creator's 'fix it and ship' after a 3-round stop: the routed roles apply…, Newest Claude Code binary: $CHILLAR_CLAUDE, the VS Code extension's bundled… (+15 more)

### Community 64 - "Comedy craft — how a Chillar joke is built"
Cohesion: 0.29
Nodes (6): Comedy craft — how a Chillar joke is built, Kill list (the reviewer fails these), Structure of a 30 s Myth vs Math (≈ 80 words), The 10 moves (each draft uses at least 5 different ones), The voice in one line, Writing process (do it, don't skip it)

### Community 65 - "2026-10-credit-card-myth/script.md"
Cohesion: 0.50
Nodes (3): Hook {field: note10}, Payoff {field: note2000}, Turn {field: note500}

### Community 68 - "qa.py"
Cohesion: 0.17
Nodes (20): area(), audio_check(), centre_in(), chrome_path(), contrast(), digits(), glyph_lines(), inr() (+12 more)

## Knowledge Gaps
- **80 isolated node(s):** `name`, `private`, `description`, `node`, `doctor` (+75 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **15 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `clean()` connect `audio_clean.py` to `produce.py`?**
  _High betweenness centrality (0.051) - this node is a cross-community bridge._
- **Why does `Candidate` connect `Candidate` to `fetch_assets.py`?**
  _High betweenness centrality (0.051) - this node is a cross-community bridge._
- **Why does `st_fix()` connect `produce.py` to `audio_clean.py`?**
  _High betweenness centrality (0.049) - this node is a cross-community bridge._
- **What connects `name`, `private`, `description` to the rest of the system?**
  _80 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Candidate` be split into smaller, more focused modules?**
  _Cohesion score 0.058544303797468354 - nodes in this community are weakly interconnected._
- **Should `CLAUDE.md brand bible` be split into smaller, more focused modules?**
  _Cohesion score 0.06284153005464481 - nodes in this community are weakly interconnected._
- **Should `make_reel.py` be split into smaller, more focused modules?**
  _Cohesion score 0.12433862433862433 - nodes in this community are weakly interconnected._