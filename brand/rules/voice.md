# Voiceover details (/voiceover)

- Channel voice: Sarvam Bulbul, speaker `sunny_hi_reels`, pace 1.2 (chosen by the creator
  2026-10-19). Settings live in `episode.toml [tts]` (template default) — don't change speaker or pace
  per episode unless the creator asks.
- The AI voice reads `voice/tts.txt`, **not** script.md: Hindi words in Devanagari, English words in
  Latin ("UPI free है। फिर bill कौन भरता है?"). Write decimals/percents as spoken English
  ("zero point nine percent"), acronyms with dots ("M.D.R."), big numbers with Indian commas
  (₹3,631). Same words and order as script.md so alignment and captions stay correct.
- A creator recording (`voice/voice.wav` they drop in) is only used if the creator explicitly says so
  for that episode.
- post.md carries `ai_voice: true`; apply Instagram's AI label if Meta's current policy requires it
  for realistic synthetic audio.
- Sunny drops nasals (chandrabindu ँ and anusvara ं read as plain vowels: खाँसा → "khaasa"). Spell
  the nasal out as a half-consonant: खान्सा, not खाँसा/खांसा (fixed on 2026-10-sale-fine-print, checked
  by faster-whisper medium).
- **Delivery (2026-10-22): the script is an actor's script.** The writer marks `(beat)` `(pause)`
  `(long pause)` `(breath)` `(deadpan)` `(excited)` `(warm)` `(soft)` `(fast)` `(slow)` `(cont'd)` in script.md;
  `tts.py` carries them to the same word of tts.txt. Moods are real per-take settings (pace × and temperature:
  deadpan 0.95 / 0.35 · excited 1.06 / 0.85 · warm 0.96 / 0.7 · soft 0.92 / 0.5). Automatic: a character's
  quoted line is its own take with a pause into it (and a reply after a question waits like one); line gaps
  follow the punctuation (? 0.40 · ! 0.34 · । 0.30 · , 0.16 s) + 0.24 s on a chapter turn, ±12 % seeded
  variation; every performed gap is kept by audio_clean (voice.json `beats`); an inhale (brand/sfx/inhale.wav,
  CC0) goes before a new sentence after a long gap (voice.json `breaths`, placed by mix.py).
- **Pronunciation is measured, not guessed** (`pipeline/pronounce.py`): Sarvam saaras:v3 verbatim hears each
  line; a misheard word is solved in code — a fresh take when the miss was take luck, else a respelling
  (nasal by consonant class, a postposition split, the writer's Roman spelling…) kept only if heard right in 2
  fresh takes and never another real word. `pronounce.py stress` tests every channel word +
  brand/pronounce_corpus.txt; `sweep` checks past reels.
- **Takes are per line** (`[tts] per_line = true`, cached in `.cache/tts_takes/` by text + settings), so a
  respelling or `tts.py <ep> --retake L6` re-pays only that line and never re-rolls lines that were fine.
  Sarvam bills characters (v4-flash ₹2 / 1,000), so per-line requests cost the same as one big one.
