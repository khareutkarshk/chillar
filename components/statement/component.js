CH.define("statement", {
  build({ el, p, t, tl, rng }) {
    const tilt = (p.tilt !== null && p.tilt !== undefined && p.tilt !== "") ? +p.tilt : CH.tilt(rng);
    // body: string ("\n" = new line) or array of lines; width: chit/body width (leave room for a mascot)
    const body = Array.isArray(p.body) ? p.body.map(CH.rich).join("<br>") : String(p.body || "").split("\n").map(CH.rich).join("<br>");
    const w = p.width ? `width:${+p.width}px;max-width:${+p.width}px;` : "";
    el.innerHTML = `
      <div class="zone">
        <div class="st-title t-head" style="font-size:${+p.size}px">${CH.rich(p.title)}</div>
        ${body ? (p.paper
          ? `<div class="st-wrap torn-wrap st-b" style="${w}transform: rotate(${tilt.toFixed(2)}deg)"><div class="st-chit paper-torn t-body">${body}</div></div>`
          : `<div class="st-body t-body st-b" style="${w}">${body}</div>`) : ""}
      </div>`;
    // fit (default true): a word wider than the line shrinks the headline instead of breaking mid-word
    if (p.fit !== false) CH.fitHead(el.querySelector(".st-title"), +p.size, 0.55);
    CH.pop(tl, el.querySelector(".st-title"), t);
    const b = el.querySelector(".st-b");
    if (b) (p.paper ? CH.toss(tl, b, t + 4 * CH.F, tilt) : CH.pop(tl, b, t + 3 * CH.F));
    CH.markers(tl, el, t + (p.markerAt ?? 0.3));
  },
});
