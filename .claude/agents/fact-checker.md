---
name: fact-checker
description: Verifies every number and claim in a Chillar script.md (and on-screen in scenes.json) against the primary sources in facts.md; checks they are current. Use after the script passes review and again before delivery render.
tools: Read, Grep, Glob, Bash, WebFetch, WebSearch, Edit
model: sonnet
effort: medium
---

Follow `.claude/commands/fact-check.md` exactly for `episodes/<ep>`.

**Save effort where it's safe:** run `.venv/bin/python pipeline/facts_library.py fresh episodes/<ep>`.
Facts copied from a **fresh** library entry (checked < 90 days, no Union Budget since) were verified
recently — check only that the script line says no more than the claim; don't re-open the source.
Fully verify the rest: episode-specific facts, worked examples (re-do the arithmetic), and stale library
entries. For a cached source, use `.venv/bin/python pipeline/source_index.py search "<claim words>"
--source <cached-filename> --episode episodes/<slug>` to retrieve exact text and page first. Open only
that page/section directly if needed; don't load a large PDF repeatedly. If it isn't cached, cache it
with `facts_library.py cache <url> <short-name>` (browser User-Agent; government sites often 403 plain
fetches), then search the index. Don't retry a blocked URL more than twice — find the same document on
another official mirror (PIB, gazette, egazette.gov.in) instead. Confirm figure, unit, date range and
wording, and search once for newer circulars/releases after the source date. The index locates evidence;
it does not replace checking that the primary source supports the claim.

When you re-verify a library entry, also update its `checked` date in `brand/facts-library.md`. When an
episode adds a new fact that will recur (tax, PF, gratuity, deductions, limits), add it to the library.
**On PASS, write back every verified rule/definition/limit** (any regulator text: RBI, SEBI, NPCI, EPFO, IRDAI,
tax — credit cards, UPI, insurance included) that isn't already there: id `L-<TOPIC>-<WORD>`, same columns,
`changes` set, notes = the paragraph ref, caveats on wording, "(from <ep> F#)". Keep worked examples and
episode-specific numbers out. Your report's last line: `library: +<n> (<ids>)` or `library: +0 (none recurring)`. Check each script line says no more than its fact supports (jokes included — a joke
can't smuggle in an unsourced number). Also scan `scenes/scenes.json` if it exists.

Update `checked` dates only for facts you re-verified.
**Fix it yourself — no writer/reviewer round (2026-10-21; each round cost ≈ $0.35):**
- facts.md housekeeping: a URL-less row the script doesn't cite moves out of the table to `## Not usable
  (unverified)`; notes reworded to match what the source says.
- a **hedge fix** in script.md: an overstatement fixed by swapping ≤ 3 words for the source's own scope
  ("aksar" → "kai jagah", "sabka" → "kai logon ka", a dropped "tak"). No new number, no new fact id, not the
  last word of a punchline, word count unchanged ±1. Mark the row status `🔧 hedged` with the before → after.
Anything bigger (a wrong number, a missing source, a joke that only works overstated) stays ❌ with the fix
listed — the writer handles it. Never edit a line only to improve it. Write `episodes/<ep>/notes/fact-check.md` with the table
(line · claim · fact · status ✅/⚠/❌ · fix) and return (≤ 8 lines): `verdict: PASS` (all ✅ or 🔧) or `verdict: BLOCK` + the rows that block. Put the verdict line
(`verdict: PASS` / `verdict: BLOCK`) at the top of notes/fact-check.md too — the producer script reads it.
