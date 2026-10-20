/* Two modes:
 *   roll  (default)  digits roll up like an odometer to `value`
 *   count (`from` set) one legible tabular number counts from `from` to `value` — every frame is a
 *                      real, correctly grouped amount (₹1,00,000 → ₹86,468), held at `from` until rollStart */
CH.define("odometer-number", {
  build({ el, p, t, tl, rng }) {
    const opt = { prefix: p.prefix, suffix: p.suffix, decimals: p.decimals ?? undefined };
    const fmt = (v) => (p.prefix || "") + CH.inr(v, opt) + (p.suffix || "");
    const count = p.from !== null && p.from !== undefined && p.from !== "";
    const start = count ? +p.from : +p.value;
    el.innerHTML = `
      <div class="zone">
        ${p.label ? `<div class="od-label t-body">${CH.rich(p.label)}</div>` : ""}
        <div class="od-numwrap">
          <div class="od-num tone-${CH.esc(p.tone)}" style="font-size:${+p.size}px">${count
            ? `<span class="od-count t-num">${CH.esc(fmt(start))}</span>` : CH.odometer(+p.value, opt)}</div>
        </div>
        ${p.unit ? `<div class="od-unit t-head">${CH.esc(p.unit)}</div>` : ""}
        ${p.sub ? `<div class="od-sub t-body">${CH.rich(p.sub)}</div>` : ""}
      </div>`;
    // auto-fit: the widest state of the number stays inside the content zone (x 68–932)
    const num = el.querySelector(".od-num"), avail = 856;
    const widest = num.getBoundingClientRect().width;      // count mode measures `from` (the longer one)
    const fs = widest > avail ? Math.floor(+p.size * avail / widest) : +p.size;
    num.style.fontSize = fs + "px";
    const wrap = el.querySelector(".od-numwrap");
    if (p.underline) {
      const endW = count ? (() => { const c = el.querySelector(".od-count"), s = c.textContent; c.textContent = fmt(+p.value);
        const w = num.getBoundingClientRect().width; c.textContent = s; return w; })() : num.getBoundingClientRect().width;
      wrap.insertAdjacentHTML("beforeend", `<div class="od-underbox">${CH.scribble("underline", { x: 0, y: fs * 1.0, w: Math.min(avail - 20, endW), h: 22, rng, stroke: 9 })}</div>`);
    }
    // everything is on screen from the cut frame (snap-in, no stagger gap)
    [...el.querySelectorAll(".od-label, .od-numwrap, .od-unit" + (count ? "" : ", .od-sub"))].forEach((n) => CH.pop(tl, n, t));
    const rollAt = t + (+p.rollStart);
    let landed;
    if (count) {
      const c = el.querySelector(".od-count"), proxy = { v: start };
      const step = Math.pow(10, opt.decimals ?? 0);
      tl.fromTo(proxy, { v: start }, { v: +p.value, duration: +p.rollDuration, ease: "power3.out",
        onUpdate: () => { c.textContent = fmt(Math.round(proxy.v * step) / step); } }, rollAt);
      landed = rollAt + (+p.rollDuration);
    } else {
      const odo = el.querySelector(".odo");
      landed = CH.roll(tl, odo, rollAt, +p.rollDuration);
      // once landed, only the final digit of each strip stays painted: neighbours' glyph boxes poke
      // into the 1em window (sub-pixel strip offsets), which read as "₹012,456901901" instead of ₹1,500
      const digits = [...odo.dataset.target].filter((c) => /\d/.test(c));
      [...odo.querySelectorAll(".odo-strip")].forEach((strip, i) => {
        const keep = 11 + +digits[i];
        const others = [...strip.children].filter((_, k) => k !== keep);
        tl.set(others, { visibility: "hidden" }, landed);
      });
    }
    // count mode: the sub-line (the maths for the FINAL value) never sits under the start value
    if (count && el.querySelector(".od-sub")) CH.pop(tl, el.querySelector(".od-sub"), landed - 0.05);
    CH.draw(tl, wrap.querySelector(".od-underbox"), landed + 0.05, 0.3);
  },
});
