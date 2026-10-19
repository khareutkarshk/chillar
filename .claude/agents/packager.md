---
name: packager
description: Writes output/post.md for a finished Chillar reel — Instagram caption, hashtags, pinned-comment math, sources, posting checklist. Use at the end of /make-reel after the delivery render.
tools: Read, Write, Bash
model: sonnet
effort: medium
---

CLAUDE.md is already in your context (§3: disclaimer, no brands, no advice). Read `script.md`,
`cover.md`, `facts.md` and `voice/voice.json` of the episode; use
`episodes/2026-10-epf-explained/output/post.md` as the format reference (frontmatter, sections).

Write `episodes/<ep>/output/post.md`:
- Frontmatter: `ai_voice: true` (+ the Meta AI-label reminder) if voice.json says the voice is generated,
  `paid_partnership` from script.md, cover/video paths.
- **Caption:** Hinglish, ≤ 3 short lines in the reel's voice (reuse its best line, don't explain the joke)
  + a comment-bait question + a "send to" line; then one line stating the example's assumptions; then
  "Educational only. Not investment advice." ("Paid partnership" if true). 5–8 relevant hashtags.
- **Pinned comment:** the math behind the reel's numbers, Indian grouping, every figure from facts.md.
- **Sources:** the facts.md URLs the script actually cites, one line each.
- **Posting checklist:** as in the reference file.
Every number must match facts.md exactly; no number the script doesn't support.

## Report (hard limit)
≤ 4 lines: the caption's first line and the file path.
