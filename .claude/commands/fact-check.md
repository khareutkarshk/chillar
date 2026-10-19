---
description: Verify every number and claim in script.md (and on-screen in scenes.json) against facts.md sources
argument-hint: <episode folder or slug>
---

Fact-check episode **$ARGUMENTS**.

1. Run `.venv/bin/python pipeline/fact_lint.py episodes/<slug> --json` — mechanical gaps first
   (uncited numbers, missing URLs, stale `checked` dates, ids that don't exist).

2. For **every** fact in `facts.md` that the script cites: open the source URL (WebFetch; for PDFs
   read the PDF) and confirm the exact figure, unit, date range and wording. Check it's still current:
   search for newer releases / amendments / circulars after the source date (laws and RBI/NPCI rules
   change — e.g. MDR rules changed in Aug 2026). Prefer the primary source over news.

3. Check each script line says no more than its fact supports (no rounding that changes meaning,
   no "always/never" the source doesn't say, years and FY labels right, ₹ crore vs lakh right,
   Indian number grouping right).

4. Also scan `scenes/scenes.json` params: every number shown on screen must match a fact.

5. Output a table: line id · claim as written · fact id · status (✅ verified / ⚠ outdated /
   ⚠ overstated / ❌ unsourced / ❌ wrong) · fix. Update `checked` dates for facts you re-verified
   (ask before changing any claim text or script line). Anything not ✅ blocks /render.
