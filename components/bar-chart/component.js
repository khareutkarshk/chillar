CH.define("bar-chart", {
  build({ el, p, t, tl, rng }) {
    const bars = p.bars || [];
    const max = Math.max(...bars.map((b) => +b.value), 1);
    const H = 450;
    el.innerHTML = `
      <div class="zone">
        ${p.title ? `<div class="bar-title t-head">${CH.rich(p.title)}</div>` : ""}
        <div class="bar-plot">
          ${bars.map((b, i) => { const v = String(b.display ?? ((p.prefix || "") + CH.inr(+b.value))), hi = i === +p.highlight; return `
            <div class="bar-col">
              <div class="bar-val num">${CH.esc(v)}${hi ? CH.scribble("circle", { x: -30, y: -8, w: v.length * 42 + 56, h: 92, rng }) : ""}</div>
              <div class="bar ${hi ? "hi" : ""} ${+b.value ? "" : "zero"}" style="height:${Math.max(+b.value ? 8 : (p.prefix ? 22 : 8), (+b.value / max) * H).toFixed(0)}px"></div>
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
  },
});
