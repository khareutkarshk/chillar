CH.define("checklist", {
  build({ el, p, t, tl, rng }) {
    const tilt = CH.tilt(rng);
    const cross = (r) => `<svg class="scrib" viewBox="-24 -24 118 110" width="118" height="110" style="left:-24px; top:-24px">
      <path d="M${4 + r() * 6} ${4 + r() * 6} L${62 - r() * 4} ${58 - r() * 4}" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1" style="stroke-width:8px"/>
      <path d="M${64 - r() * 6} ${2 + r() * 6} L${2 + r() * 6} ${60 - r() * 4}" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1" style="stroke-width:8px"/></svg>`;
    el.innerHTML = `
      <div class="zone">
        ${p.title ? `<div class="cl-title t-head">${CH.rich(p.title)}</div>` : ""}
        <div class="cl-chit paper-obj" style="transform: rotate(${tilt.toFixed(2)}deg)">
          ${(p.items || []).map((it) => `
            <div class="cl-item ${it.ok ? "ok" : "no"}">
              <div class="cl-mark">${it.ok ? CH.scribble("tick", { w: 72, h: 62, rng, stroke: 9 }) : cross(rng)}</div>
              <div class="cl-text t-body">${CH.rich(it.text)}</div>
            </div>`).join("")}
        </div>
      </div>`;
    const title = el.querySelector(".cl-title");
    if (title) CH.pop(tl, title, t);
    CH.toss(tl, el.querySelector(".cl-chit"), t + 3 * CH.F, tilt);
    [...el.querySelectorAll(".cl-item")].forEach((it, i) => {
      const at = t + 0.3 + i * (+p.stagger);
      tl.fromTo(it.querySelector(".cl-text"), { opacity: 0, x: -24 }, { opacity: 1, x: 0, duration: 5 * CH.F, ease: "power3.out" }, at);
      CH.draw(tl, it.querySelector(".cl-mark"), at + 4 * CH.F, 0.22);
    });
  },
});
