verdict: PASS
round: 1
swipe risk: 0–3s low · 3–15s low · middle med · payoff low

## Prior notes
- none (round 1)

## qa (0 errors, 4 warnings — routed)
- small-object t=3.02 papa-dabba, t=24.3 their-big-box, t=49.06 small-dabba: [director|component:mithai-dabba] paper spans 175–362 px. The frame at 3.02 shows the box at about 700 px, so the measure is probably the inner tray. Polish only.
- empty-paper t=13.59 meme-bas-karo: [director|component:meme] the meme card is filled in the frame, so the warning is minor.
- voice_check: 0 flagged lines, nothing to route. L7/L8 at 60% are ASR noise on "तीस/30".
- sfx_dropped: whoosh at 14.27 (zoom transition) lost to the stamp, and the outro printer lost to a coin. Neither joke depends on them.

## Notes
- [director] polish t=23.54 and t=47.94: "Unka: bada wala" and "Aura: kam" show the same 22-piece box as "Sirf ek" at 2.02. The big-vs-small joke is carried only by the sticker. Fix: vary `count` (e.g. a 2×-size box with 30 pieces for "bada wala", 6 pieces for "kam") and set `removed`/`remove` for the small one. Also set `sticker` to the same text size as the others.
- [director] polish t=50.18 meme-aura: the "−400 aura" label sits on the photo and the caption underneath says only "Ab bolo,". The headline "Bada dabba wale log" also lands before the voice has said the aura line (L18 ends at 49.8). Fix: move the meme to start at 49.3 on "aura kam", or keep the timing and change the label to "−400 ka aura".
- [director] polish t=12.78 meme-bas-karo: the headline "List abhi shuru hui" is fine, but the meme arrives about 0.1 s after "naam" and holds into "Maan lo list mein". Fix: shorten the scene to end at 14.0 so the thirty-receipt zoom lands on "तीस". The paper is small and sits high. Use `height` or `wide:true` to fill the content zone.
- [director] polish t=33.56 gst-cut: the box is 573 px wide and sits left. This is deliberate left-aligned layout, so no change is needed. Fixing the ASR-noisy line L14 ("बारह से पान्च percent घटा") isn't needed either.
- [editor] polish t=14.27: the dropped whoosh leaves the zoom transition silent. Optional: move stamp-18000 to 16.2 so both play.

Frames checked this round: 0, 3.02, 13.59, 24.3 (via sheet), 34.5, 49.06, 50.8. The contact sheet shows a complete outro with the disclaimer and the wordmark on every frame until the outro. No AI-look tells: no eyebrow labels, no structure words. The fields change on each chapter cut. Stamps: 2 (within the 60 s budget of 2–3). Styled cuts: zoom 14.4 and wipe 40.88, spaced more than 12 s apart. Memes: 2 (a crying-men image and the aura video clip). Both are within the budget of 5. The Indian image is fine and the video is global.
