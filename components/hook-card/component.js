CH.define("hook-card", {
  build({ el, p, t, d, tl, id, rng }) {
    const tilt = CH.tilt(rng, 2.4);
    const stakes = p.stakes || [];
    el.innerHTML = `
      <div class="zone">
        <div class="hk-q t-head" style="font-size:${+p.size}px">${CH.rich(p.question)}</div>
        <div class="hk-row${p.wide ? " wide" : ""}">
          <div class="hk-wrap torn-wrap" style="transform: rotate(${tilt.toFixed(2)}deg)"><div class="hk-stub paper-torn t-print">
            ${stakes.map((s, i) => `<div class="hk-line"><span>${CH.esc(s.label)}</span><span class="hk-amt num print">${CH.esc(s.amount)}${
              p.circle && i === stakes.length - 1 ? CH.scribble("circle", { x: -26, y: -8, w: (p.wide ? 42 : 30) * String(s.amount).length + 52, h: p.wide ? 104 : 78, rng }) : ""}</span></div>`).join("")}
          </div></div>
          ${p.mascot ? `<div class="hk-mascot">${CH.mascot(p.mascot, id + "-m", 330)}</div>` : ""}
        </div>
      </div>`;
    // frame 1 = final layout. Motion starts after it.
    // frame 1 is fully drawn: the marker is already on the key word at t=0
    el.querySelectorAll(".marker").forEach((m) => tl.set(m, { "--marker": 1 }, t));
    CH.draw(tl, el.querySelector(".hk-stub"), t + 0.35, 0.3);
    CH.mascotAnim(tl, el.querySelector(".hk-mascot svg"), "blink", t + 0.2, d - 0.2);
  },
});
