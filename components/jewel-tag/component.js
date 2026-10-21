// jewel-tag — gold bangle with etched HUID, matched by a pen line to the same code on a bill row.
CH.define("jewel-tag", {
  build({ el, p, t, tl, rng }) {
    const W = Math.min(880, +p.width || 860), D = Math.round(W * 0.44), plateTop = D - 34, billTop = D + 80;
    const huid = String(p.huid || "AB12CD").toUpperCase();
    const amt = CH.inr(+p.amount || 0);
    const t1 = CH.tilt(rng, 2), t2 = CH.tilt(rng, 2);
    const codeW = huid.length * 25 + 8;                       // mono 40 px ≈ 24 px per char
    const cx = W - 40 - codeW / 2, cy = 26 + 44 + 8 + 72 + 26; // inside the bill, so marks tilt with it
    const plateCx = W / 2, plateCy = plateTop + 34 - billTop;
    el.innerHTML = `<div class="jt-wrap" style="left:${+p.x}px; top:${+p.y}px; width:${W}px; height:${billTop + 260}px">
      <div class="jt-ring" style="width:${D}px; height:${D}px; margin-left:${-D / 2}px; transform: rotate(${t1.toFixed(2)}deg)"></div>
      <div class="jt-plate" style="top:${plateTop}px">${CH.esc(huid)}</div>
      <div class="jt-bill" style="top:${billTop}px; transform: rotate(${t2.toFixed(2)}deg)">
        <div class="jt-head">Tax invoice</div>
        <div class="jt-row"><span>${CH.esc(p.item || "")}</span><b>₹${amt}</b></div>
        <div class="jt-row"><span>HUID</span><b>${CH.esc(huid)}</b></div>
        ${CH.scribble("circle", { x: cx - codeW / 2 - 14, y: cy - 30, w: codeW + 28, h: 60, rng, stroke: 6 })}
        <svg class="scrib jt-line" viewBox="0 0 ${W} 300" width="${W}" height="300" style="left:0; top:0">
          <path d="M${plateCx + 190} ${plateCy} C ${W + 30} ${plateCy - 20}, ${W + 30} ${cy - 150}, ${cx + 10} ${cy - 40}" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1" style="stroke-width:6px"/></svg></div></div>`;
    CH.toss(tl, el.querySelector(".jt-ring"), t, t1);
    CH.toss(tl, el.querySelector(".jt-bill"), t, t2);
    const mt = t + (p.matchAt == null ? 0.9 : +p.matchAt);
    const line = el.querySelector(".jt-line"), circ = el.querySelector(".scrib:not(.jt-line)");
    CH.draw(tl, { querySelectorAll: () => line.querySelectorAll("path") }, mt, 0.4);
    CH.draw(tl, { querySelectorAll: () => circ.querySelectorAll("path") }, mt + 0.4, 0.35);
  },
});
