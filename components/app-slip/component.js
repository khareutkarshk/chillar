// app-slip — phone purchase slip with a shiny gold badge; blue-pen arrow + note drawn on later.
CH.define("app-slip", {
  build({ el, p, t, tl, rng }) {
    const W = Math.min(880, +p.width || 860), H = 340, noteH = 200;
    const tilt = CH.tilt(rng, 2);
    el.innerHTML = `<div class="as-slip" style="left:${+p.x}px; top:${+p.y}px; width:${W}px; height:${H}px; transform: rotate(${tilt.toFixed(2)}deg)">
      <div class="as-title">${CH.esc(p.title || "")}</div>
      <div class="as-row"><span>${CH.esc(p.item || "")}</span></div>
      <div class="as-row" style="margin-top:12px"><b>₹${CH.inr(+p.amount || 0)}</b></div>
      <div class="as-badge">${CH.esc(p.badge || "")}</div>
      ${CH.scribble("arrow", { x: W - 330, y: 215, w: 200, h: H - 115, rng, stroke: 7 })}
      <div class="as-note" style="left:${W - 600}px; top:${H + 100}px; opacity:0">${CH.esc(p.note || "")}</div></div>`;
    CH.toss(tl, el.querySelector(".as-slip"), t, tilt);
    const at = t + (p.noteAt == null ? 0.8 : +p.noteAt), root = el.querySelector(".as-slip");
    const end = CH.draw(tl, root, at, 0.4);
    tl.set(el.querySelector(".as-note"), { opacity: 1 }, end);
    void noteH;
  },
});
