# Themes (director + component work)

The palette is a theme; nothing off-theme ever. All three are brand. **The director picks one per
script by mood** and sets `"theme"` in `scenes/scenes.json` (cover and palette check follow it);
`episode.toml [render] theme` can override; `brand/tokens.json "theme"` is only the fallback.
One theme per video, never mixed.
Boards: `components/_gallery/gallery.png` (pastel), `gallery-calm.png`, `gallery-night.png` — look at
one only when choosing between themes for a new look, not on every episode.

| theme | feel | chapter fields (slots note10 → note20 → note50 → note500, twist note2000, outro bone) |
|---|---|---|
| **pastel** — everyday money, friendly explainers | "Soft Rupee": note colours softened to milk-tea pastels | mocha · soft lime · sky · stone · rose · warm white |
| **calm** — taxes, insurance, debt, news | tone-on-tone, each field with a deep ink of its own hue | sage · powder blue · sand · dusty rose · slate · warm white |
| **night** — scams, myths, hidden fees, drama | night desk: warm paper under a lamp | deep forest · midnight · espresso · teal · oxblood · charcoal |

Typical picks: pastel — UPI, budgeting, first salary, Chillar in 60, ₹100 vs ₹1,00,000. calm — taxes,
insurance, EMI stress, credit score, Chillar Report. night — scams, myths busted, hidden fees, Myth vs Math.

Every theme has: **ink** (text on paper/haldi, always dark), **paper** (objects), **pencil**
(secondary text on paper), **red** (stamp ink, debits), **pen** (blue ballpoint — handwriting only),
**green / greenText**, **haldi** (highlight, marker, mascot — **never text colour**), and an ink per field.

Fields are flat with one soft same-hue light from above (`.field-light`); nothing else may be a
gradient (the marker fill and a passbook's own ruling are techniques, not looks). Shadows exist only
under paper objects (soft contact + ambient, `--lift`) — never glows, never on text.

Design direction came from the `design-taste-frontend` skill (`.agents/skills/design-taste-frontend`,
direction "Colour chapters", 2026-10-19), then softened for calm: tonal fields, real paper depth.
