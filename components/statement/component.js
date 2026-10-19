CH.define("statement", {
  build({ el, p, t, tl, rng }) {
    const tilt = CH.tilt(rng);
    el.innerHTML = `
      <div class="zone">
        <div class="st-title t-head" style="font-size:${+p.size}px">${CH.rich(p.title)}</div>
        ${p.body ? (p.paper
          ? `<div class="st-wrap torn-wrap st-b" style="transform: rotate(${tilt.toFixed(2)}deg)"><div class="st-chit paper-torn t-body">${CH.rich(p.body)}</div></div>`
          : `<div class="st-body t-body st-b">${CH.rich(p.body)}</div>`) : ""}
      </div>`;
    CH.pop(tl, el.querySelector(".st-title"), t);
    const b = el.querySelector(".st-b");
    if (b) (p.paper ? CH.toss(tl, b, t + 4 * CH.F, tilt) : CH.pop(tl, b, t + 3 * CH.F));
    CH.markers(tl, el, t + 0.3);
  },
});
