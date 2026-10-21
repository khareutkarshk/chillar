# Formats + retention (MrBeast structure, Fireship delivery)

| format | length | spoken words | chapters | laughs ≥ | re-hook every | stamps | styled cuts ≤ |
|---|---|---|---|---|---|---|---|
| **30 s** | 27–36 s | 70–95 | 3 | 3 | ~10 s | 1–2 | 1 |
| **60 s** | 52–68 s | 140–180 | 4 | 6 | ~16 s | 2–3 | 2 |
| **90 s** | 80–98 s | 215–260 | 5 | 9 | ~18 s | 3 | 3 |

Set `target_seconds: 30|60|90` in script.md; `validate_scenes.py` reads the format from it (numbers
also in `brand/tokens.json "formats"`).
- Before scripting, write the **cover text (≤5 words)** and **first frame** (`cover.md`).
- Frame 1 shows the stakes; sentence 1 states the question. **No intros.** First laugh by 4–5 s.
- **Open loop:** the hook plants one specific question only the payoff answers (frontmatter `open_loop: "L2 → L9"`,
  fact_lint checks it): "…par yeh paisa gaya kahan?" — never "end tak dekho" or "last mein bataunga" (a tell).
  3–15 s, where the explaining starts, was the swipe zone on 5 of 6 reels; an unanswered question is what holds it.
- **First re-hook early:** by 8 s (30 s) / 10 s (60, 90 s) — a stamp, reveal, meme or Chillar beat, not more
  explaining. validate enforces it (`firstRehookBy` in tokens.json).
- **The end:** the last spoken word is the punchline; the outro cuts in on it (1.9 s). Write the last line so it
  calls back the hook — on Instagram's auto-replay the hook plays right after it, and a callback makes the loop land.
- Escalate: each chapter bigger than the last (and its note field a bigger denomination).
- One concept per Reel; show a coin meter (`progress-meter`) or a growing receipt/passbook.
- The payoff must exactly deliver the cover's promise. No get-rich clickbait; stakes = mistakes and
  surprising math.
- Styled cuts: budget above, ≥ 12 s apart, never the same style twice in a row.
