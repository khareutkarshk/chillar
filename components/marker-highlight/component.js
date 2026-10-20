CH.define("marker-highlight", {
  build({ el, p, t, tl, rng }) {
    const c = p.align === "center";
    const paper = !!p.paper;
    const tilt = paper ? CH.tilt(rng, 1.6) : 0;
    const inner = `
        <div class="mh-text t-head" style="font-size:${+p.size}px">${CH.rich(p.text)}</div>
        ${p.sub ? `<div class="mh-sub t-body">${CH.rich(p.sub)}</div>` : ""}`;
    el.innerHTML = `
      <div class="zone ${c ? "center" : ""}" style="text-align:${c ? "center" : "left"}">
        ${paper ? `<div class="mh-scrap paper-obj" style="transform: rotate(${tilt.toFixed(2)}deg)">${inner}</div>` : inner}
      </div>`;
    // fit: never break inside a word — shrink the headline until its longest word fits the width.
    const head = el.querySelector(".mh-text");
    if (p.fit !== false) CH.fitHead(head, +p.size, 0.55);
    if (paper) {
      // paper: the scrap carrying the quote is tossed onto the field on the cut frame; the sub follows
      CH.toss(tl, el.querySelector(".mh-scrap"), t, tilt);
      const sub = el.querySelector(".mh-sub");
      if (sub) CH.pop(tl, sub, t + 4 * CH.F, { y: 14, from: 1 });
    } else {
      [...el.querySelectorAll(".mh-text, .mh-sub")].forEach((n, i) => CH.pop(tl, n, t + i * 4 * CH.F));
    }
    CH.markers(tl, el, t + (+p.markerAt));
  },
});
