# Sound design (editor)

- **Sonic signature:** stamp thunk · receipt-printer buzz · cash-register ding · coin clink
  (Chillar's footsteps). Use consistently.
- **Accents:** record scratch (twists), short glitch ("scam"), typing (Chillar Report), whoosh only on
  whip/zoom/page cuts. **Max one SFX per 2 s.**
- **Foley:** an action the voice describes ("khansa", "slurp", "knock", "sigh") gets its real sound in the gap
  right after the word — `fetch_assets.py foley <name> "<search words>"` cuts one CC0 hit to
  `brand/sfx/<name>.wav` (ledgered, reused by every reel); place it with a scene's `"sfx"`. Foley ranks with
  meme sounds in the 2 s thinning (above ding/printer/coin/whoosh); validate lists anything dropped in
  `scenes.resolved.json` → `sfx_dropped`.
- **Music:** quiet lo-fi, light tabla/dholak feel, sidechain-ducked, **20–24 dB below voice**.
- Final mix −14 LUFS integrated, −1 dBTP (`qa.py` checks final.mp4 after mix).
- `brand/sfx/custom/` = sounds the creator recorded (real stamp, real coins). **They override**
  downloaded ones of the same name.
