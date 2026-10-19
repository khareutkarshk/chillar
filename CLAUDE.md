# chillar-reels — brand bible + working rules

This repo turns a Hinglish `script.md` + a recorded voiceover into 9:16 finance Reels for Gen Z
India, made by a team of agents (scriptwriter, script-reviewer, fact-checker, director, editor,
video-reviewer) with feedback loops. **Every rule below is enforced in every video.** If a request
conflicts with this file, say so before doing it.

Machine-readable tokens: `brand/tokens.json` (validators read it). CSS: `brand/colors.css`.

---

## 1. Brand
- **Brand:** Chillar. **Series:** "Chillar in 60" (concepts) · "Chillar Report" (weekly money news) ·
  "Myth vs Math" (debunks) · "₹100 vs ₹1,00,000" (escalation comparisons).
- **Style: "Note Fields"** — every chapter is one softly lit, calm field; the passbook, receipts,
  slips and calendars are real paper objects lying on it (soft contact shadow, slight tilt), marked up
  in blue ballpoint and stamp-pad red. Soothing, tactile, made by hand, not by a template.
  **3-second test:** any paused frame must be recognisable as Chillar.
- Design direction came from the `design-taste-frontend` skill (`.agents/skills/design-taste-frontend`,
  direction "Colour chapters", 2026-10-19), then softened for calm: tonal fields, real paper depth.

### Themes — the palette is a theme, nothing off-theme ever
All three are brand. **The director picks one per script by mood** and sets `"theme"` in
`scenes/scenes.json` (cover and palette check follow it); `episode.toml [render] theme` can override;
`brand/tokens.json "theme"` is only the fallback. One theme per video, never mixed.
Boards: `components/_gallery/gallery.png` (pastel), `gallery-calm.png`, `gallery-night.png`.
| theme | feel | chapter fields (slots note10 → note20 → note50 → note500, twist note2000, outro bone) |
|---|---|---|
| **pastel** — everyday money, friendly explainers | "Soft Rupee": note colours softened to milk-tea pastels | mocha · soft lime · sky · stone · rose · warm white |
| **calm** — taxes, insurance, debt, news | tone-on-tone, each field with a deep ink of its own hue | sage · powder blue · sand · dusty rose · slate · warm white |
| **night** — scams, myths, hidden fees, drama | night desk: warm paper under a lamp | deep forest · midnight · espresso · teal · oxblood · charcoal |
Every theme has: **ink** (text on paper/haldi, always dark), **paper** (objects), **pencil**
(secondary text on paper), **red** (stamp ink, debits), **pen** (blue ballpoint — handwriting only),
**green / greenText**, **haldi** (highlight, marker, mascot — **never text colour**), and an ink per field.
Fields are flat with one soft same-hue light from above (`.field-light`); nothing else may be a gradient
(the marker fill and a passbook's own ruling are techniques, not looks).
Shadows exist only under paper objects (soft contact + ambient, `--lift`) — never glows, never on text.

### Type — three faces, OFL, in `brand/fonts/`
- **Bricolage Grotesque 800** — headlines in **sentence case** (tracking −0.022em, leading 1.0) and
  every big number (tabular figures, has ₹). Devanagari falls back to Mukta via `var(--font-head)`.
- **Mukta ExtraBold** — captions + body (Roman + Devanagari).
- **JetBrains Mono** — **only inside printouts** (thermal receipts, passbook entries, slip metadata),
  where it is the printer's face. Never as a "technical" label voice. Use `var(--font-print)`.
- Headlines ≤ 6 words, left-aligned on the shared content edge; centre at most one moment per video.
  Objects span the full content width (≈ 860–880 px) — big and calm beats small and busy.
- **Indian number format everywhere:** ₹1,00,000 not ₹100,000 (`toLocaleString('en-IN')`).
- **Captions are Roman Hinglish**, centred, in the field's ink; the active word is ink on a rounded haldi pill.

### Banned "AI-look" tells (the video-reviewer fails a frame for any of these)
Eyebrow/pill labels above headlines ("CHILLAR IN 60", "DEFINITION", "PLOT TWIST") · tiny tracked
uppercase labels · mono micro-labels · grid/ledger lines on the frame · hard offset shadows / outlined cards · every element centred · the same entrance on every shot · bouncy overshoot on everything ·
title cards between chapters · **script-structure words on screen** (chapter names, "Setup",
"Escalation", "Payoff", "Part 2", "Page 3", "Step 1").

### Human touch
Paper objects rest at a seeded tilt (±2°), cast a soft shadow and are *tossed* in; key numbers get a
blue-ballpoint circle or double underline drawn at hand speed; myths get a red-pen scratch-out; paper
grain sits over the field. Every mark is generated (`CH.scribble`), seeded, so renders are deterministic.

### Signature move: the "thappa"
Key facts slam in as a stamp-pad red rubber stamp on a scrap of paper: scale 140%→100%, 2-frame
shake, thunk SFX. **30 s: 1–2 · 60 s: 2–3 · 90 s: 3. Never more than 3.**

### Motion
- Entrances 5–7 frames, `power3.out`, **no overshoot** (overshoot is reserved for Chillar and the stamp).
- Receipt/passbook lines print line-by-line in steps (printer buzz). Numbers roll like an odometer.
- Yellow marker swipe on key words. Small zoom punch on punchlines.
- **New visual every 2–3 s.** 1080×1920, 30 fps.

### Cuts and transitions — like a real editor
- **Default is the hard cut.** Within a chapter: hard cuts only. Between chapters: a hard cut on the
  chapter's first word, and the field colour changes on that cut (a scene must start there).
- Styled cuts are moves on the shots themselves (`components/transition`), set per scene with
  `"cut"`: **whip** (time/place jump), **zoom** (going into a number/document), **wipe** (next field
  slides over — mood flip into a twist), **page** (a blank passbook page turns — literally the next page).
  Budget: 30 s → 1 · 60 s → 2 · 90 s → 3; ≥ 12 s apart; never the same style twice in a row.
- **A transition never carries text.** No chapter titles, no "PAGE 2", no setup/escalation labels.
  Chapter names exist only for the writer and director. `validate_scenes.py` blocks violations.
- Cut on the stressed word or on action; hold a punchline to its last word, then cut to the reaction.

### Handle + wordmark (every video)
- Instagram: **@chillar.ind** (`brand/tokens.json` `"brand".handle` — change it only there).
- **Wordmark:** a tiny haldi coin + `@chillar.ind`, Mukta 30 px in the field's ink at 78 %, bottom-left
  at **x 72, y 1460–1500** (just under the caption band, inside the safe zone). It is on **every frame
  from 0 until the outro**, so downloads and reshares carry the name. `validate_scenes.py` inserts it
  automatically — never place, move or hide it in scenes.json; keep stamps/Chillar off its box.
- The outro's follow line is filled from the handle ("Follow @chillar.ind").
- **Profile picture:** `brand/profile/dp-<theme>.jpg` (1080×1080, Chillar side-eye, no text — it has to
  read as a 110 px circle). Rebuild with `pipeline/profile_pic.py`. Current DP: `dp-night.jpg`.

### Outro (every video)
Outro field (bone slot). Receipt tears off: **"Is video ka MDR: 0%. Gyaan free hai."** + follow prompt +
"Educational only. Not investment advice."

### Mascot "Chillar"
Healthy, round ₹1 coin (no dent, no damage), haldi yellow, thick ink outline, deadpan
half-closed eyes, tiny stick limbs, **never fully smiles.** Chillar reactions replace memes. Files: `brand/mascot/`.
Expressions: neutral-tired, shocked, side-eye, smug, crying, facepalm, thinking, counting-money.

### Tone
Hinglish, fast, dense, deadpan, genuinely funny — the register of Indian internet comedy writers like
Tanmay Bhat and Vishal Dayama (self-roast, hyper-specific desi detail, escalation, callbacks, puns that
work spoken, meme formats). Their craft, never their material: all jokes original. No filler words
("toh guys", "basically", "dosto" — cut them). Punch up or at ourselves, never down.

## 2. Instagram layout rules (safe zones)
- 1080×1920 canvas. Keep key content out of: **top 220px, bottom 420px, right 140px**, left 60px.
- Captions live in the band **y = 1150–1450**.
- **Cover:** key text inside the central **1080×1440 (3:4)** area (y 240–1680) — profile grid crop.

## 3. Content rules (non-negotiable)
- Education only. **Never recommend specific stocks/funds/apps, never promise returns.**
- Outro + post caption carry "Educational only. Not investment advice." (SEBI finfluencer norms,
  ASCI influencer guidelines). Paid partnerships: on-screen "Paid partnership" label + caption tag.
- No real brand logos or names, no app sounds, no copyrighted memes / movie stills / clips / lyrics.
  Recreate meme **formats** with Chillar and original text; filmy-line nods only as a few-word parody.
- Never show realistic rupee banknotes — note *colours* as fields only, never note imagery.
- **Every fact must appear in `episodes/<ep>/facts.md` with a source URL**, and the script line
  citing it carries its id, e.g. `UPI pe MDR zero hai [F1]`. `pipeline/fact_lint.py` blocks the
  render on any number without a fact id or a fact without a URL. Jokes can't smuggle in numbers.

## 4. Formats + retention (MrBeast structure, Fireship delivery)
| format | length | spoken words | chapters | laughs ≥ | re-hook every | stamps | styled cuts ≤ |
|---|---|---|---|---|---|---|---|
| **30 s** | 27–36 s | 70–95 | 3 | 3 | ~10 s | 1–2 | 1 |
| **60 s** | 52–68 s | 140–180 | 4 | 6 | ~16 s | 2–3 | 2 |
| **90 s** | 80–98 s | 215–260 | 5 | 9 | ~18 s | 3 | 3 |
Set `target_seconds: 30|60|90` in script.md; the validator reads the format from it.
- Before scripting, write the **cover text (≤5 words)** and **first frame** (`cover.md`).
- Frame 1 shows the stakes; sentence 1 states the question. **No intros.** First laugh by 4–5 s.
- Escalate: each chapter bigger than the last (and its note field a bigger denomination).
- One concept per Reel; show a coin meter (`progress-meter`) or a growing receipt/passbook.
- The payoff must exactly deliver the cover's promise. No get-rich clickbait; stakes = mistakes
  and surprising math.

## 5. Sound design
- **Sonic signature:** stamp thunk · receipt-printer buzz · cash-register ding · coin clink
  (Chillar's footsteps). Use consistently.
- **Accents:** record scratch (twists), short glitch ("scam"), typing (Chillar Report), whoosh only on
  whip/zoom/page cuts. **Max one SFX per 2 s.**
- **Music:** quiet lo-fi, light tabla/dholak feel, sidechain-ducked, **20–24 dB below voice**.
- Final mix −14 LUFS integrated, −1 dBTP.
- `brand/sfx/custom/` = sounds the creator recorded (real stamp, real coins). **They override**
  downloaded ones of the same name.

## 6. Assets & licensing
- Sources: Freesound (CC0 only), Pixabay, Mixkit, Kenney (CC0), Pexels (sparingly), Lucide/Tabler
  icons (MIT), Google Noto Emoji, Google Fonts (OFL, via `setup.sh`). Nothing else.
- Fetch only through `pipeline/fetch_assets.py`; every file is logged in `assets/licenses.json`
  with a saved license snapshot. Refuse anything without a clear commercial-use license.
- Scraping (Pixabay/Mixkit audio) is low-volume and polite; it is against Pixabay's ToS, so keep
  volume minimal.

## 7. Voiceover — the channel voice is Sarvam "Sunny"
- **Every Chillar reel is voiced by Sarvam Bulbul, speaker `sunny_hi_reels`, pace 1.2** (chosen by the
  creator 2026-10-19): fast, Fireship-paced Hinglish. Settings live in `episode.toml [tts]` (template
  default) — don't change speaker or pace per episode unless the creator asks.
- The pipeline does **not** stop to ask about voice: after the script passes review + fact-check, run
  `/voiceover <ep>` (`pipeline/tts.py`) and continue. A creator recording (`voice/voice.wav` they drop
  in) is only used if the creator explicitly says so for that episode.
- AI voice reads `voice/tts.txt`, **not** script.md: Hindi words in Devanagari, English words in
  Latin ("UPI free है। फिर bill कौन भरता है?"). Write decimals/percents as spoken English
  ("zero point nine percent"), acronyms with dots ("M.D.R."), big numbers with Indian commas
  (₹3,631). Same words and order as script.md so alignment and captions stay correct.
- Every reel is AI-voiced: post.md carries `ai_voice: true`; apply Instagram's AI label if Meta's
  current policy requires it for realistic synthetic audio.

## 8. How work happens here — the production line
- **One command:** `/make-reel <topic> [30|60|90]` runs everything below with the loops.
- Step by step: `/new-reel <topic> [30|60|90]` → `/package <ep>` → `/fact-check <ep>` → `/voiceover <ep>`
  (Sunny, automatic) → `/render <ep>`.
- **Agents** (`.claude/agents/`), each with one job; the main session is the producer that routes work:
  | agent | does | loop |
  |---|---|---|
  | `scriptwriter` | writes/rewrites script.md (jokes, puns, meme refs, facts cited) | ⇄ script-reviewer, ≤ 3 rounds |
  | `script-reviewer` | scores + line notes → `notes/script-review-<n>.md`, PASS/REVISE | |
  | `fact-checker` | verifies every claim against sources → `notes/fact-check.md`, PASS/BLOCK | BLOCK → scriptwriter |
  | `director` | script + words.json → `scenes/scenes.json` (visuals, fields, stamps, cuts) | ⇄ video-reviewer |
  | `editor` | rhythm, cut points, comedic timing, transitions, SFX in scenes.json | ⇄ video-reviewer |
  | `video-reviewer` | reviews the render (contact sheet + frames at every cut) → `notes/video-review-<n>.md` | ≤ 3 rounds |
  After 3 rounds without PASS, stop and ask the creator.
- Pipeline: `.venv/bin/python pipeline/make_reel.py episodes/<ep> [--from STAGE]`
  Stages: `facts → clean → align → validate → build → render → mix → cover → sheet → igcheck`.
  `pipeline/validate_scenes.py` must pass (it enforces formats, fields, cuts, stamps, labels, facts).
- Components live in `components/<name>/` (`component.json` + css + js, declaring params and SFX
  events). Reuse them; don't hand-build one-offs inside episodes. After changing one, re-render
  `pipeline/component_gallery.py <name>` and look at `components/<name>/preview.png`.
- **Never claim a render is done without looking at `output/contact_sheet.png`** and fixing
  overlapping text, off-screen elements, off-palette colours or AI-look tells.
- Python: `.venv/bin/python` (managed by uv). Node tools: `npx hyperframes …` (pinned in package.json).

## 9. Instagram upload spec (so Reels don't break after upload)
Source: Meta's Reels spec in the Instagram Platform reference (checked 2026-10-19) — recorded in
`brand/tokens.json` `"instagram"`. Meta's hard limits: MP4/MOV with the moov atom at the front and no
edit lists · H.264 or HEVC, progressive, closed GOP, 4:2:0 · 23–60 fps · width ≤ 1920 · VBR ≤ 25 Mbps ·
AAC ≤ 48 kHz mono/stereo, 128 kbps · 3 s – 15 min · ≤ 300 MB · cover JPEG, sRGB, ≤ 8 MB, 9:16.
**Our export is stricter, always:**
- **1080×1920, 9:16, 30 fps constant**, H.264 High 4.2, `yuv420p`, 1 s closed GOP, CRF 18 capped at
  16 Mbps, BT.709 colour tags, `+faststart`, no edit lists, metadata stripped. Not HEVC (uploads from
  some devices/transcodes glitch on it).
- **Audio:** AAC 128 kbps, 48 kHz, stereo, −14 LUFS / −1 dBTP. Never upload silent video.
- **`output/final.mp4` is always re-encoded by `pipeline/mix.py` with `ig_export.encode_args()`** —
  never stream-copied from the renderer (the raw render has 8 s keyframe gaps and an edit list).
- **Cover:** `output/cover.jpg` (JPEG, sRGB, 1080×1920). Key text inside the 3:4 grid crop (§2).
- **Gate:** `make_reel.py` ends with the `igcheck` stage (`pipeline/ig_export.py check output/final.mp4
  --cover output/cover.jpg`). Nothing is posted unless it prints "upload-safe".
- **Upload habits:** upload the file itself (not a WhatsApp/Telegram-forwarded copy, which is
  recompressed); in the Instagram app turn on *Settings → Data usage and media quality → Upload at
  highest quality*; upload on Wi-Fi; don't trim or add filters in the IG editor (it re-encodes and
  can shift the captions out of the safe zone). Our formats (30/60/90 s) stay under 3 min, the limit
  for Reels being recommended to non-followers.

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
