---
description: Create a new Chillar episode — research sourced facts, cover, then the writers' room (scriptwriter ⇄ script-reviewer) writes the Hinglish script
argument-hint: <topic> [30|60|90]
---

Create a new Chillar Reel episode about: **$ARGUMENTS** (format 30 / 60 / 90 s; default 60).

Follow CLAUDE.md exactly (brand bible §1–§4, content rules §3). Steps:

1. **Folder.** Pick a slug `YYYY-MM-<short-topic>` (today's year-month). `cp -r episodes/_template episodes/<slug>`.
   Pick the series that fits (Chillar in 60 / Chillar Report / Myth vs Math / ₹100 vs ₹1,00,000).
   Set `target_seconds` in script.md frontmatter to the format.

2. **Library first, then research.** `.venv/bin/python pipeline/facts_library.py list` — copy every
   recurring fact the topic needs from `brand/facts-library.md` with
   `facts_library.py copy episodes/<slug> L-… L-…` (they arrive as F# rows with source + checked date).
   Research only what the library doesn't have. Use WebSearch/WebFetch (cache primary-source PDFs with
   `facts_library.py cache <url> <name>` and read the local copy). Prefer primary sources (RBI, NPCI, SEBI,
   PIB, gazette notifications, ministry releases, company filings). For each fact add a row to
   `facts.md`: id, claim, source URL, today's date in `checked`, notes (what page/section; anything
   disputed or recently changed). Read the source itself — don't cite a news article for a number the
   primary source publishes. Gather a few more facts than you need: the writers need material.
   Also note 3–5 *texture* details (how people actually experience this topic in India) for the writers.
   Add any new fact that will recur in other reels to `brand/facts-library.md` too.

3. **Cover before script.** Fill `cover.md`: cover_text ≤ 5 words (honest — the payoff must deliver
   it), kicker, optional stamp word, Chillar expression, cover_field, the first frame (must show the
   stakes) and the hook line (sentence 1 = the question).

4. **Writers' room** (max 3 rounds): `scriptwriter` agent writes `script.md` → `script-reviewer` agent
   returns PASS/REVISE in `notes/script-review-<n>.md` → on REVISE, a **new** `scriptwriter` agent
   rewrites from the notes file (never resume an earlier agent — the files carry the state). Stop at PASS; after round 3 show me the last notes and ask.

5. Run `.venv/bin/python pipeline/fact_lint.py episodes/<slug>` and fix anything it flags.

6. Report back: cover text, hook line, word count + estimated seconds, laugh count + the three best
   jokes, review rounds used, and any fact you're unsure about. Next: `/fact-check`, then `/voiceover` (Sunny).
