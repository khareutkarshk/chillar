# Component catalog (generated — `pipeline/component_catalog.py`, don't edit)

Read this instead of the component folders. Open a `components/<name>/component.json` only for a
component you are about to use and need its full `example`. Layers: `scene` lasts until the next scene;
`overlay` needs `until`/`duration`. Times in params are seconds from the scene's start.

**scenes.json keys** (full spec: `pipeline/validate_scenes.py` docstring — no need to open it):
scene `{id, component, at, params, fact?, cut?}` · overlay adds `until` or `duration` · times: seconds, `"w12"` (word 12 start), `"w12.end"`, `"w12+0.2"` · `cut`: whip | zoom | wipe | page (default hard cut) · top level: `scenes`, `effects` (`{type: "punch", at}`), `theme` (pastel | calm | night), `outro {duration, cut, params}`, `music {track, under_voice_db}` · scene components with a content zone accept `params.dy` (px, nudge down + / up −).

### avatar
Instagram profile picture: Chillar's face, big, centred in the 1080x1080 square at y 420–1500 of the frame (cropped by pipeline/profile_pic.py). Built to survive the circle crop and the 110 px feed size — no text.
`layer scene · min 0.5s`
params: expr="side-eye"

### bar-chart
Bars standing on the bottom of the content zone, straight on the chapter field — no card, no axes, no grid. Each bar is a strip of paper (paper stock, soft contact shadow, seeded blue-ballpoint hatching); the one the line is about is haldi with its value circled by hand. Every bar's value sits above it in the headline face; labels 54 px, caption 44 px (put notes like "example" in caption, never a loose tag). Optional: prefix (e.g. "₹", default "") goes before every value, and a 0 bar then shows as a thin paper slab labelled "₹0" instead of a bare line. bracket (default false): true draws a pen bracket on the taller bar spanning the difference, labelled "+<difference>" (prefix + Indian grouping); a string sets the label text instead. bracketBars ([i, j], optional) picks which two bars to compare (default: the two tallest).
`layer scene · min 1.6s`
params: title="", bars=[{"label": "A", "value": 1}], highlight=-1, caption="", stagger=0.2, prefix="", bracket=false, bracketBars=null

### calendar-flip
Tear-off desk calendar (paper pages, red month band) riffles through pages and lands on the last one — time passing, deadlines, 'since 2020'. Label sits on the field above it.
`layer scene · min 1.6s · sfx whoosh@0.1s`
params: pages=["JAN 2020", "JAN 2023", "OCT 2026"], label="", flip=0.16

### chat-screen
A generic phone chat printed out and lying on the field (paper card, seeded tilt, soft shadow; no app colours or logos). 3–5 messages type in one by one, stagger s apart (first 0.3 s after the cut): 'them' messages after a typing-dots bubble, 'me' messages slide in from the right in a soft haldi tint. Layout is reserved from the cut — nothing reflows. messages: [{from: 'me'|'them', text, time?}] (text takes *marker*; max 6). name (optional) adds a header with a back chevron + initial avatar; pinned (optional) adds a pinned-message bar at the top. highlight (message index, default -1) gets a blue-ballpoint circle drawn 0.3 s after it lands. Timestamps are JetBrains Mono (printout metadata) on a seeded clock; set msg.time to fix one, times:false hides them. width px (560–880, default 820); tilt (deg) fixes the tilt instead of the seeded one. Keep it to ~5 one-line messages so it stays inside the content zone.
`layer scene · min 2.6s · sfx typing@0.05s`
params: messages=[{"from": "them", "text": "Hi"}, …], name="", pinned="", highlight=-1, stagger=0.5, width=820, times=true, tilt=null, dy=0

### checklist
A paper chit list: each item gets a blue-ballpoint tick or a red-pen cross, written in sequence. Title sits on the field above the chit. Optional `grow` (default false): the chit lands holding only the first row and lengthens downward as each later row is written; the final size is reserved, so the title never shifts.
`layer scene · min 1.8s`
params: title="", items=[{"text": "Item", "ok": true}], stagger=0.35, grow=false

### cover
Static 1080x1920 cover (rendered to output/cover.png by cover.py from cover.md) on a note-colour field. Headline left-aligned, kicker under it, an optional stamp and Chillar. Key text sits inside the 3:4 profile-grid crop (y 240–1680). No series label.
`layer scene · min 0.5s`
params: text="UPI ka bill kaun bharta?", kicker="", stamp="", mascot="side-eye"

### glyph-character
A big typographic glyph ("*", "%", "₹", "0%", "T&C") turned into a deadpan character for visual jokes ('the asterisk is the offer's lawyer'): headline-face glyph, Chillar's half-closed eyes, stick limbs and a hand-drawn SVG costume. Centred on x, y (the glyph's ink centre); size = ink height in px (wide glyphs are capped at maxWidth). costume: lawyer (tiny black coat + white bands, one arm raised — 'Objection.') | crown | detective (hat + magnifier) | none. eyes: deadpan | side-eye (pupils toward the bubble) | none. tone: ink (field ink) | red. bubble: optional paper speech bubble on bubbleSide (right | left; the busy arm goes on the other side), kept inside x 60–940. anim: toss (lands at a seeded tilt) | grow — needs line: a torn fine-print slip (y = lineY) ending in a tiny glyph like a footnote mark, which grows into the character growAt s after the cut; the costume drops on as it lands. legs/arms (default true) draw the stick limbs. Keep it clear of the caption band: default y 720 with size 400 ends ~ y 1060.
`layer scene · min 1.2s · sfx coin@0.05s`
params: glyph="*", costume="lawyer", eyes="deadpan", bubble="", bubbleSide="right", size=400, x=380, y=720, tone="ink", anim="toss", line="", lineY=300, growAt=0.45, legs=true, arms=true, maxWidth=620

### hook-card
Frame 1. FULLY DRAWN AT t=0 (no entrance): the question as a big left-aligned headline on the chapter field, a torn receipt stub with the stakes lying under it at a tilt, the last amount circled in blue ballpoint (drawn after frame 1), Chillar side-eyeing. No series label — the question is the headline. Optional: wide:true makes the stakes slip span the content width (≈860 px, bigger print) with Chillar sitting on its top-right corner. dy (px) nudges the whole composition down (+) or up (−) inside the content zone.
`layer scene · min 1.5s`
params: question="UPI free hai. Phir *bill* kaun bharta?", stakes=[{"label": "Chai", "amount": "₹20"}, …], circle=true, mascot="side-eye", size=132, wide=false, dy=0

### line-chart
Compounding curve vs a straight simple-interest/savings line, drawn on a sheet of graph paper lying on the field. End value of the curve circled in blue ballpoint. Values in ₹ (Indian format). Rate/years are illustrative — cite a fact for any real rate.
`layer scene · min 2.0s · sfx ding@1.45s`
params: title="Compounding", principal=10000, rate=0.12, years=30, compare="simple", compareLabel="Simple", curveLabel="Compound", drawDuration=1.2

### marker-highlight
A headline on the chapter field; words wrapped in *asterisks* get the yellow marker swipe. Optional sub line below in the field ink. Left-aligned (align:center only for the one centred moment of a video). Keep it ≤ 6 words. fit (default true): a word wider than the line shrinks the headline (down to 55% of size) instead of breaking mid-word; fit:false restores break-word wrapping. paper (default false): true puts the headline (and sub) on a paper scrap / circular lying on the field at a seeded tilt, tossed in on the cut frame, text in paper ink — use for quotes; ~120 size reads best since the scrap's padding narrows the line.
`layer scene · min 1.2s`
params: text="UPI *free* nahi hai", sub="", size=168, align="left", markerAt=0.25, fit=true, paper=false

### mascot-reaction
Chillar pops up from the bottom of the content zone with an expression + animation and an optional deadpan speech bubble (a paper bubble, no outline). Replaces memes; counts as a re-hook. Can be an overlay on another scene. ring: optional short text on a green profile-photo ring around the coin (e.g. 'open to work'), drawn after the pop. sound: optional meme sound (e.g. 'vine boom'), fetched by pipeline/memes.py (soundPick picks the result), played soundAt s after the pop; it replaces the arrival coin and counts as a meme beat in the reel's meme budget. Default '' keeps the coin.
`layer overlay · min 1.0s · re-hook · sfx coin@0.05s`
params: expr="side-eye", anim="blink", x=760, y=1120, size=320, bubble="", bubbleSide="left", ring="", sound="", soundPick=0, soundAt=0.05

### meme
A real global meme (imgflip template or GIF, fetched at build time by pipeline/memes.py) as a printed photo tossed onto the field, full content width, with optional paper-scrap labels on it and an optional meme sound (myinstants). Cut to it on the word after a punchline. kind image|video (video = silent GIF loop, stepped from a sprite). Pick the exact template with `memes.py search "<q>" --kind <kind>` and set pick. labels: [{text, x, y}] in % of the picture (centre of the scrap). Global memes only — no Indian films/TV/people.
`layer scene · min 1.5s · re-hook`
params: meme="This Is Fine", kind="image", pick=0, headline="", labels=[], sound="", soundPick=0, soundAt=0.0

### meme-format
Recreated meme FORMATS with Chillar and original text — never real meme images. Formats: two-panel (nah/haan), expectation-reality, nobody-me. Each panel is a printed photo lying on the field, spanning the full content width (870 px), punchline text 60 px (48 px with 3 panels), the format word set big in the headline face. Panels drop in order.
`layer scene · min 1.8s · re-hook`
params: format="two-panel", panels=[{"label": "Nah", "text": "Cash mein chillar dhoondna", "expr": "facepalm"}, …], reveal=0.8

### mithai-dabba
Mummy's mithai dabba: a red box with a haldi trim, laddoos in paper cups (rows 6-5-6-5 for 22). Honest share: one laddoo = 1/count. Layouts — hero: big box (letter {title,line,amount,note} under it, Mummy's hand, sticker, static mascot); fully drawn at t=0, good as frame 1; closeAt = the lid standing open behind the box folds shut while Chillar leans in and pushes it. slip: big box on top, payslip below (slip {title, meta, at, rows}); a line with laddoo:true pulls the next laddoo, which arcs high and lands on that row as it prints. close: push-in on the slip — 1-2 big rows, the box corner peeking in top-left. locker: box top-left + a PF locker (locker {label, amount, sub, tag, laddooAt, doorAt, lockAt, openAt}): laddoo flies in, door swings shut, padlock with a paper tag drops; doorAt:null + lockAt:null = already shut and locked at t=0 (fully drawn, good as frame 1); openAt = padlock pops off and the door swings open; locker.inside = a printed paper slip on the shelf, seen once the door opens; box:false (locker layout) = no dabba, the locker alone centred and 1.3× bigger. Lines: {label, amount, sub, icon:'lock', tone: red|green|ink, circle, laddoo, at, amountAt}. removed = laddoos already gone (empty cups). Times are seconds from the scene start; null = already there.
`layer scene · min 1.2s`
params: layout="hero", count=22, removed=0, remove=[], letter=null, sticker="", stickerStrike=null, hand=false, mascot="", slip=null, lines=[], locker=null, closeAt=null, box=true

### odometer-number
One huge number rolls up like an odometer (Indian digit grouping); with `from` it instead counts from→value as one legible tabular number (e.g. ₹1,00,000 → ₹86,468), set straight on the chapter field and double-underlined by hand. Use for the big reveal of a ₹ amount or %. tone red/green only on light fields (bone, note20, note50); on dark fields the number stays in the field ink. dy (px) nudges the whole composition down (+) or up (−) inside the content zone.
`layer scene · min 1.6s · sfx ding@1.25s`
params: value=3631, from=null, prefix="₹", suffix="", decimals=null, label="", unit="", sub="", tone="field", size=270, underline=true, rollStart=0.15, rollDuration=0.9, dy=0

### passbook-page
An open bank passbook page lying on the field: printed column heads, entries printed dot-matrix style one line at a time (printer buzz), running balance computed, the final balance circled in blue ballpoint. Debits red, credits green. The most Chillar object there is — strong as frame 1 (printed:true) or as the growing-receipt meter.
`layer scene · min 1.8s · sfx printer@0s`
params: opening=10000, rows=[{"date": "01-10", "text": "Salary", "amount": 50000, "type": "cr"}], step=0.24, printed=false, circleBalance=true

### progress-meter
The chillar meter: a row of ₹1 coins along the top (y≈170, decorative, outside the content zone). Filled coins are haldi, the rest are empty rings in the field ink; each newly earned coin drops in. Place one per chapter; it fills from→to (fractions of the row).
`layer overlay · min 0.6s · sfx coin@0.1s`
params: from=0, to=0.5, coins=8

### receipt-list
Thermal receipt that prints line by line (stepped) out of a printer slot, lying on the field; the paper feeds out with the print, so it is always sized to the lines already printed (rows 46 px, meta/footer 36 px). The total is circled in blue ballpoint after it prints. Great as frame 1 (printed:true shows it fully at t=0) or as a growing receipt meter. Optional: width (paper px, default 760, max 860; the printer is 100 px wider, capped at 880); stampTotal:true slams the total amount on as a textured red rubber-stamp mark (instead of the ballpoint circle) once it prints. dy (px) nudges the whole composition down (+) or up (−) inside the content zone. totalAt (s from scene start, optional) holds the total block until then, so the amount lands on its word.
`layer scene · min 1.5s · sfx printer@0s`
params: title="UPI RECEIPT", meta="", items=[{"label": "Chai", "amount": "₹20"}], total={"label": "TOTAL", "amount": "₹20", "tone": "ink"}, footer="", circleTotal=true, step=0.22, printed=false, width=760, stampTotal=false, dy=0, totalAt=null

### salary-slip
Payslip lying on the field: earnings in green, deductions in red with minus, rows print in steps, net pay rolls on an odometer and gets a double ballpoint underline. Amounts are numbers (formatted en-IN).
`layer scene · min 2.5s · sfx printer@0s, ding@2.1s`
params: title="Salary slip", month="OCT 2026", rows=[{"label": "Basic", "amount": 50000, "type": "earn"}], netLabel="In-hand", step=0.2

### split-compare
Myth vs Math: the MYTH chit lands, gets scratched out with a red pen, then the MATH chit is slapped down below it (record-scratch twist). The chits never overlap: they keep a clear gap of at least `gap` px (default 30) at their closest tilted corners. Main text is set at headline scale, sized by the longer side (textSize "auto": ≤8 chars 128 px, ≤14 → 100, ≤22 → 80, else 66; or a px number). Works best on the note2000 field.
`layer scene · min 1.8s · re-hook · sfx scratch@0.85s`
params: left={"title": "Myth", "text": "UPI free hai"}, right={"title": "Math", "text": "Sarkar ne ₹3,631 crore bhare"}, strikeAt=0.6, revealAt=0.9, gap=30, textSize="auto"

### stamp
The thappa: a stamp-pad red rubber stamp slams in (140%→100% in 4 frames + 2-frame shake) on a scrap of paper, so it reads on every field. Ink is textured (not a clean vector). Max 3 per video. Overlay on top of a scene.
`layer overlay · min 1.2s · re-hook · sfx stamp@0.133s`
params: text="MDR 0%", sub="", x=540, y=760, rotate=-8, size=150

### statement
One big statement on the chapter field: headline (≤ 6 words, *marker* words swipe yellow) and an optional body line. With paper:true the body is a hand-torn chit lying under the headline (definitions, fine print). Left-aligned on the shared edge. Optional: body may be an array of lines (or use \n) to break it on purpose; width (px, default 0 = full 860) narrows the chit/body so a mascot overlay can sit beside it without covering text. Optional: tilt (deg) fixes the chit's tilt instead of the seeded one; markerAt (s) is when the marker swipe starts (default 0.3). fit (default true): a word wider than the line shrinks the headline (down to 55% of size) instead of breaking mid-word; fit:false keeps the fixed size. dy (px) nudges the whole composition down (+) or up (−) inside the content zone.
`layer scene · min 1.2s`
params: title="MDR kya hai?", body="", paper=false, size=156, width=0, tilt=null, markerAt=0.3, dy=0, fit=true

### tier-compare
₹100 vs ₹1,000 vs ₹1,00,000 escalation: three paper columns standing on the bottom of the content zone, each taller than the last, revealed in sequence; the last result gets a ballpoint circle. The row spans the full content width (≈ 876 px) once every column stands. reveal: 'bars' (default — each column rises in turn, then its result) or 'results' (all columns rise together on the cut so the paper spans the full width from frame 1; only the results step in, `stagger` apart). Optional: wide (default false) stretches the row to the full ≈876 px content width whatever the tier count (2 tiers otherwise stay 276 px columns); width (px, default 0 = auto) sets the row width exactly (max 880). amtSize / resSize (px, default 0 = 44 / 64, last result 92) enlarge the amount and result text; amtSize lets the amount wrap onto two lines in its bar instead of shrinking. A row of 4+ tiers always shrinks to fit the content width.
`layer scene · min 2.6s · sfx coin@0.1s, ding@2.0s`
params: title="", tiers=[{"amount": "₹100", "result": ""}, …], stagger=0.9, reveal="bars", wide=false, width=0, amtSize=0, resSize=0

## Placed by the pipeline

### captions  _(auto — never place in scenes.json)_
Word-highlight captions in the caption band (y 1150–1450). Mukta ExtraBold in the chapter field's ink; the active word gets a flat haldi highlight with ink text (no shadow, no box outline). Built automatically from words.json — not placed in scenes. Lines wrap balanced (text-wrap: balance) and the last two words never split, so no line ends on a one-word widow.
`layer captions`

### chapter-field  _(auto — never place in scenes.json)_
The ground of every frame: one flat rupee-note colour per chapter (fields in brand/tokens.json), switched with a hard cut on the chapter's first scene. Sets --field / --on-field on #root so every scene and the captions take the right ink. Print grain on top. Always on, full duration, track 0 — inserted automatically.
`layer background · min 1s`

### outro  _(auto — never place in scenes.json)_
Every video ends here (bone field): a thermal receipt prints 'Is video ka MDR: 0%. Gyaan free hai.', then the follow stub tears off along the perforation. Includes the 'Educational only' disclaimer.
`layer scene · min 2.8s · sfx printer@0.0s, coin@2.1s`

### transition  _(auto — never place in scenes.json)_
A real editor's transition between two shots — never a title card. It moves the outgoing and incoming scenes themselves (or wipes the next chapter's field across), centred on the cut. Styles: whip (out left 4f, in from right 5f, hard cut between), zoom (punch through the old shot, land on the new), wipe (next field colour slides up over the frame, cut under it), page (a blank passbook page turns over the frame). Carries NO text. Placed from a scene's "cut" key; plain hard cuts need no clip.
`layer transition · min 0.2s · sfx whoosh@0.0s · styles whip/zoom/wipe/page`

### wordmark  _(auto — never place in scenes.json)_
The channel handle (@chillar.ind) with a tiny coin, bottom-left just under the caption band (box in brand/tokens.json "wordmark"), in the field's ink. On every frame from 0 to the outro, so downloads and reshares carry the name. Inserted automatically — never placed in scenes.json.
`layer overlay · min 0.5s`
