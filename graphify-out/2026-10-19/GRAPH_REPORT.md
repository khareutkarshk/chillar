# Graph Report - /home/khare/Desktop/chillar  (2026-10-19)

## Corpus Check
- Corpus is ~39,131 words - fits in a single context window. You may not need a graph.

## Summary
- 379 nodes · 693 edges · 45 communities (43 shown, 2 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 49 edges (avg confidence: 0.83)
- Token cost: 80,319 input · 0 output

## Community Hubs (Navigation)
- Asset Fetching & Sources
- Agents & Brand Rules
- Composition Builder & Gallery
- Episode Loading & Alignment
- Asset Licensing & Audition
- 12 LPA Episode & Facts
- Node Deps (GSAP, HyperFrames)
- Contact Sheet & Palette Check
- Voiceover (Sarvam TTS)
- Voice Cleanup
- Setup Script
- Instagram Export Gate
- Audio Mix
- Mascot SVG
- Font Glyph Check
- Project Root

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

## Communities (45 total, 2 thin omitted)

### Community 0 - "Asset Fetching & Sources"
Cohesion: 0.06
Nodes (69): Exception, Candidate, env(), polite_sleep(), Shared paths, env, HTTP session and politeness helpers., One downloadable asset. `verify()` must be called right before download., slug(), text_of() (+61 more)

### Community 1 - "Agents & Brand Rules"
Cohesion: 0.07
Nodes (59): director agent, @chillar.ind wordmark (x 72-492, y 1460-1500), Motivated transitions (hard cut default; whip/zoom/wipe/page budgeted), No on-screen structure labels rule, Chapters = rupee-note colour fields (₹10→₹20→₹50→₹500, ₹2000 for twists), scenes/scenes.json shot plan, Show, don't caption, Theme selection: pastel / calm / night (+51 more)

### Community 2 - "Composition Builder & Gallery"
Cohesion: 0.12
Nodes (20): all_components(), build(), component_meta(), merged_params(), Path, demo_captions(), main(), cover() (+12 more)

### Community 3 - "Episode Loading & Alignment"
Cohesion: 0.12
Nodes (17): align(), _model(), Path, Episode, frontmatter(), Line, load(), norm() (+9 more)

### Community 4 - "Asset Licensing & Audition"
Cohesion: 0.22
Nodes (18): /fetch-assets command, Asset licensing allow-list (CC0/MIT etc.), build_audition(), _diverse(), duration_of(), fetch(), ingest(), lock() (+10 more)

### Community 5 - "12 LPA Episode & Facts"
Cohesion: 0.26
Nodes (18): mithai-dabba component (laddoo deductions), 12 LPA episode cover.md, 12 LPA episode facts.md, F1 new-regime tax slabs, F10 EPF partial withdrawal after 12 months, F2 no tax up to ₹12 lakh (₹12.75 lakh salaried) rebate, F3 Income-tax Act 2025 from Apr 2026, F4 EPF 12% employee + 12% employer (+10 more)

### Community 6 - "Node Deps (GSAP, HyperFrames)"
Cohesion: 0.14
Nodes (13): gsap, hyperframes, description, devDependencies, gsap, hyperframes, engines, node (+5 more)

### Community 7 - "Contact Sheet & Palette Check"
Cohesion: 0.24
Nodes (12): Image, frame_at(), guides(), off_palette(), pal_array(), ndarray, Path, sheet() (+4 more)

### Community 8 - "Voiceover (Sarvam TTS)"
Cohesion: 0.35
Nodes (10): Voiceover policy (Sarvam sunny_hi_reels, pace 1.2, every reel), audition_page(), chunks(), concat(), duration(), kokoro(), main(), Path (+2 more)

### Community 9 - "Voice Cleanup"
Cohesion: 0.33
Nodes (10): clean(), ff(), find_voice(), has_filter(), loudnorm(), CompletedProcess, ndarray, Path (+2 more)

### Community 10 - "Setup Script"
Cohesion: 0.33
Nodes (10): can_sudo(), fail(), fetch_font(), have(), pass(), PATH, RESULTS, setup.sh script (+2 more)

### Community 11 - "Instagram Export Gate"
Cohesion: 0.40
Nodes (9): atoms(), check(), encode_args(), keyframe_gap(), probe(), Path, ffmpeg output args: H.264 High 4:2:0, 30 fps CFR, 1 s closed GOP, capped VBR,…, Top-level MP4 atoms in file order. (+1 more)

### Community 12 - "Audio Mix"
Cohesion: 0.50
Nodes (8): ff(), loudnorm_2pass(), lufs(), mix(), CompletedProcess, Path, resolve_music(), resolve_sound()

### Community 14 - "Mascot SVG"
Cohesion: 0.83
Nodes (3): brow(), eye(), svg()

## Knowledge Gaps
- **12 isolated node(s):** `name`, `private`, `description`, `node`, `doctor` (+7 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Candidate` connect `Asset Fetching & Sources` to `Asset Licensing & Audition`?**
  _High betweenness centrality (0.086) - this node is a cross-community bridge._
- **Why does `CLAUDE.md brand bible` connect `Agents & Brand Rules` to `Voiceover (Sarvam TTS)`, `Composition Builder & Gallery`, `Asset Licensing & Audition`?**
  _High betweenness centrality (0.078) - this node is a cross-community bridge._
- **Why does `Episode` connect `Episode Loading & Alignment` to `Voice Cleanup`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `12 LPA episode script.md` (e.g. with `12 LPA episode cover.md` and `Chillar series: Chillar in 60, Chillar Report, Myth vs Math, ₹100 vs ₹1,00,000`) actually correct?**
  _`12 LPA episode script.md` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `name`, `private`, `description` to the rest of the system?**
  _12 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Asset Fetching & Sources` be split into smaller, more focused modules?**
  _Cohesion score 0.058544303797468354 - nodes in this community are weakly interconnected._
- **Should `Agents & Brand Rules` be split into smaller, more focused modules?**
  _Cohesion score 0.0655367231638418 - nodes in this community are weakly interconnected._