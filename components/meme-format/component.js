CH.define("meme-format", {
  build({ el, p, t, tl, id, rng }) {
    const panels = (p.panels || []).slice(0, 3);
    const defaults = {
      "two-panel": ["Nah", "Haan"], "expectation-reality": ["Expectation", "Reality"], "nobody-me": ["Nobody:", "Me:"],
    }[p.format] || [];
    const tilts = panels.map((_, i) => CH.tilt(rng, 2.2) * (i % 2 ? -1 : 1));
    el.innerHTML = `
      <div class="zone${panels.length > 2 ? " n3" : ""}">
        ${panels.map((pn, i) => `
          <div class="mf-panel paper-obj fmt-${CH.esc(p.format)} i${i}" style="transform: rotate(${tilts[i].toFixed(2)}deg)">
            <div class="mf-pic">${pn.expr ? CH.mascot(pn.expr, `${id}-p${i}`, 250) : ""}</div>
            <div class="mf-copy">
              <div class="mf-label t-head">${CH.esc(pn.label || defaults[i] || "")}</div>
              <div class="mf-text t-body"${p.textSize ? ` style="font-size:${+p.textSize}px"` : ""}>${CH.rich(pn.text)}</div>
            </div>
          </div>`).join("")}
      </div>`;
    [...el.querySelectorAll(".mf-panel")].forEach((pn, i) => CH.toss(tl, pn, t + i * (+p.reveal), tilts[i]));
    CH.markers(tl, el, t + panels.length * (+p.reveal));
  },
});
