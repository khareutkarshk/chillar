# chillar-reels — brand bible + working rules

This repo turns a Hinglish `script.md` + a voiceover into 9:16 finance Reels for Gen Z India, made by
a team of agents with feedback loops. **Every rule below is enforced in every video.** If a request
conflicts with this file, say so before doing it. Machine-readable tokens: `brand/tokens.json`
(validators read it). CSS: `brand/colors.css`.

**Reference rules — open only when your job needs them** (`brand/rules/`):
`themes.md` (theme table, palette roles) · `formats.md` (30/60/90 table, retention) · `sound.md` ·
`voice.md` (tts.txt writing) · `instagram.md` (export/upload spec, profile pic) · `production.md`
(agents, model tiers, hand-offs, QA, image budget, facts library, session hygiene) ·
`posting-schedule.md` (daily timetable: series per weekday, post times, production day, backlog).

## 1. Brand
- **Brand:** Chillar. **Series:** "Chillar in 60" (concepts) · "Chillar Report" (weekly money news) ·
  "Myth vs Math" (debunks) · "₹100 vs ₹1,00,000" (escalation comparisons).
- **Style: "Note Fields"** — every chapter is one softly lit, calm field; the passbook, receipts,
  slips and calendars are real paper objects lying on it (soft contact shadow, slight tilt), marked up
  in blue ballpoint and stamp-pad red. Soothing, tactile, made by hand, not by a template.
  **3-second test:** any paused frame must be recognisable as Chillar.
- **Themes:** pastel (everyday money) · calm (taxes, insurance, debt, news) · night (scams, myths,
  drama). The director picks one per script by mood (`"theme"` in scenes.json); one theme per video,
  nothing off-theme ever. **haldi is never a text colour; pen blue is handwriting only.** Fields are
  flat with one soft same-hue light; no other gradients. Shadows only under paper objects — never
  glows, never on text. Details: `brand/rules/themes.md`.

### Type — three faces, OFL, in `brand/fonts/`
- **Bricolage Grotesque 800** — headlines in **sentence case** (tracking −0.022em, leading 1.0) and
  every big number (tabular figures, has ₹). Devanagari falls back to Mukta via `var(--font-head)`.
- **Mukta ExtraBold** — captions + body (Roman + Devanagari).
- **JetBrains Mono** — **only inside printouts** (receipts, passbook entries, slip metadata), via
  `var(--font-print)`. Never as a "technical" label voice.
- Headlines ≤ 6 words, left-aligned on the shared content edge; centre at most one moment per video.
  Objects span the full content width (≈ 860–880 px) — big and calm beats small and busy.
- **Indian number format everywhere:** ₹1,00,000 not ₹100,000 (`toLocaleString('en-IN')`).
- **Captions are Roman Hinglish**, centred, in the field's ink; the active word is ink on a rounded haldi pill.

### Banned "AI-look" tells (the video-reviewer fails a frame for any of these)
Eyebrow/pill labels above headlines ("CHILLAR IN 60", "DEFINITION", "PLOT TWIST") · tiny tracked
uppercase labels · mono micro-labels · grid/ledger lines on the frame · hard offset shadows / outlined
cards · every element centred · the same entrance on every shot · bouncy overshoot on everything ·
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
- Styled cuts (`"cut"` on a scene, `components/transition`) are moves on the shots themselves:
  **whip** (time/place jump), **zoom** (into a number/document), **wipe** (mood flip into a twist),
  **page** (a blank passbook page turns). Budget 30 s → 1 · 60 s → 2 · 90 s → 3; ≥ 12 s apart; never
  the same style twice in a row.
- **A transition never carries text.** Chapter names exist only for the writer and director.
  `validate_scenes.py` blocks violations.
- Cut on the stressed word or on action; hold a punchline to its last word, then cut to the reaction.

### Handle, wordmark, outro (every video)
- Instagram: **@chillar.ind** (`brand/tokens.json` `"brand".handle` — change it only there).
- **Wordmark:** tiny haldi coin + `@chillar.ind`, Mukta 30 px in the field's ink at 78 %, bottom-left
  at **x 72, y 1460–1500**, on **every frame from 0 until the outro**. `validate_scenes.py` inserts it —
  never place, move or hide it in scenes.json; keep stamps/Chillar off its box.
- **Outro** (bone field): receipt tears off: **"Is video ka MDR: 0%. Gyaan free hai."** + "Follow
  @chillar.ind" (filled from the handle) + "Educational only. Not investment advice."

### Mascot "Chillar"
Healthy, round ₹1 coin (no dent, no damage), haldi yellow, thick ink outline, deadpan half-closed
eyes, tiny stick limbs, **never fully smiles.** Chillar reactions and real global memes carry the reaction beats. Files: `brand/mascot/`.
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
- No real brand logos or names, no app sounds, no song lyrics, no movie/TV clips with their audio.
- **Real memes are allowed** (creator's call, 2026-10-20): imgflip templates/GIFs and meme sounds,
  fetched per episode at build time by `pipeline/memes.py` (`meme` component), the Fireship way: cut to
  one on the word after a punchline. **Images: global or Indian. Video and sound: global only.**
  **Fresh only:** every meme and reference is from this month — facts.md `## Culture now` (researcher)
  or `memes.py trending`; ≤ 1 old-but-everywhere classic per reel; validate blocks stale ones.
  Meme beats are written into the script as jokes (`brand/rules/comedy.md` §7), not sprinkled on.
  No politician memes. Our own text on them; never a meme that mocks a private person.
  Budget: 30 s ≤ 3 · 60 s ≤ 5 · 90 s ≤ 7. Filmy-line nods stay a few-word parody.
- Never show realistic rupee banknotes — note *colours* as fields only, never note imagery.
- **Every fact must appear in `episodes/<ep>/facts.md` with a source URL**, and the script line
  citing it carries its id, e.g. `UPI pe MDR zero hai [F1]`. `pipeline/fact_lint.py` blocks the
  render on any number without a fact id or a fact without a URL. Jokes can't smuggle in numbers.
  Only two URL-less facts pass (creator's call, 2026-10-20): a source cell saying **hypothetical** (an
  invented example; the script frames it as one, never as a real offer) or **computed from F#** (arithmetic
  on facts that are themselves sourced or hypothetical).
  Recurring facts come from `brand/facts-library.md`.

## 4. Formats + retention
30 s (27–36 s, 70–95 words, 3 chapters, ≥ 3 laughs) · 60 s (52–68 s, 140–180 words, 4 chapters, ≥ 6)
· 90 s (80–98 s, 215–260 words, 5 chapters, ≥ 9). Set `target_seconds` in script.md. Frame 1 shows
the stakes; sentence 1 states the question; **no intros**; first laugh by 4–5 s; each chapter
escalates; one concept per Reel; the payoff exactly delivers the cover's promise; no get-rich
clickbait. Full table (re-hooks, stamps, cuts) + cover-first rule: `brand/rules/formats.md`.

## 5. Sound
Sonic signature: stamp thunk · printer buzz · register ding · coin clink. **Max one SFX per 2 s.**
Music 20–24 dB under voice. Final mix −14 LUFS / −1 dBTP. Creator recordings in `brand/sfx/custom/`
override downloads. Details: `brand/rules/sound.md`.

## 6. Assets & licensing
- Sources: Freesound (CC0 only), Pixabay, Mixkit, Kenney (CC0), Pexels (sparingly), Lucide/Tabler
  icons (MIT), Google Noto Emoji, Google Fonts (OFL, via `setup.sh`). Nothing else.
- Fetch only through `pipeline/fetch_assets.py`; every file is logged in `assets/licenses.json`
  with a saved license snapshot. Refuse anything without a clear commercial-use license.
  **One exception: memes** (§3) come only through `pipeline/memes.py`, are logged as
  `"Meme (uncleared, creator-approved)"` with their source page, and live in the episode's `.cache/memes/`.
- Scraping (Pixabay/Mixkit audio) is low-volume and polite; it is against Pixabay's ToS, so keep
  volume minimal.

## 7. Voiceover — the channel voice is Sarvam "Sunny"
Every reel is voiced by Sarvam Bulbul `sunny_hi_reels`, pace 1.2 (`episode.toml [tts]`). The
pipeline does **not** stop to ask about voice: after review + fact-check, run `/voiceover <ep>` and
continue. A creator recording is used only if the creator says so for that episode. The voice reads
`voice/tts.txt` (Devanagari Hindi + Latin English, same words as script.md). post.md carries
`ai_voice: true`. Details: `brand/rules/voice.md`.

## 8. How work happens here — the production line
- **One command:** `/make-reel <topic> [30|60|90]`. Step by step: `/new-reel` → `/package` →
  `/fact-check` → `/voiceover` → `/render`.
  `/make-reel` runs `pipeline/produce.py` (headless lean agents, pinned models, real cost per run in
  `notes/usage.md`) — keep the producer session thin; see `brand/rules/production.md`.
- Agents (`.claude/agents/`): scriptwriter ⇄ script-reviewer (≤ 3 rounds) · fact-checker · director ⇄
  editor ⇄ video-reviewer (≤ 3 rounds). After 3 rounds without PASS the pipeline stops; the producer decides by the table in `.claude/commands/make-reel.md` and asks only for a fact-check BLOCK, a §3 conflict or cost > $12.
  **Each round is a fresh agent that reads the notes files — never resume an agent.** Model tiers,
  hand-off and image-budget rules: `brand/rules/production.md`.
- Pipeline: `.venv/bin/python pipeline/make_reel.py episodes/<ep> [--from STAGE]`
  Stages: `facts → clean → align → validate → build → qa → render → mix → cover → sheet → igcheck`.
  `validate_scenes.py` (formats, fields, cuts, stamps, labels, facts) and `qa.py` (layout, timing,
  odometer, audio) must pass before a render.
- Gates code runs so agents don't pay to find them (2026-10-20): `fact_lint` (unframed example facts, reused
  memes, length) goes back to the writer **before** each script review · `voice_check.py` (whisper medium,
  line by line) sends flagged lines back to the voice agent once; known fixes live in `brand/pronunciations.tsv`
  · validate blocks memes from the last 4 reels and shots < 70 % of minDuration · a PASS's polish notes are
  applied (qa-guarded) before delivery · component requests go to `components/_backlog.md`, built in batch
  (`produce.py <ep> --only components`) · action words get foley (`fetch_assets.py foley`).
- Components live in `components/<name>/` (`component.json` + css + js). Reuse them; don't hand-build
  one-offs inside episodes. Index: `components/_catalog.md`. After changing one, run
  `pipeline/component_gallery.py <name>` (also refreshes the catalog) and look at its `preview.png`.
- **Never claim a render is done without looking at `output/contact_sheet.png`** and fixing
  overlapping text, off-screen elements, off-palette colours or AI-look tells.
- Python: `.venv/bin/python` (managed by uv). Node tools: `npx hyperframes …` (pinned in package.json).

## 9. Instagram upload spec
Export is always 1080×1920, 30 fps CFR, H.264 High (not HEVC), yuv420p, 1 s closed GOP, +faststart,
AAC 128 kbps 48 kHz stereo; `output/final.mp4` is always re-encoded by `mix.py`, never stream-copied.
Nothing is posted unless the `igcheck` stage prints "upload-safe". Full spec, cover, upload habits,
profile picture: `brand/rules/instagram.md`.

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
