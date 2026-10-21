// photo-frame — a framed photo + a speech bubble from someone off-screen.
CH.define("photo-frame", {
  build({ el, p, t, tl, rng }) {
    const tilt = CH.tilt(rng), side = p.side === "right" ? "right" : "left";
    const fw = Math.min(860, +p.frameWidth || 620);
    el.innerHTML = `<div class="zone"><div class="pf-stack">
      <div class="pf-bubble ${side} t-body">${CH.rich(p.speech || "")}${p.speaker ? `<div class="pf-who">${CH.esc(p.speaker)}</div>` : ""}</div>
      <div class="pf-frame paper-obj" style="width:${fw}px; transform: rotate(${tilt.toFixed(2)}deg)"><div class="pf-mat"><div class="pf-photo"><div class="pf-head"></div><div class="pf-body"></div></div></div>
      ${p.caption ? `<div class="pf-cap">${CH.esc(p.caption)}</div>` : ""}</div></div></div>`;
    CH.toss(tl, el.querySelector(".pf-frame"), t, tilt);
    CH.pop(tl, el.querySelector(".pf-bubble"), t + 4 * CH.F);
  },
});
