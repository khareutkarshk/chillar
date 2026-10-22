CH.define("checklist", {
  build({ el, p, t, tl, rng }) {
    const tilt = CH.tilt(rng);
    const grow = p.grow !== false && p.grow !== 0 && p.grow !== "false";
    const cross = (r) => `<svg class="scrib" viewBox="-24 -24 118 110" width="118" height="110" style="left:-24px; top:-24px">
      <path d="M${4 + r() * 6} ${4 + r() * 6} L${62 - r() * 4} ${58 - r() * 4}" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1" style="stroke-width:8px"/>
      <path d="M${64 - r() * 6} ${2 + r() * 6} L${2 + r() * 6} ${60 - r() * 4}" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1" style="stroke-width:8px"/></svg>`;
    const rows = (p.items || []).map((it) => `
            <div class="cl-row"><div class="cl-item ${it.ok ? "ok" : "no"}">
              <div class="cl-mark">${it.ok ? CH.scribble("tick", { w: 72, h: 62, rng, stroke: 9 }) : cross(rng)}</div>
              <div class="cl-text t-body">${CH.rich(it.text)}</div>
            </div></div>`).join("");
    // grow: an invisible full-length ghost reserves the final size, so the layout never shifts while the chit lengthens
    el.innerHTML = `
      <div class="zone">
        ${p.title ? `<div class="cl-title t-head">${CH.rich(p.title)}</div>` : ""}
        <div class="cl-stack${grow ? " grow" : ""}">
          ${grow ? `<div class="cl-chit cl-ghost" aria-hidden="true">${rows}</div>` : ""}
          <div class="cl-chit paper-obj" style="transform: rotate(${tilt.toFixed(2)}deg)">${rows}</div>
        </div>
      </div>`;
    const title = el.querySelector(".cl-title");
    if (title) CH.pop(tl, title, t);
    CH.toss(tl, el.querySelector(".cl-chit.paper-obj"), t + 3 * CH.F, tilt);
    [...el.querySelectorAll(".cl-chit.paper-obj .cl-row")].forEach((row, i) => {
      const at = t + 0.3 + i * (+p.stagger);
      // the first row is on the chit when it lands; each later row opens more paper just before it is written
      if (grow && i > 0) tl.fromTo(row, { height: 0 }, { height: "auto", duration: 5 * CH.F, ease: "power3.out" }, at - 2 * CH.F);
      // once open, let the pen marks spill past the row edge (no clipped crosses/ticks)
      if (grow && i > 0) tl.set(row, { overflow: "visible" }, at + 3 * CH.F);
      if (grow && i === 0) { tl.fromTo(row.querySelector(".cl-text"), { opacity: 0, x: -24 }, { opacity: 1, x: 0, duration: 5 * CH.F, ease: "power3.out" }, t + 3 * CH.F); CH.draw(tl, row.querySelector(".cl-mark"), t + 7 * CH.F, 0.22); return; }
      tl.fromTo(row.querySelector(".cl-text"), { opacity: 0, x: -24 }, { opacity: 1, x: 0, duration: 5 * CH.F, ease: "power3.out" }, at);
      CH.draw(tl, row.querySelector(".cl-mark"), at + 4 * CH.F, 0.22);
    });
  },
});
