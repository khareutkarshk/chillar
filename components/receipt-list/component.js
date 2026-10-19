CH.define("receipt-list", {
  build({ el, p, t, tl, rng }) {
    const tilt = CH.tilt(rng, 1.2);
    const rows = (p.items || []).map((it) => `
      <div class="rc-row rc-line"><span class="rc-l">${CH.esc(it.label)}</span><span class="rc-a">${CH.esc(it.amount)}</span></div>`).join("");
    const tone = (p.total && p.total.tone) || "ink";
    const tot = p.total ? String(p.total.amount) : "";
    const W = Math.min(860, Math.max(400, +p.width || 760));
    el.innerHTML = `
      <div class="zone">
        <div class="rc-printer" style="width:${Math.min(880, W + 100)}px"><div class="rc-slot"></div></div>
        <div class="rc-wrap torn-wrap" style="transform: rotate(${tilt.toFixed(2)}deg); transform-origin: 50% 0%"><div class="rc-paper paper-torn t-print" style="width:${W}px">
          <div class="rc-title rc-line">${CH.esc(p.title)}</div>
          ${p.meta ? `<div class="rc-meta rc-line">${CH.esc(p.meta)}</div>` : ""}
          <div class="rc-rule rc-line"></div>
          ${rows}
          ${p.total ? `<div class="rc-rule2 rc-line"></div>
          <div class="rc-row rc-total rc-line tone-${tone}${p.stampTotal ? " has-stamp" : ""}"><span class="rc-l">${CH.esc(p.total.label)}</span>${p.stampTotal
            ? `<span class="rc-a"><span class="rc-stampmark">${CH.esc(tot)}</span></span>`
            : `<span class="rc-a">${CH.esc(tot)}${p.circleTotal ? CH.scribble("circle", { x: -22, y: -2, w: 33 * tot.length + 36, h: 80, rng }) : ""}</span>`}</div>` : ""}
          ${p.footer ? `<div class="rc-foot rc-line">${CH.esc(p.footer)}</div>` : ""}
        </div></div>
      </div>`;
    const lines = [...el.querySelectorAll(".rc-line")];
    const paper = el.querySelector(".rc-paper");
    if (!p.printed) {
      CH.pop(tl, el.querySelector(".rc-printer"), t, { frames: 5, y: -20 });
      const step = +p.step || 0.22, tot = el.querySelector(".rc-total");
      // totalAt (s from scene start): the total block (double rule onwards) waits for the voice
      const cut = tot && p.totalAt !== null && p.totalAt !== undefined && p.totalAt !== "" ? lines.indexOf(tot) - 1 : lines.length;
      let end = CH.print(tl, lines.slice(0, cut), t + 0.12, step);
      if (cut < lines.length) end = CH.print(tl, lines.slice(cut), Math.max(end, t + (+p.totalAt) - step), step);
      CH.draw(tl, paper, end + 0.05, 0.3);
      const sm = el.querySelector(".rc-stampmark");
      if (sm) {   // slams onto the paper right after the total line prints
        const at = cut < lines.length ? Math.max(t + 0.12 + cut * step, t + (+p.totalAt)) : t + 0.12 + lines.indexOf(tot) * step;
        CH.slam(tl, sm, at + 2 * CH.F, -7);
      }
    } else {
      CH.draw(tl, paper, t + 0.3, 0.3);
      const sm = el.querySelector(".rc-stampmark");
      if (sm) tl.set(sm, { rotation: -7 }, t);
    }
  },
});
