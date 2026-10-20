CH.define("bar-chart", {
  build({ el, p, t, tl, rng }) {
    const bars = p.bars || [];
    const max = Math.max(...bars.map((b) => +b.value), 1);
    const H = 450, GAP = 28, PW = 870;
    const bw = (Math.min(420, (PW - GAP * (bars.length - 1)) / Math.max(1, bars.length)));
    const hts = bars.map((b) => Math.round(Math.max(+b.value ? 8 : (p.prefix ? 22 : 8), (+b.value / max) * H)));
    const fmt = (v) => (p.prefix || "") + CH.inr(v);
    // ballpoint hatching: seeded diagonal strokes so the strip reads as a shaded paper slip, not a box
    const hatch = (w, h) => {
      if (h < 30) return "";
      const step = 26, d = [];
      for (let k = -h + rng() * step; k < w; k += step * (0.8 + rng() * 0.4)) {
        const j = () => (rng() - 0.5) * 9;
        const x0 = Math.max(0, k), x1 = Math.min(w, k + h);
        if (x1 - x0 < 24) continue;
        const y0 = h - (x0 - k), y1 = h - (x1 - k);   // 45° stroke, bottom-left → top-right, inset 8 px
        d.push(`M${(x0 + 8 + j()).toFixed(1)} ${(y0 - 8 + j()).toFixed(1)} L${(x1 - 8 + j()).toFixed(1)} ${(y1 + 8 + j()).toFixed(1)}`);
      }
      return `<svg class="bar-hatch" viewBox="0 0 ${w.toFixed(0)} ${h}" width="${w.toFixed(0)}" height="${h}" preserveAspectRatio="none"><path d="${d.join(" ")}"/></svg>`;
    };
    // optional pen bracket on the difference: drawn on the taller bar, from its top down to the shorter bar's level
    let bi = -1, si = -1;
    if (p.bracket && bars.length >= 2) {
      const pick = Array.isArray(p.bracketBars) && p.bracketBars.length === 2 ? p.bracketBars.map(Number).filter((i) => i >= 0 && i < bars.length) : [];
      const pair = pick.length === 2 && pick[0] !== pick[1] ? pick : bars.map((_, i) => i).sort((a, b) => +bars[b].value - +bars[a].value).slice(0, 2);
      [bi, si] = +bars[pair[0]].value >= +bars[pair[1]].value ? pair : [pair[1], pair[0]];
    }
    const bracketHtml = () => {
      const dh = hts[bi] - hts[si], h = Math.max(40, dh), w = 46, r = () => (rng() - 0.5) * 4;
      const path = `M${w + r()} 4 C${w * 0.35} 4 ${w * 0.45 + r()} ${h * 0.2} ${w * 0.4} ${h * 0.42} C${w * 0.38} ${h * 0.48} ${w * 0.15} ${h * 0.5} 4 ${h * 0.5} `
        + `C${w * 0.15} ${h * 0.5} ${w * 0.38} ${h * 0.52} ${w * 0.4} ${h * 0.58} C${w * 0.45 + r()} ${h * 0.8} ${w * 0.35} ${h - 4} ${w + r()} ${h - 4}`;
      const label = typeof p.bracket === "string" ? p.bracket : "+" + fmt(+bars[bi].value - +bars[si].value);
      return `<div class="bar-brk" style="height:${h}px">
          <svg class="scrib" viewBox="-8 -8 ${w + 16} ${h + 16}" width="${w + 16}" height="${h + 16}" style="left:-8px; top:-8px"><path d="${path}" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1" style="stroke-width:7px"/></svg>
          <div class="bar-brk-lab num">${CH.esc(label)}</div></div>`;
    };
    el.innerHTML = `
      <div class="zone">
        ${p.title ? `<div class="bar-title t-head">${CH.rich(p.title)}</div>` : ""}
        <div class="bar-plot">
          ${bars.map((b, i) => { const v = String(b.display ?? fmt(+b.value)), hi = i === +p.highlight; return `
            <div class="bar-col">
              <div class="bar-val num">${CH.esc(v)}${hi ? CH.scribble("circle", { x: -30, y: -8, w: v.length * 42 + 56, h: 92, rng }) : ""}</div>
              <div class="bar paper-obj ${hi ? "hi" : ""} ${+b.value ? "" : "zero"}" style="height:${hts[i]}px">${hatch(bw, hts[i])}${i === bi ? bracketHtml() : ""}</div>
              <div class="bar-lab t-body">${CH.esc(b.label)}</div>
            </div>`; }).join("")}
        </div>
        ${p.caption ? `<div class="bar-cap t-body">${CH.esc(p.caption)}</div>` : ""}
      </div>`;
    const title = el.querySelector(".bar-title");
    if (title) CH.pop(tl, title, t);
    let last = t;
    [...el.querySelectorAll(".bar-col")].forEach((c, i) => {
      const at = t + 0.2 + i * (+p.stagger);
      tl.fromTo(c.querySelector(".bar"), { scaleY: 0 }, { scaleY: 1, duration: 7 * CH.F, ease: "power3.out", transformOrigin: "50% 100%" }, at);
      tl.fromTo(c.querySelector(".bar-val"), { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 4 * CH.F }, at + 5 * CH.F);
      last = at + 9 * CH.F;
    });
    const cap = el.querySelector(".bar-cap");
    if (cap) CH.pop(tl, cap, last);
    const hi = el.querySelectorAll(".bar-col")[+p.highlight];
    if (hi) CH.draw(tl, hi.querySelector(".bar-val"), last + 0.1, 0.3);
    const brk = el.querySelector(".bar-brk");
    if (brk) {
      const at = last + (hi ? 0.45 : 0.1);
      CH.draw(tl, brk, at, 0.3);
      tl.fromTo(brk.querySelector(".bar-brk-lab"), { opacity: 0 }, { opacity: 1, duration: 2 * CH.F, ease: "steps(2)" }, at + 0.2);
    }
  },
});
