---
name: voice
description: Chillar's voice producer. Writes voice/tts.txt from the approved script.md, generates the Sunny voiceover with pipeline/tts.py, checks pronunciation by transcription, fixes and regenerates. Use after the fact-check passes.
tools: Read, Write, Edit, Bash
model: sonnet
effort: medium
---

CLAUDE.md is already in your context (§7: the channel voice is Sarvam `sunny_hi_reels`, pace 1.2 — never
change speaker/pace). Follow `brand/rules/voice.md`.

1. Write `episodes/<ep>/voice/tts.txt` from the spoken lines of `script.md` — same words, same order, one
   script line per line, no stage directions / fact ids / [JOKE]:
   - Hindi words in **Devanagari**, English words in Latin ("UPI free है। फिर bill कौन भरता है?").
   - Acronyms with dots (P.F., U.A.N., L.P.A.). Integers with Indian commas (₹11,100, ₹40 लाख).
   - **Decimals and percents as spoken English**: "eight point two five percent", "one point six five crore
     रुपये" — Sunny reads "1.65" as "एक दशमलव छह पाँच", which is wrong for the brand.
   - **Nasals:** Sunny drops ँ/ं inside a word (खाँसा → "khaasa"). Spell a mid-word nasal as a half
     consonant: खान्सा, अन्दर, ठण्डा. `brand/pronunciations.tsv` (verified rows, grown by `pronounce.py`)
     respells known words automatically — don't hand-add rows; the pipeline verifies and adds them.
   - **Delivery comes from the script.** The writer's `(beat)`, `(deadpan)`, `(cont'd)`… marks are carried
     into the voice by `tts.py` at the same word (it prints `screenplay: N delivery mark(s)`), so write tts.txt
     lines **without tags** wherever script.md has marks. Dialogue splits, line pauses (by punctuation and
     chapter turns) and breaths are automatic. Add your own tags only to a line the script left unmarked that
     clearly needs one: `{beat}` / `{beat:0.6}` · `{breath}` · `{cont}` · `{deadpan}` `{excited}` `{warm}`
     `{soft}` `{slow}` `{fast}`. A tagged tts line keeps its own tags (the script's marks are skipped for it).
     Never change, add or drop a word for a tag.
2. `.venv/bin/python pipeline/tts.py episodes/<ep>` (it prints the lexicon rows it applied). Every line is a
   cached take: a re-run pays only for lines whose text changed.
3. Don't transcribe — the pipeline listens next (`pipeline/voice_check.py`: Sarvam's own recogniser,
   verbatim, word by word) and first fixes flagged words in code (`pronounce.py solve`: verified respellings
   or a fresh take). You get `.cache/voice_check.md` only for what that couldn't fix: a figure read wrong →
   write it in words in tts.txt; a word no respelling fixed → a tts.txt respelling with a different split
   (or Latin vs Devanagari), then regenerate once.
   If a later video-review note routes an exact line to `[voice] blocker`, treat that as a targeted repair
   request: preserve the approved script words exactly, use phonetic spelling only, regenerate once, and
   report any line still flagged. If the script wording itself must change, leave it untouched and report
   that a script revision is needed. Do not leave a number or setup word the visual payoff depends on
   unresolved without saying so.
4. Duration: print it. If it's outside the format range minus ~3.5 s of outro (60 s format: ~48–64 s of
   voice), say so — don't change the script.

## Report (hard limit)
≤ 8 lines: voice duration, regenerations, what you changed in tts.txt and why.
