# Graph Report - chillar  (2026-10-20)

## Corpus Check
- 141 files · ~71,700 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 574 nodes · 963 edges · 77 communities (60 shown, 17 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 58 edges (avg confidence: 0.78)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `fe06b9a3`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Candidate
- CLAUDE.md brand bible
- build_composition.py
- episode.py
- fetch_assets.py
- 12 LPA episode script.md
- package.json
- contact_sheet.py
- tts.py
- 2026-10-chai-vs-phone/script.md
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
- Comedy craft — how a Chillar script gets funny
- 2026-10-credit-card-myth/script.md
- 2026-10-credit-card-myth/cover.md
- Facts — 2026-10-credit-card-myth
- qa.py
- 2026-10-chai-vs-phone/cover.md
- Facts — 2026-10-chai-vs-phone
- make_reel.py
- director agent
- fact_lint.py
- /make-reel command
- validate_scenes.py
- align.py

## God Nodes (most connected - your core abstractions)
1. `Candidate` - 39 edges
2. `CLAUDE.md brand bible` - 23 edges
3. `Component catalog (generated — `pipeline/component_catalog.py`, don't edit)` - 22 edges
4. `Line` - 18 edges
5. `12 LPA episode script.md` - 16 edges
6. `qa()` - 14 edges
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
- `/new-reel command` --references--> `template facts.md`  [INFERRED]
  .claude/commands/new-reel.md → episodes/_template/facts.md
- `12 LPA episode script.md` --implements--> `Thappa red rubber stamp (2-3 per video)`  [INFERRED]
  episodes/2026-10-12lpa-in-hand/script.md → CLAUDE.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Writers' room loop (scriptwriter ⇄ script-reviewer, fact-checker)** — _claude_agents_scriptwriter, _claude_agents_script_reviewer, _claude_agents_fact_checker, _claude_commands_new_reel, _claude_commands_make_reel [EXTRACTED 1.00]
- **Edit suite loop (director → editor → render → video-reviewer)** — _claude_agents_director, _claude_agents_editor, _claude_agents_video_reviewer, _claude_commands_render, _claude_agents_director_scenes_json, pipeline_make_reel [EXTRACTED 1.00]
- **12 LPA CTC → ₹86,468 in-hand computation** — episodes_2026_10_12lpa_in_hand_facts_f9, episodes_2026_10_12lpa_in_hand_facts_f1, episodes_2026_10_12lpa_in_hand_facts_f2, episodes_2026_10_12lpa_in_hand_facts_f4, episodes_2026_10_12lpa_in_hand_facts_f6, episodes_2026_10_12lpa_in_hand_facts_f7, episodes_2026_10_12lpa_in_hand_facts_f8 [EXTRACTED 1.00]

## Communities (77 total, 17 thin omitted)

### Community 0 - "Candidate"
Cohesion: 0.06
Nodes (69): Exception, Candidate, env(), polite_sleep(), Shared paths, env, HTTP session and politeness helpers., One downloadable asset. `verify()` must be called right before download., slug(), text_of() (+61 more)

### Community 1 - "CLAUDE.md brand bible"
Cohesion: 0.13
Nodes (21): Script review rubric (stop power, laughs, specificity, clarity, escalation, payoff, speakability, facts), 3-second brand test on every frame, /package command, Bricolage Grotesque cover font, Cover package scoring (curiosity, clarity, honesty ≥4), output/post.md Instagram caption, CLAUDE.md brand bible, Bricolage Grotesque / Mukta / JetBrains Mono typography (+13 more)

### Community 2 - "build_composition.py"
Cohesion: 0.23
Nodes (10): all_components(), build(), component_meta(), merged_params(), Path, demo_captions(), main(), cover() (+2 more)

### Community 3 - "episode.py"
Cohesion: 0.09
Nodes (26): clean(), ff(), find_voice(), has_filter(), loudnorm(), CompletedProcess, ndarray, Path (+18 more)

### Community 4 - "fetch_assets.py"
Cohesion: 0.22
Nodes (18): /fetch-assets command, Asset licensing allow-list (CC0/MIT etc.), build_audition(), _diverse(), duration_of(), fetch(), ingest(), lock() (+10 more)

### Community 5 - "12 LPA episode script.md"
Cohesion: 0.24
Nodes (19): Theme selection: pastel / calm / night, mithai-dabba component (laddoo deductions), 12 LPA episode cover.md, 12 LPA episode facts.md, F1 new-regime tax slabs, F10 EPF partial withdrawal after 12 months, F2 no tax up to ₹12 lakh (₹12.75 lakh salaried) rebate, F3 Income-tax Act 2025 from Apr 2026 (+11 more)

### Community 6 - "package.json"
Cohesion: 0.14
Nodes (13): gsap, hyperframes, description, devDependencies, gsap, hyperframes, engines, node (+5 more)

### Community 7 - "contact_sheet.py"
Cohesion: 0.24
Nodes (12): Image, frame_at(), guides(), off_palette(), pal_array(), ndarray, Path, sheet() (+4 more)

### Community 8 - "tts.py"
Cohesion: 0.40
Nodes (9): audition_page(), chunks(), concat(), duration(), kokoro(), main(), Path, sarvam() (+1 more)

### Community 9 - "2026-10-chai-vs-phone/script.md"
Cohesion: 0.40
Nodes (4): Escalation {field: note50}, Hook {field: note10}, Payoff {field: note500}, Setup {field: note20}

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
Cohesion: 0.48
Nodes (6): entry(), main(), A default the director can copy without opening component.json: lists of…, render(), short(), stale()

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
Cohesion: 0.15
Nodes (32): director(), draft(), duration(), find_cli(), frontmatter(), length_miss(), Line, main() (+24 more)

### Community 64 - "Comedy craft — how a Chillar script gets funny"
Cohesion: 0.25
Nodes (7): 1. The voice, 2. One game per reel (the single biggest upgrade), 3. Where laughs come from (patterns to learn, not lines to copy), 4. Anti-AI writing (the script-reviewer fails these), 5. Writing process (do all of it — the reviewer can tell), 6. Format notes, Comedy craft — how a Chillar script gets funny

### Community 65 - "2026-10-credit-card-myth/script.md"
Cohesion: 0.50
Nodes (3): Hook {field: note10}, Payoff {field: note2000}, Turn {field: note500}

### Community 68 - "qa.py"
Cohesion: 0.17
Nodes (20): area(), audio_check(), centre_in(), chrome_path(), contrast(), digits(), glyph_lines(), inr() (+12 more)

### Community 71 - "make_reel.py"
Cohesion: 0.19
Nodes (12): Chapters = rupee-note colour fields (₹10→₹20→₹50→₹500, ₹2000 for twists), Editor passes: rhythm, cut points, comedic timing, transitions, sound, overlays, igcheck stage (upload-safe), brand/tokens.json, make_reel.py pipeline stages (clean→align→validate→build→render→mix→cover→sheet), Sound design: sonic signature, max one SFX / 2 s, -14 LUFS, main(), CompletedProcess (+4 more)

### Community 72 - "director agent"
Cohesion: 0.27
Nodes (12): director agent, @chillar.ind wordmark (x 72-492, y 1460-1500), Motivated transitions (hard cut default; whip/zoom/wipe/page budgeted), No on-screen structure labels rule, scenes/scenes.json shot plan, Show, don't caption, editor agent, video-reviewer agent (+4 more)

### Community 73 - "fact_lint.py"
Cohesion: 0.24
Nodes (11): fact-checker agent, /fact-check command, Fact-check status table (✅ / ⚠ / ❌), Every fact cited with [F#] id + source URL, template facts.md, lint(), main(), How many words the voice says for a written number token (Hinglish/English… (+3 more)

### Community 74 - "/make-reel command"
Cohesion: 0.38
Nodes (10): script-reviewer agent, scriptwriter agent, Reel format table (30/60/90 s: words, chapters, laughs, re-hook cadence), Joke craft (specificity, self-roast, rule of three, deadpan tag, callbacks), [JOKE] laugh-line marker, /make-reel command, /new-reel command, /voiceover command (+2 more)

### Community 75 - "validate_scenes.py"
Cohesion: 0.36
Nodes (7): caption_groups(), chapter_starts(), Ctx, main(), Every string a viewer could read in a params tree., resolve(), strings()

### Community 76 - "align.py"
Cohesion: 0.47
Nodes (5): align(), _model(), Path, The same timings as words.json in ~⅓ of the tokens, for the agents (one script…, words_txt()

## Knowledge Gaps
- **88 isolated node(s):** `avatar`, `bar-chart`, `calendar-flip`, `checklist`, `cover` (+83 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **17 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `words_txt()` connect `align.py` to `produce.py`?**
  _High betweenness centrality (0.075) - this node is a cross-community bridge._
- **Why does `st_edit()` connect `produce.py` to `align.py`?**
  _High betweenness centrality (0.071) - this node is a cross-community bridge._
- **Why does `Candidate` connect `Candidate` to `fetch_assets.py`?**
  _High betweenness centrality (0.048) - this node is a cross-community bridge._
- **What connects `avatar`, `bar-chart`, `calendar-flip` to the rest of the system?**
  _88 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Candidate` be split into smaller, more focused modules?**
  _Cohesion score 0.058544303797468354 - nodes in this community are weakly interconnected._
- **Should `CLAUDE.md brand bible` be split into smaller, more focused modules?**
  _Cohesion score 0.12857142857142856 - nodes in this community are weakly interconnected._
- **Should `episode.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08571428571428572 - nodes in this community are weakly interconnected._