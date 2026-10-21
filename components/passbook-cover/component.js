// passbook-cover — front cover, only the name line filled in.
CH.define("passbook-cover", {
  build({ el, p, t, tl, rng }) {
    const W = Math.min(880, +p.width || 800), H = Math.round(W * 0.72);
    const tilt = CH.tilt(rng, 2);
    const nm = String(p.name || "");
    const uw = Math.min(W * 0.62, 34 * nm.length + 30);
    el.innerHTML = `<div class="pc-book" style="left:${+p.x}px; top:${+p.y}px; width:${W}px; height:${H}px; transform: rotate(${tilt.toFixed(2)}deg)">
      <div class="pc-spine"></div><div class="pc-coin">₹</div>
      <div class="pc-title">${CH.esc(p.title || "")}</div>
      <div class="pc-label"><span class="pc-name">${CH.esc(nm)}${CH.scribble("underline", { x: 0, y: 66, w: uw, h: 16, rng, stroke: 6 })}</span></div></div>`;
    CH.toss(tl, el.querySelector(".pc-book"), t, tilt);
    CH.draw(tl, el.querySelector(".pc-name"), t + 0.35, 0.35);
  },
});
