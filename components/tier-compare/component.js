CH.define("tier-compare", {
  build({ el, p, t, tl, rng }) {
    const tiers = p.tiers || [];
    const heights = [150, 300, 470];
    // column width: today's 276 px (3 tiers = the full ≈876 px content width); wide:true or width (px)
    // stretch the row to that width; a row that would leave the content zone always shrinks to fit
    const n = Math.max(1, tiers.length), gap = 24, full = 876;
    const rowW = +p.width > 0 ? Math.min(+p.width, 880) : (p.wide ? full : Math.min(full, n * 276 + (n - 1) * gap));
    const colW = Math.floor((rowW - (n - 1) * gap) / n);
    el.innerHTML = `
      <div class="zone">
        ${p.title ? `<div class="tc-title t-head">${CH.rich(p.title)}</div>` : ""}
        <div class="tc-row">
          ${tiers.map((tr, i) => { const last = i === tiers.length - 1, r = String(tr.result || ""); return `
            <div class="tc-col" style="width:${colW}px">
              <div class="tc-res num ${last ? "big" : ""}">${CH.esc(r)}${last && r ? CH.scribble("circle", { x: -20, y: -6, w: r.length * 56 + 30, h: 112, rng }) : ""}</div>
              <div class="tc-bar" style="width:${colW}px;height:${heights[Math.min(i, 2)]}px"><span class="tc-amt num">${CH.esc(tr.amount)}</span></div>
            </div>`; }).join("")}
        </div>
      </div>`;
    // narrow columns (wide/width with many tiers): an amount or result never spills past its column
    const shrink = (node, maxW) => { let f = parseFloat(getComputedStyle(node).fontSize); const min = f * 0.6;
      while (node.scrollWidth > maxW && f > min) { f = Math.max(min, f * 0.94); node.style.fontSize = `${Math.round(f)}px`; } };
    const aS = +p.amtSize > 0 ? +p.amtSize : 0, rS = +p.resSize > 0 ? +p.resSize : 0;
    if (aS) el.querySelectorAll(".tc-amt").forEach((a) => { a.style.fontSize = `${aS}px`; a.style.whiteSpace = "normal"; a.style.lineHeight = "1.02"; });
    if (rS) el.querySelectorAll(".tc-res").forEach((r) => { r.style.fontSize = `${rS}px`; });
    el.querySelectorAll(".tc-amt").forEach((a) => { if (!aS) shrink(a, colW - 34); });
    el.querySelectorAll(".tc-res").forEach((r) => shrink(r, colW));
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
