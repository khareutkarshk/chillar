---
description: Make an AI voiceover (Sarvam Bulbul) from script.md — writes voice/tts.txt, then voice/voice.wav
argument-hint: <episode folder or slug> [--audition]
---

Voiceover for **$ARGUMENTS** — the channel voice (Sarvam `sunny_hi_reels`, pace 1.2; CLAUDE.md §7).

1. Write `voice/tts.txt` from the spoken lines of `script.md` — same words, same order, one script
   line per line — converted for Sarvam:
   - Hindi words in **Devanagari**, English words in Latin ("UPI free है। फिर bill कौन भरता है?").
   - Decimals / percents as spoken English: "zero point nine percent". Acronyms with dots: "M.D.R.".
   - ₹ amounts with Indian commas (₹3,631 crore). Years as written (2023-24).
   - No stage directions, fact ids or [JOKE] marks.
2. `.venv/bin/python pipeline/tts.py episodes/<slug>` (speaker/pace from `[tts]` in episode.toml;
   brand default `sunny_hi_reels` at 1.2). With `--audition`: run `--audition a,b,c` and point me to
   `voice/audition/index.html`.
3. Sanity-check pronunciation: transcribe `voice/voice.wav` with faster-whisper (`language="hi"`)
   and compare against tts.txt; fix wording in tts.txt for any number or word that came out wrong.
4. Report duration vs target_seconds and remind me AI-voiced posts may need Instagram's AI label.
