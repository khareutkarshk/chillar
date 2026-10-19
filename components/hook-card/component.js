CH.define("hook-card", {
  build({ el, p, t, d, tl, id, rng }) {
    const tilt = CH.tilt(rng, 2.4);
    const stakes = p.stakes || [];
    el.innerHTML = `
      <div class="zone">
        <div class="hk-q t-head" style="font-size:${+p.size}px">${CH.rich(p.question)}</div>
        <div class="hk-row">
          <div class="hk-wrap torn-wrap" style="transform: rotate(${tilt.toFixed(2)}deg)"><div class="hk-stub paper-torn t-print">
            ${stakes.map((s, i) => `<div class="hk-line"><span>${CH.esc(s.label)}</span><span class="hk-amt num print">${CH.esc(s.amount)}${
              p.circle && i === stakes.length - 1 ? CH.scribble("circle", { x: -26, y: -8, w: 30 * String(s.amount).length + 52, h: 78, rng }) : ""}</span></div>`).join("")}
          </div></div>
          ${p.mascot ? `<div class="hk-mascot">${CH.mascot(p.mascot, id + "-m", 330)}</div>` : ""}
        </div>
      </div>`;
    // frame 1 = final layout. Motion starts after it.
    CH.markers(tl, el, t + 0.2);
    CH.draw(tl, el.querySelector(".hk-stub"), t + 0.35, 0.3);
    CH.mascotAnim(tl, el.querySelector(".hk-mascot svg"), "blink", t + 0.2, d - 0.2);
  },
});
