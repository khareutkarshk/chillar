CH.define("calendar-flip", {
  build({ el, p, t, tl, rng }) {
    const pages = p.pages || [];
    const width = Math.min(860, Math.max(400, +p.width || 600));
    const sc = width / 600, auto = +p.height < 0;
    const height = auto ? 0 : Math.min(760, Math.max(360, +p.height || 620));
    const yearSize = Math.min(230, Math.max(120, +p.yearSize || 230));
    const details = p.details || [];
    const tilt = CH.tilt(rng, 1.8);
    const split = (s) => { const m = String(s).match(/^(\D*?)\s*(\d+)$/); return m ? [m[1] || " ", m[2]] : [s, ""]; };
    el.innerHTML = `
      <div class="zone">
        ${p.label ? `<div class="cf-label t-head">${CH.rich(p.label)}</div>` : ""}
        <div class="cf-cal${auto ? " auto" : ""}" style="width:${width}px;${auto ? "" : `height:${height}px;`}--cf-s:${sc.toFixed(3)};transform: rotate(${tilt.toFixed(2)}deg)">
          <div class="cf-rings"><span></span><span></span></div>
          <div class="cf-stack${auto ? " auto" : ""}" data-layout-allow-overlap>
            ${pages.map((pg, i) => { const [a, b] = split(pg); return `
              <div class="cf-page paper-obj" style="z-index:${pages.length - i}">
                <div class="cf-band t-head">${CH.esc(a)}</div>
                ${b ? `<div class="cf-big t-num" style="font-size:${yearSize}px">${CH.esc(b)}</div>` : ""}
                ${details[i] ? `<div class="cf-body">${CH.esc(details[i])}</div>` : ""}
              </div>`; }).join("")}
          </div>
        </div>
      </div>`;
    const lab = el.querySelector(".cf-label");
    if (lab) { CH.pop(tl, lab, t); CH.markers(tl, lab, t + 0.3); }
    CH.toss(tl, el.querySelector(".cf-cal"), t, tilt);   // on the cut frame, never an empty field
    const pgs = [...el.querySelectorAll(".cf-page")];
    pgs.forEach((pg, i) => { if (i > 0) tl.set(pg, { opacity: 0 }, 0); });   // pages beneath stay hidden until revealed
    pgs.slice(0, -1).forEach((pg, i) => {
      const at = t + 0.25 + i * (+p.flip);
      tl.set(pgs[i + 1], { opacity: 1 }, at + 2 * CH.F);   // revealed once the top page has faded
      tl.fromTo(pg, { rotationX: 0 }, { rotationX: -100, duration: 4 * CH.F, ease: "power2.in", transformOrigin: "50% 0%" }, at);
      tl.fromTo(pg, { opacity: 1 }, { opacity: 0, duration: 2 * CH.F, ease: "none" }, at);
    });
  },
});
