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
- **Direction tags** in tts.txt (stripped before the API, never spoken, ignored by voice_check):
  `{beat}` / `{beat:0.6}` a pause (0.45 s default, 0.15–1.2 s) at that spot — before a punchline;
  `{slow}` / `{fast}` that line at 0.9× / 1.1× the channel pace. ≤ 4 beats, ≤ 2 pace tags per reel.
  audio_clean keeps tagged beats (voice.json `beats`); every other pause is still capped at `max_gap_s`.
- **Takes are per line** (`[tts] per_line = true`, cached in `.cache/tts_takes/` by text + settings), so a
  respelling or `tts.py <ep> --retake L6` re-pays only that line and never re-rolls lines that were fine.
  Sarvam bills characters (v4-flash ₹2 / 1,000), so per-line requests cost the same as one big one.
