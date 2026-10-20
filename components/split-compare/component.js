CH.define("split-compare", {
  build({ el, p, t, tl, rng }) {
    const L = p.left || {}, R = p.right || {};
    const t1 = CH.tilt(rng, 2.4), t2 = -Math.sign(t1) * Math.abs(CH.tilt(rng, 1.6));
    // main text at headline scale, sized by the longer side so both chits match (textSize: "auto" | px)
    const plain = (s) => String(s || "").replace(/\*/g, "");
    const longest = Math.max(plain(L.text).length, plain(R.text).length, 1);
    const fs = +p.textSize > 0 ? +p.textSize
      : longest <= 8 ? 128 : longest <= 14 ? 100 : longest <= 22 ? 80 : 66;
    const cw = fs * 0.5, LW = 740;                          // Mukta ExtraBold ≈ 0.5em per char
    const tw = plain(L.text).length * cw, lw = Math.min(LW, tw), lh = fs * 1.08;
    // one red scratch per wrapped line, so a long myth is struck out all the way
    const nl = Math.max(1, Math.ceil(tw / LW));
    const strikes = Array.from({ length: nl }, (_, i) => CH.scribble("strike", {
      x: -10, y: i * lh, w: (i === nl - 1 && nl > 1 ? Math.max(140, tw - (nl - 1) * LW) : lw) + 20, h: lh, rng, stroke: Math.max(7, Math.round(fs / 11)) })).join("");
    // clear gap between the chits whatever the tilt: ≥ `gap` px at the closest corner
    const half = 420, rise = half * (Math.sin(Math.abs(t1) * Math.PI / 180) + Math.sin(Math.abs(t2) * Math.PI / 180));
    const gap = Math.max(30, +p.gap || 30) + Math.ceil(rise);
    el.innerHTML = `
      <div class="zone" style="gap:${gap}px">
        <div class="sc-chit sc-myth paper-obj" style="transform: rotate(${t1.toFixed(2)}deg)">
          <div class="sc-word t-head">${CH.esc(L.title)}</div>
          <div class="sc-text t-body" style="font-size:${fs}px">${CH.rich(L.text)}${strikes}</div>
        </div>
        <div class="sc-chit sc-math paper-obj" style="transform: rotate(${t2.toFixed(2)}deg)">
          <div class="sc-word t-head">${CH.esc(R.title)}</div>
          <div class="sc-text t-body" style="font-size:${fs}px">${CH.rich(R.text)}</div>
        </div>
      </div>`;
    CH.toss(tl, el.querySelector(".sc-myth"), t, t1);
    CH.draw(tl, el.querySelector(".sc-myth"), t + (+p.strikeAt), 0.22);
    CH.toss(tl, el.querySelector(".sc-math"), t + (+p.revealAt), t2, { frames: 5, y: 140, twist: 8 });
    CH.markers(tl, el.querySelector(".sc-math"), t + (+p.revealAt) + 0.3);
  },
});
