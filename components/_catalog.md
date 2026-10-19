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
Bars standing on the bottom of the content zone, straight on the chapter field — no card, no axes, no grid. Bars are paper; the one the line is about is haldi with its value circled by hand. Values in the headline face above each bar. Optional: prefix (e.g. "₹", default "") goes before every value, and a 0 bar then shows as a thin paper slab labelled "₹0" instead of a bare line.
`layer scene · min 1.6s`
params: title="", bars=[{"label": "A", "value": 1}], highlight=-1, caption="", stagger=0.2, prefix=""

### calendar-flip
Tear-off desk calendar (paper pages, red month band) riffles through pages and lands on the last one — time passing, deadlines, 'since 2020'. Label sits on the field above it.
`layer scene · min 1.6s · sfx whoosh@0.1s`
params: pages=["JAN 2020", "JAN 2023", "OCT 2026"], label="", flip=0.16

### checklist
A paper chit list: each item gets a blue-ballpoint tick or a red-pen cross, written in sequence. Title sits on the field above the chit.
`layer scene · min 1.8s`
params: title="", items=[{"text": "Item", "ok": true}], stagger=0.35

### cover
Static 1080x1920 cover (rendered to output/cover.png by cover.py from cover.md) on a note-colour field. Headline left-aligned, kicker under it, an optional stamp and Chillar. Key text sits inside the 3:4 profile-grid crop (y 240–1680). No series label.
`layer scene · min 0.5s`
params: text="UPI ka bill kaun bharta?", kicker="", stamp="", mascot="side-eye"

### hook-card
Frame 1. FULLY DRAWN AT t=0 (no entrance): the question as a big left-aligned headline on the chapter field, a torn receipt stub with the stakes lying under it at a tilt, the last amount circled in blue ballpoint (drawn after frame 1), Chillar side-eyeing. No series label — the question is the headline. Optional: wide:true makes the stakes slip span the content width (≈860 px, bigger print) with Chillar sitting on its top-right corner. dy (px) nudges the whole composition down (+) or up (−) inside the content zone.
`layer scene · min 1.5s`
params: question="UPI free hai. Phir *bill* kaun bharta?", stakes=[{"label": "Chai", "amount": "₹20"}, …], circle=true, mascot="side-eye", size=132, wide=false, dy=0

### line-chart
Compounding curve vs a straight simple-interest/savings line, drawn on a sheet of graph paper lying on the field. End value of the curve circled in blue ballpoint. Values in ₹ (Indian format). Rate/years are illustrative — cite a fact for any real rate.
`layer scene · min 2.0s · sfx ding@1.45s`
params: title="Compounding", principal=10000, rate=0.12, years=30, compare="simple", compareLabel="Simple", curveLabel="Compound", drawDuration=1.2

### marker-highlight
A headline on the chapter field; words wrapped in *asterisks* get the yellow marker swipe. Optional sub line below in the field ink. Left-aligned (align:center only for the one centred moment of a video). Keep it ≤ 6 words.
`layer scene · min 1.2s`
params: text="UPI *free* nahi hai", sub="", size=168, align="left", markerAt=0.25

### mascot-reaction
Chillar pops up from the bottom of the content zone with an expression + animation and an optional deadpan speech bubble (a paper bubble, no outline). Replaces memes; counts as a re-hook. Can be an overlay on another scene. ring: optional short text on a green profile-photo ring around the coin (e.g. 'open to work'), drawn after the pop.
`layer overlay · min 1.0s · re-hook · sfx coin@0.05s`
params: expr="side-eye", anim="blink", x=760, y=1120, size=320, bubble="", bubbleSide="left", ring=""

### meme-format
Recreated meme FORMATS with Chillar and original text — never real meme images. Formats: two-panel (nah/haan), expectation-reality, nobody-me. Each panel is a printed photo lying on the field, the format word set big in the headline face. Panels drop in order.
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
Thermal receipt that prints line by line (stepped) out of a printer slot, lying on the field. The total is circled in blue ballpoint after it prints. Great as frame 1 (printed:true shows it fully at t=0) or as a growing receipt meter. Optional: width (paper px, default 760, max 860; the printer is 100 px wider, capped at 880); stampTotal:true slams the total amount on as a textured red rubber-stamp mark (instead of the ballpoint circle) once it prints. dy (px) nudges the whole composition down (+) or up (−) inside the content zone. totalAt (s from scene start, optional) holds the total block until then, so the amount lands on its word.
`layer scene · min 1.5s · sfx printer@0s`
params: title="UPI RECEIPT", meta="", items=[{"label": "Chai", "amount": "₹20"}], total={"label": "TOTAL", "amount": "₹20", "tone": "ink"}, footer="", circleTotal=true, step=0.22, printed=false, width=760, stampTotal=false, dy=0, totalAt=null

### salary-slip
Payslip lying on the field: earnings in green, deductions in red with minus, rows print in steps, net pay rolls on an odometer and gets a double ballpoint underline. Amounts are numbers (formatted en-IN).
`layer scene · min 2.5s · sfx printer@0s, ding@2.1s`
params: title="Salary slip", month="OCT 2026", rows=[{"label": "Basic", "amount": 50000, "type": "earn"}], netLabel="In-hand", step=0.2

### split-compare
Myth vs Math: the MYTH chit lands, gets scratched out with a red pen, then the MATH chit is slapped down over its lower half (record-scratch twist). Works best on the note2000 field.
`layer scene · min 1.8s · re-hook · sfx scratch@0.85s`
params: left={"title": "Myth", "text": "UPI free hai"}, right={"title": "Math", "text": "Sarkar ne ₹3,631 crore bhare"}, strikeAt=0.6, revealAt=0.9

### stamp
The thappa: a stamp-pad red rubber stamp slams in (140%→100% in 4 frames + 2-frame shake) on a scrap of paper, so it reads on every field. Ink is textured (not a clean vector). Max 3 per video. Overlay on top of a scene.
`layer overlay · min 1.2s · re-hook · sfx stamp@0.133s`
params: text="MDR 0%", sub="", x=540, y=760, rotate=-8, size=150

### statement
One big statement on the chapter field: headline (≤ 6 words, *marker* words swipe yellow) and an optional body line. With paper:true the body is a hand-torn chit lying under the headline (definitions, fine print). Left-aligned on the shared edge. Optional: body may be an array of lines (or use \n) to break it on purpose; width (px, default 0 = full 860) narrows the chit/body so a mascot overlay can sit beside it without covering text. Optional: tilt (deg) fixes the chit's tilt instead of the seeded one; markerAt (s) is when the marker swipe starts (default 0.3). dy (px) nudges the whole composition down (+) or up (−) inside the content zone.
`layer scene · min 1.2s`
params: title="MDR kya hai?", body="", paper=false, size=156, width=0, tilt=null, markerAt=0.3, dy=0

### tier-compare
₹100 vs ₹1,000 vs ₹1,00,000 escalation: three paper columns standing on the bottom of the content zone, each taller than the last, revealed in sequence; the last result gets a ballpoint circle.
`layer scene · min 2.6s · sfx coin@0.1s, ding@2.0s`
params: title="", tiers=[{"amount": "₹100", "result": ""}, …], stagger=0.9

## Placed by the pipeline

### captions  _(auto — never place in scenes.json)_
Word-highlight captions in the caption band (y 1150–1450). Mukta ExtraBold in the chapter field's ink; the active word gets a flat haldi highlight with ink text (no shadow, no box outline). Built automatically from words.json — not placed in scenes.
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
