CH.define("calendar-flip", {
  build({ el, p, t, tl, rng }) {
    const pages = p.pages || [];
    const tilt = CH.tilt(rng, 1.8);
    const split = (s) => { const m = String(s).match(/^(\D*?)\s*(\d+)$/); return m ? [m[1] || " ", m[2]] : [s, ""]; };
    el.innerHTML = `
      <div class="zone">
        ${p.label ? `<div class="cf-label t-head">${CH.rich(p.label)}</div>` : ""}
        <div class="cf-cal" style="transform: rotate(${tilt.toFixed(2)}deg)">
          <div class="cf-rings"><span></span><span></span></div>
          <div class="cf-stack">
            ${pages.map((pg, i) => { const [a, b] = split(pg); return `
              <div class="cf-page paper-obj" style="z-index:${pages.length - i}">
                <div class="cf-band t-head">${CH.esc(a)}</div>
                <div class="cf-big t-num">${CH.esc(b)}</div>
              </div>`; }).join("")}
          </div>
        </div>
      </div>`;
    const lab = el.querySelector(".cf-label");
    if (lab) { CH.pop(tl, lab, t); CH.markers(tl, lab, t + 0.3); }
    CH.toss(tl, el.querySelector(".cf-cal"), t + 2 * CH.F, tilt);
    [...el.querySelectorAll(".cf-page")].slice(0, -1).forEach((pg, i) => {
      tl.fromTo(pg, { rotationX: 0, opacity: 1 }, { rotationX: -100, opacity: 0, duration: 4 * CH.F, ease: "power2.in", transformOrigin: "50% 0%" }, t + 0.25 + i * (+p.flip));
    });
  },
});
