// phone-note — a plain notes list that grows name by name.
CH.define("phone-note", {
  build({ el, p, t, tl, rng }) {
    const tilt = CH.tilt(rng);
    const items = p.items || [];
    const rowsHtml = (live) => items.map((it) => {
      const w = Math.max(80, Math.min(700, 34 * String(it.text || "").length));
      return `<div class="pn-row"><div class="pn-line${it.strike ? " strike" : ""}"><span class="t-body">${CH.rich(it.text)}</span>${live && it.strike ? CH.scribble("strike", { x: 0, y: 42, w, h: 40, rng, stroke: 7 }) : ""}</div></div>`;
    }).join("");
    const total = p.total ? `<div class="pn-row pn-trow"><div class="pn-total">${CH.rich(p.total)}${CH.scribble("underline", { x: 0, y: 116, w: Math.min(700, 52 * String(p.total).length), h: 16, rng, stroke: 7 })}</div></div>` : "";
    const title = p.title ? `<div class="pn-title">${CH.rich(p.title)}</div>` : "";
    el.innerHTML = `<div class="zone"><div class="pn-sheet paper-obj" style="transform: rotate(${tilt.toFixed(2)}deg)">
      <div class="pn-in pn-ghost" aria-hidden="true">${title}${rowsHtml(false)}${total}</div>
      <div class="pn-in pn-live">${title}${rowsHtml(true)}${total}</div></div></div>`;
    if (p.grow) el.querySelector(".pn-ghost").style.display = "none";
    CH.toss(tl, el.querySelector(".pn-sheet"), t, tilt);
    const rows = [...el.querySelectorAll(".pn-live .pn-row")];
    rows.forEach((row, i) => {
      const isTot = row.classList.contains("pn-trow");
      const at = (isTot && +p.totalAt >= 0) ? t + +p.totalAt : t + 0.3 + i * (+p.stagger || 0.35);
      tl.fromTo(row, { height: 0 }, { height: "auto", duration: 5 * CH.F, ease: "power3.out" }, at - 2 * CH.F);
      tl.set(row, { overflow: "visible" }, at + 3 * CH.F);
      const tx = row.querySelector(".t-body, .pn-total");
      tl.fromTo(tx, { opacity: 0, x: -24 }, { opacity: 1, x: 0, duration: 5 * CH.F, ease: "power3.out" }, at);
      CH.draw(tl, row, at + 4 * CH.F, 0.22);
    });
  },
});
