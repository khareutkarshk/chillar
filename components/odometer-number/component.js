CH.define("odometer-number", {
  build({ el, p, t, tl, rng }) {
    const odo = CH.odometer(+p.value, { prefix: p.prefix, suffix: p.suffix, decimals: p.decimals ?? undefined });
    const chars = ((p.prefix || "") + CH.inr(+p.value, { decimals: p.decimals ?? undefined }) + (p.suffix || "")).length;
    const w = Math.min(820, chars * +p.size * 0.54);
    el.innerHTML = `
      <div class="zone">
        ${p.label ? `<div class="od-label t-body">${CH.rich(p.label)}</div>` : ""}
        <div class="od-numwrap">
          <div class="od-num tone-${CH.esc(p.tone)}" style="font-size:${+p.size}px">${odo}</div>
          ${p.underline ? CH.scribble("underline", { x: 0, y: +p.size * 1.0, w, h: 22, rng, stroke: 9 }) : ""}
        </div>
        ${p.unit ? `<div class="od-unit t-head">${CH.esc(p.unit)}</div>` : ""}
        ${p.sub ? `<div class="od-sub t-body">${CH.rich(p.sub)}</div>` : ""}
      </div>`;
    const parts = [...el.querySelectorAll(".od-label, .od-numwrap, .od-unit, .od-sub")];
    parts.forEach((n, i) => CH.pop(tl, n, t + i * 3 * CH.F));
    const landed = CH.roll(tl, el.querySelector(".odo"), t + (+p.rollStart), +p.rollDuration);
    CH.draw(tl, el.querySelector(".od-numwrap"), landed + 0.05, 0.3);
  },
});
