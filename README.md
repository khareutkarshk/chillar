# chillar-reels

Hinglish script + voiceover → 9:16 "Note Fields" finance Reels for **Chillar**, made by a team of
agents (scriptwriter ⇄ script-reviewer, fact-checker, director, editor ⇄ video-reviewer).
Brand bible and all rules: [CLAUDE.md](CLAUDE.md).

```
./setup.sh                                   # once (idempotent): ffmpeg, Node, uv venv, HyperFrames, fonts, models
/make-reel <topic> [30|60|90]                # the whole production line with review loops (or step by step ↓)
/new-reel <topic> [30|60|90]                 # research → facts.md, cover.md → writers' room writes script.md
/package <ep>                                # 5 cover/first-frame/hook options, scored; post.md caption
/voiceover <ep>                              # channel voice: Sarvam Sunny, pace 1.2 (automatic in /make-reel)
/fact-check <ep>                             # every number re-verified against its source
/render <ep>                                 # director → editor → render → video-reviewer loop → delivery
```

The pipeline by hand: `.venv/bin/python pipeline/make_reel.py episodes/<ep> [--from STAGE] [--quality draft]`
(stages: `facts clean align validate build qa render mix cover sheet igcheck`; `qa` measures the built
composition in headless Chrome and blocks the render on layout/timing errors).

## Layout
| path | what |
|---|---|
| `brand/` | `colors.css`, `tokens.json` (rules the validators read), `rules/` (reference rules agents open on demand), `facts-library.md` (reusable sourced facts) + `sources/` (cached source PDFs), `fonts/` (OFL), `mascot/` (Chillar layered SVG, `sheet.png`), `sfx/` (locked) + `sfx/custom/` (your recordings, always win), `music/`, `_audition/` |
| `.claude/agents/` | scriptwriter, script-reviewer, fact-checker, director, editor, video-reviewer |
| `components/` | 22 HyperFrames-ready blocks (`component.json` = params, example, SFX events). Index: `components/_catalog.md` (generated). Gallery: `components/_gallery/gallery.png` (`pipeline/component_gallery.py`) |
| `pipeline/` | `make_reel.py` + stages, `qa.py` (mechanical QA), `frames.py` (half-size review frames), `facts_library.py`, `component_catalog.py`, `fetch_assets.py` (licensed assets only), `tts.py` (Sarvam voice), `mascot_sheet.py` |
| `episodes/_template/` | `script.md`, `cover.md`, `facts.md`, `episode.toml`, `voice/`, `scenes/`, `output/` |
| `assets/licenses.json` | every downloaded file: source, URL, license, attribution, date, sha256, license snapshot |

## Your first real reel (with your own voice)

1. **Lock the sounds once.** Open `brand/_audition/index.html`, listen, then
   `.venv/bin/python pipeline/fetch_assets.py lock stamp=1 printer=2 ding=1 coin=3 scratch=1 glitch=2 typing=1 whoosh=1 music=1,3`.
   Recorded a real stamp or coins? Drop `stamp.wav` / `coin.wav` into `brand/sfx/custom/` — they override.
2. **`/new-reel <topic> 60`** in Claude Code. The scriptwriter and script-reviewer go back and forth
   (notes in `episodes/<ep>/notes/`). Read `facts.md` (are the sources real and current?) and make
   any `[JOKE]` line yours if it doesn't sound like you.
3. **`/package <ep>`** and pick a cover. The payoff must deliver exactly what the cover promises.
4. **Record.** Phone voice memo or USB mic, quiet room, 15–20 cm from the mic, read `script.md`
   as written (fast, flat, no "toh guys"). Small pauses are fine — they get tightened automatically.
   Save as `episodes/<ep>/voice/voice.wav` (m4a/mp3 also fine).
5. **`/fact-check <ep>`** — nothing ships with ⚠ or ❌.
6. **`/render <ep>`** — Claude aligns your words, plans scenes to them, renders a draft, reviews the
   contact sheet and fixes it. Watch `output/final.mp4`. Want a change? Edit
   `scenes/scenes.json` (or tell Claude) and run `make_reel.py episodes/<ep> --from validate`.
7. **Final:** `make_reel.py episodes/<ep> --from validate --quality delivery`. Upload `final.mp4`,
   set `cover.jpg` as the cover (check `cover_grid_preview.png` for the profile grid), paste
   `output/post.md` as the caption.

## Notes
- Captions are Roman Hinglish from `script.md`; the voice is aligned to the script (forced alignment),
  so caption words are always exactly yours. `.cache/adlibs.md` lists anything you said off-script.
- Music sits ~22 dB under the voice with sidechain ducking; final mix is −14 LUFS / −1 dBTP.
- Sounds not yet locked render as **PROVISIONAL** (option 1 of each audition slot) — the mix log says so.
- Pixabay audio scraping opens a visible Chrome window (Cloudflare) and is against Pixabay's ToS:
  keep it rare. Mixkit's search pages show paid Envato items — the fetcher only takes free Mixkit items.
