CH.define("tier-compare", {
  build({ el, p, t, tl, rng }) {
    const tiers = p.tiers || [];
    const heights = [150, 300, 470];
    el.innerHTML = `
      <div class="zone">
        ${p.title ? `<div class="tc-title t-head">${CH.rich(p.title)}</div>` : ""}
        <div class="tc-row">
          ${tiers.map((tr, i) => { const last = i === tiers.length - 1, r = String(tr.result || ""); return `
            <div class="tc-col">
              <div class="tc-res num ${last ? "big" : ""}">${CH.esc(r)}${last && r ? CH.scribble("circle", { x: -20, y: -6, w: r.length * 56 + 30, h: 112, rng }) : ""}</div>
              <div class="tc-bar" style="height:${heights[Math.min(i, 2)]}px"><span class="tc-amt num">${CH.esc(tr.amount)}</span></div>
            </div>`; }).join("")}
        </div>
      </div>`;
    const title = el.querySelector(".tc-title");
    if (title) CH.pop(tl, title, t);
    // reveal "bars" (default): each column rises in turn, then its result.
    // reveal "results": all columns rise together on the cut (full width at once), results step in.
    const together = p.reveal === "results";
    [...el.querySelectorAll(".tc-col")].forEach((c, i) => {
      const at = t + 0.1 + i * (+p.stagger);
      tl.fromTo(c.querySelector(".tc-bar"), { scaleY: 0 }, { scaleY: 1, duration: 7 * CH.F, ease: "power3.out", transformOrigin: "50% 100%" }, together ? t : at);
      CH.pop(tl, c.querySelector(".tc-res"), at + 6 * CH.F, { from: 1.2, y: 0 });
      if (i === tiers.length - 1) CH.draw(tl, c.querySelector(".tc-res"), at + 0.5, 0.3);
    });
  },
});
