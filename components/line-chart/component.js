CH.define("line-chart", {
  build({ el, p, t, tl, rng }) {
    const W = 782, H = 500, P = +p.principal, r = +p.rate, n = +p.years;
    const tilt = CH.tilt(rng, 1.4);
    const comp = [...Array(n + 1)].map((_, y) => P * Math.pow(1 + r, y));
    const simp = [...Array(n + 1)].map((_, y) => P * (1 + r * y));
    const max = comp[n];
    const X = (y) => 14 + (y / n) * (W - 40), Y = (v) => H - 16 - (v / max) * (H - 56);
    const path = (arr) => arr.map((v, y) => `${y ? "L" : "M"}${X(y).toFixed(1)} ${Y(v).toFixed(1)}`).join(" ");
    const fmt = (v) => "₹" + CH.inr(Math.round(v / 1000) * 1000);
    const end = fmt(comp[n]);
    el.innerHTML = `
      <div class="zone">
        <div class="lc-title t-head">${CH.rich(p.title)}</div>
        <div class="lc-sheet paper-obj" style="transform: rotate(${tilt.toFixed(2)}deg)">
          <svg class="lc-svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
            <line x1="14" y1="${H - 16}" x2="${W - 26}" y2="${H - 16}" stroke="var(--ink)" stroke-width="5" opacity=".85" stroke-linecap="round"/>
            ${p.compare ? `<path class="lc-simple" d="${path(simp)}" pathLength="1" fill="none" stroke="var(--pencil)" stroke-width="9" stroke-linecap="round" stroke-dasharray="1 1"/>` : ""}
            <path class="lc-comp" d="${path(comp)}" pathLength="1" fill="none" stroke="var(--green)" stroke-width="14" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="1 1"/>
            <circle class="lc-dot" cx="${X(n)}" cy="${Y(max)}" r="17" fill="var(--green)"/>
          </svg>
          <div class="lc-end t-body"><span class="sw g"></span>${CH.esc(p.curveLabel)} <span class="num t-green">${CH.esc(end)}${
            CH.scribble("circle", { x: -22, y: -4, w: 34 * end.length + 30, h: 82, rng })}</span></div>
          ${p.compare ? `<div class="lc-end sub t-body"><span class="sw p"></span>${CH.esc(p.compareLabel)} <span class="num">${fmt(simp[n])}</span></div>` : ""}
        </div>
      </div>`;
    const dd = +p.drawDuration;
    CH.pop(tl, el.querySelector(".lc-title"), t);
    CH.toss(tl, el.querySelector(".lc-sheet"), t + 2 * CH.F, tilt);
    const s = el.querySelector(".lc-simple");
    if (s) tl.fromTo(s, { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: dd * 0.8, ease: "none" }, t + 0.25);
    tl.fromTo(el.querySelector(".lc-comp"), { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: dd, ease: "power2.in" }, t + 0.25);
    tl.fromTo(el.querySelector(".lc-dot"), { scale: 0, transformOrigin: "50% 50%" }, { scale: 1, duration: 4 * CH.F, ease: "power3.out" }, t + 0.25 + dd);
    tl.fromTo([...el.querySelectorAll(".lc-end")], { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 5 * CH.F, stagger: 0.12 }, t + 0.3 + dd);
    CH.draw(tl, el.querySelector(".lc-end"), t + 0.5 + dd, 0.32);
  },
});
