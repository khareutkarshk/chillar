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
