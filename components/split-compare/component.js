CH.define("split-compare", {
  build({ el, p, t, tl, rng }) {
    const L = p.left || {}, R = p.right || {};
    const t1 = CH.tilt(rng, 2.4), t2 = -Math.sign(t1) * Math.abs(CH.tilt(rng, 1.6));
    const lw = Math.min(740, String(L.text || "").length * 31);
    el.innerHTML = `
      <div class="zone">
        <div class="sc-chit sc-myth paper-obj" style="transform: rotate(${t1.toFixed(2)}deg)">
          <div class="sc-word t-head">${CH.esc(L.title)}</div>
          <div class="sc-text t-body">${CH.rich(L.text)}${CH.scribble("strike", { x: -10, y: 0, w: lw + 20, h: 72, rng, stroke: 7 })}</div>
        </div>
        <div class="sc-chit sc-math paper-obj" style="transform: rotate(${t2.toFixed(2)}deg)">
          <div class="sc-word t-head">${CH.esc(R.title)}</div>
          <div class="sc-text t-body">${CH.rich(R.text)}</div>
        </div>
      </div>`;
    CH.toss(tl, el.querySelector(".sc-myth"), t, t1);
    CH.draw(tl, el.querySelector(".sc-myth"), t + (+p.strikeAt), 0.22);
    CH.toss(tl, el.querySelector(".sc-math"), t + (+p.revealAt), t2, { frames: 5, y: 140, twist: 8 });
    CH.markers(tl, el.querySelector(".sc-math"), t + (+p.revealAt) + 0.3);
  },
});
