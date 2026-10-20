// envelope — an addressed paper envelope (letter beats). Frame-1 safe: fully drawn, tossed on the cut.
CH.define("envelope", {
  build({ el, p, t, tl, rng }) {
    const W = Math.min(880, +p.width || 860), H = Math.round(W * 0.62);
    const lines = (p.lines || []).map((l) => `<span class="t-body">${CH.esc(l)}</span>`).join("");
    const pin = p.pincode ? `<span class="ev-pin">${CH.esc(p.pincode)}${CH.scribble("underline", { x: 0, y: 70, w: 40 * String(p.pincode).length + 20, h: 16, rng, stroke: 6 })}</span>` : "";
    const tilt = CH.tilt(rng, 2);
    el.innerHTML = `<div class="ev-env" style="left:${+p.x}px; top:${+p.y}px; width:${W}px; height:${H}px; transform: rotate(${tilt.toFixed(2)}deg)">
      <div class="ev-flap"></div>
      <svg class="ev-fold" viewBox="0 0 100 36" preserveAspectRatio="none"><path d="M0 0 L50 36 L100 0" vector-effect="non-scaling-stroke"/></svg>
      <div class="ev-corner">₹1</div>${p.postmark ? `<div class="ev-mark">${CH.esc(p.postmark)}</div>` : ""}
      <div class="ev-addr">${lines}${pin}</div></div>`;
    CH.toss(tl, el.querySelector(".ev-env"), t, tilt);
    if (p.pincode) CH.draw(tl, el.querySelector(".ev-pin"), t + 0.35, 0.3);
  },
});
