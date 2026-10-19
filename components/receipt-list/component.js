CH.define("receipt-list", {
  build({ el, p, t, tl, rng }) {
    const tilt = CH.tilt(rng, 1.2);
    const rows = (p.items || []).map((it) => `
      <div class="rc-row rc-line"><span class="rc-l">${CH.esc(it.label)}</span><span class="rc-a">${CH.esc(it.amount)}</span></div>`).join("");
    const tone = (p.total && p.total.tone) || "ink";
    const tot = p.total ? String(p.total.amount) : "";
    el.innerHTML = `
      <div class="zone">
        <div class="rc-printer"><div class="rc-slot"></div></div>
        <div class="rc-wrap torn-wrap" style="transform: rotate(${tilt.toFixed(2)}deg); transform-origin: 50% 0%"><div class="rc-paper paper-torn t-print">
          <div class="rc-title rc-line">${CH.esc(p.title)}</div>
          ${p.meta ? `<div class="rc-meta rc-line">${CH.esc(p.meta)}</div>` : ""}
          <div class="rc-rule rc-line"></div>
          ${rows}
          ${p.total ? `<div class="rc-rule2 rc-line"></div>
          <div class="rc-row rc-total rc-line tone-${tone}"><span class="rc-l">${CH.esc(p.total.label)}</span><span class="rc-a">${CH.esc(tot)}${
            p.circleTotal ? CH.scribble("circle", { x: -22, y: -2, w: 33 * tot.length + 36, h: 80, rng }) : ""}</span></div>` : ""}
          ${p.footer ? `<div class="rc-foot rc-line">${CH.esc(p.footer)}</div>` : ""}
        </div></div>
      </div>`;
    const lines = [...el.querySelectorAll(".rc-line")];
    const paper = el.querySelector(".rc-paper");
    if (!p.printed) {
      CH.pop(tl, el.querySelector(".rc-printer"), t, { frames: 5, y: -20 });
      const end = CH.print(tl, lines, t + 0.12, +p.step || 0.22);
      CH.draw(tl, paper, end + 0.05, 0.3);
    } else {
      CH.draw(tl, paper, t + 0.3, 0.3);
    }
  },
});
