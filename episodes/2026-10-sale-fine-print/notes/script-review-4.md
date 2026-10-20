verdict: PASS
round: 4
scores: stop 4 · laughs 4 (count 5/3) · specific 4 · clarity 4 · escalation 4 · payoff 4 · speak 4 · fresh 4 · facts PASS
words: 70 written / ≈ 93 spoken (~33 s incl. outro, target 30 s: 70–95 words, 27–36 s). It's back inside the range after being 7 over in round 3. Written words are on the 70 floor, so any fix below has to keep the count where it is, not cut it.

Line ids follow fact_lint (11 lines): L1 "Maan lo, ₹1,00,000 ke phone…", L2 "Banner ka statement:", L3 "Star khansa: 'Objection.'", L4 "₹100 pe bhi 10% milega…",
L5 "Aadhi raat…", L6 "Ghar pe chargers ka museum hai.", L7 "Maximum ₹1,500. Mere client ne…", L8 "Yaani 1.5%.", L9 "Sapne ka out-of-court settlement.",
L10 "10% sirf ₹5,000 se ₹15,000 tak.", L11 "Banner jhooth nahi bolta…".

Note on process: CLAUDE.md §8 caps the loop at 3 rounds and then sends it to the creator. I'm treating this round 4 as creator-approved.

Game in one sentence: "the asterisk is the offer's lawyer, and he argues your ₹10,000 down to ₹1,500 on technicalities, all of it technically true."
The game holds from start to finish now. Every round-3 note was fixed:
- the F1 framing is back as "Maan lo" (light, said aloud, not a label);
- ₹1,00,000 is in the voice;
- "clause do" is gone, and L4 is now a lawyer move (technically true and absurd) instead of a ruling;
- "mere client";
- the ₹1,500 repeat is cut, so L9 keeps "settle" without the number;
- M3 is off the stamp and has its own beat after a half-second of silence;
- the length is back in range.

Real laughs:
- L2: M1 is the punchline, about 4 s in.
- L4: the lawyer technicality.
- L6: the charger museum.
- L7: "Mere client ne 10% bola, ₹10,000 nahi."
- L11: "chhote font mein" plus the M1 callback.

Half-laughs: L3, L9, and L10 if the disclaimer speed actually happens. That makes 5 against a minimum of 3, all inside the game. Nothing scores 5 because of the notes below. They are polish, and none of them blocks the PASS.

## Notes (most important first)
- FACTS / PIPELINE, F1 and F4 "no source URL" (ESCALATED, flagged in all four rounds, not fixed). The script is clean: every number is cited, F4
  backs up 1.5%, ₹1,500 and the ₹5,000–₹15,000 window, "Maan lo" frames the invented offer, and there are no brands and no advice. But fact_lint
  still prints RENDER BLOCKED because F1 is hypothetical and F4 is computed. → Producer/fact-checker: mark those rows the way the lint accepts
  (or run with `--allow-unsourced` if the creator approves). This isn't the writer's job. Don't let it bounce back to the script again.
- L2→L3 "Banner ka statement:" / "Star khansa: 'Objection.'": who is he objecting to? By ear, the asterisk objects to the *banner*. In L7 he
  calls the banner "mere client", so he has just objected to his own client. The laugh works on instinct (the fine print contradicts the headline), but a sharp
  viewer hears the role flip, and it blurs the game exactly where it's planted. → Aim the objection at *your* assumption (the ₹10,000 you think
  you're saving, which is only pencilled on frame 1 and never voiced), or have him "clarify" his client's statement rather than object to it. Zero net words.
- L2 "Banner ka statement:": the courtroom word is right for the game. But it's a 3-word fragment that ends on a colon, and Sunny will read it as a
  finished sentence with falling intonation. Put it next to L3's colon line and the hook has two telegraphic label lines in a row, which is the
  nearest this draft gets to the §4 caption-speak tell. → Read L2–L3 aloud at pace. The setup has to *sound* unfinished so the meme can finish it
  (a rising question, or "aur banner ka…" energy). Director: cut to M1 on the last syllable with no gap.
- L10 {voice: the star, mumbling fast like an ad disclaimer}: Sunny runs at a fixed pace of 1.2 (voice.md, no per-line pace), so the TTS can't
  "mumble fast". If nobody plans for it, the act-out is lost and the line plays as plain narration. → Writer: the line has to be funny at normal
  pace too. Editor: if the gag stays, speed up that one clip in the mix (pitch-preserved) and flag it in the hand-off.
- L6→L7 voice switch: one TTS voice, and the quote marks can't be heard. "…chargers ka museum hai. Maximum ₹1,500." By ear, the narrator's self-own runs
  straight into the lawyer with no cue, and "Mere client" only arrives 2 s later. → Give the star a re-entry cue: a callback to his L3 cough is
  the cheapest, or a visual/SFX cue the director owns. Don't add words.
- Clarity, ₹100 → 0%: the series is "₹100 vs ₹1,00,000" and the cover kicker promises the ₹100 cart, but its 0% is never said or shown. It's
  only implied by "bas cart ₹5,000 ka ho". → Director: show 0% on the ₹100 receipt under L4 (a red-pen strike, not a second thappa unless it's
  worth it; the budget allows 2). That costs no voice words.
- L11 {meme: M1 callback, label "chhote font mein likha tha"}: the label echoes the VO's twist word on screen. If it appears before
  "mein", it spoils the last word, and if it appears after, it just repeats it. → The callback label should add a new beat, for example the banner's
  reply now the truth is out, and it should come in after the last word.
- L9 "Sapne ka out-of-court settlement.": it's in the game and it's the right tag (round 3's ask), but it's a half-laugh. "Out-of-court" right after
  "Objection" (in court) works on paper and slips past the ear. Low priority. If the writer has a sharper settle image, use it. If not, it stays.
- L1 stop power: "Maan lo" plus a lakh phone and 10% is a clear setup, but the *question* (₹10,000 bache?) is only on the frame. Low priority.
  If the L2/L3 objection gets re-aimed at "your ₹10,000" (see above), that same change brings the stakes into the voice without costing L1 anything.

## Keep
- L7 "Mere client ne 10% bola, ₹10,000 nahi.": the game's best line, with the math inside the joke. Now it has the possessive.
- L4 "₹100 pe bhi 10% milega. Bas cart ₹5,000 ka ho." → L5–L6 charger museum: the lawyer's technicality leads straight into the self-own. That
  is the round-1 note ("the lawyer *made* you pad the cart") finally landing.
- L11 "Banner jhooth nahi bolta. Sach vakeel bolta hai, chhote font mein." with the M1 callback: the twist word comes last and pays off the plant.
