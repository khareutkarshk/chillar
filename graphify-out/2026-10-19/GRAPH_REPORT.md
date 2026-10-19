# Graph Report - chillar  (2026-10-19)

## Corpus Check
- 108 files · ~39,275 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 380 nodes · 693 edges · 46 communities (43 shown, 3 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 49 edges (avg confidence: 0.83)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `19bd4d0b`
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
- audio_clean.py
- setup.sh
- ig_export.py
- mix.py
- chillar.js
- glyph_check.py
- chillar-reels
- CompletedProcess

## God Nodes (most connected - your core abstractions)
1. `Candidate` - 39 edges
2. `CLAUDE.md brand bible` - 23 edges
3. `12 LPA episode script.md` - 16 edges
4. `LicenseRefused` - 13 edges
5. `director agent` - 12 edges
6. `/make-reel command` - 12 edges
7. `12 LPA episode facts.md` - 11 edges
8. `env()` - 10 edges
9. `scriptwriter agent` - 10 edges
10. `/render command` - 10 edges

## Surprising Connections (you probably didn't know these)
- `Note Fields design (rupee-note colour fields)` --semantically_similar_to--> `Chapters = rupee-note colour fields (₹10→₹20→₹50→₹500, ₹2000 for twists)`  [INFERRED] [semantically similar]
  README.md → .claude/agents/director.md
- `12 LPA episode script.md` --references--> `Chillar series: Chillar in 60, Chillar Report, Myth vs Math, ₹100 vs ₹1,00,000`  [INFERRED]
  episodes/2026-10-12lpa-in-hand/script.md → CLAUDE.md
- `12 LPA episode cover.md` --references--> `Theme selection: pastel / calm / night`  [INFERRED]
  episodes/2026-10-12lpa-in-hand/cover.md → .claude/agents/director.md
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

## Communities (46 total, 3 thin omitted)

### Community 0 - "Candidate"
Cohesion: 0.06
Nodes (68): Exception, Candidate, env(), polite_sleep(), Shared paths, env, HTTP session and politeness helpers., One downloadable asset. `verify()` must be called right before download., text_of(), check_policy() (+60 more)

### Community 1 - "CLAUDE.md brand bible"
Cohesion: 0.07
Nodes (59): director agent, @chillar.ind wordmark (x 72-492, y 1460-1500), Motivated transitions (hard cut default; whip/zoom/wipe/page budgeted), No on-screen structure labels rule, Chapters = rupee-note colour fields (₹10→₹20→₹50→₹500, ₹2000 for twists), scenes/scenes.json shot plan, Show, don't caption, Theme selection: pastel / calm / night (+51 more)

### Community 2 - "build_composition.py"
Cohesion: 0.23
Nodes (10): all_components(), build(), component_meta(), merged_params(), Path, demo_captions(), main(), cover() (+2 more)

### Community 3 - "episode.py"
Cohesion: 0.08
Nodes (27): align(), _model(), Path, Episode, frontmatter(), Line, load(), norm() (+19 more)

### Community 4 - "fetch_assets.py"
Cohesion: 0.22
Nodes (19): /fetch-assets command, Asset licensing allow-list (CC0/MIT etc.), build_audition(), _diverse(), duration_of(), fetch(), ingest(), lock() (+11 more)

### Community 5 - "12 LPA episode script.md"
Cohesion: 0.26
Nodes (18): mithai-dabba component (laddoo deductions), 12 LPA episode cover.md, 12 LPA episode facts.md, F1 new-regime tax slabs, F10 EPF partial withdrawal after 12 months, F2 no tax up to ₹12 lakh (₹12.75 lakh salaried) rebate, F3 Income-tax Act 2025 from Apr 2026, F4 EPF 12% employee + 12% employer (+10 more)

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

### Community 11 - "ig_export.py"
Cohesion: 0.40
Nodes (9): atoms(), check(), encode_args(), keyframe_gap(), probe(), Path, ffmpeg output args: H.264 High 4:2:0, 30 fps CFR, 1 s closed GOP, capped VBR,…, Top-level MP4 atoms in file order. (+1 more)

### Community 12 - "mix.py"
Cohesion: 0.50
Nodes (8): CompletedProcess, ff(), loudnorm_2pass(), lufs(), mix(), Path, resolve_music(), resolve_sound()

### Community 14 - "chillar.js"
Cohesion: 0.83
Nodes (3): brow(), eye(), svg()

## Knowledge Gaps
- **12 isolated node(s):** `name`, `private`, `description`, `node`, `doctor` (+7 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Candidate` connect `Candidate` to `fetch_assets.py`?**
  _High betweenness centrality (0.085) - this node is a cross-community bridge._
- **Why does `CLAUDE.md brand bible` connect `CLAUDE.md brand bible` to `tts.py`, `episode.py`, `fetch_assets.py`?**
  _High betweenness centrality (0.077) - this node is a cross-community bridge._
- **Why does `Episode` connect `episode.py` to `audio_clean.py`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `12 LPA episode script.md` (e.g. with `12 LPA episode cover.md` and `Chillar series: Chillar in 60, Chillar Report, Myth vs Math, ₹100 vs ₹1,00,000`) actually correct?**
  _`12 LPA episode script.md` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `name`, `private`, `description` to the rest of the system?**
  _12 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Candidate` be split into smaller, more focused modules?**
  _Cohesion score 0.05842259006815969 - nodes in this community are weakly interconnected._
- **Should `CLAUDE.md brand bible` be split into smaller, more focused modules?**
  _Cohesion score 0.0655367231638418 - nodes in this community are weakly interconnected._