// steel-dabba — a steel tiffin with a haldi price sticker (optional struck-out old price).
CH.define("steel-dabba", {
  build({ el, p, t, tl, rng }) {
    const W = Math.min(880, +p.width || 640), n = Math.max(2, Math.min(4, +p.tiers || 3));
    const lidH = Math.round(W * 0.2), tierH = Math.round(W * 0.26), handleTop = 0, knobH = 40;
    const top0 = Math.round(W * 0.3), H = top0 + lidH + n * tierH + 60;
    const tilt = CH.tilt(rng, 1.5);
    let tiers = "";
    for (let i = 0; i < n; i++) tiers += `<div class="sd-tier" style="top:${top0 + lidH - 4 + i * (tierH - 4)}px; height:${tierH}px"></div>`;
    const stickerTop = top0 + lidH + Math.round(tierH * 0.45);
    const old = +p.oldPrice ? `<span class="sd-old">₹${CH.inr(+p.oldPrice)}${CH.scribble("strike", { x: -6, y: 0, w: 150, h: 48, rng, stroke: 6 })}</span>` : "";
    el.innerHTML = `<div class="sd-wrap" style="left:${+p.x}px; top:${+p.y}px; width:${W}px; height:${H}px">
      <div class="sd-shadow" style="top:${H - 40}px"></div>
      <div class="sd-body" style="position:absolute; left:0; top:0; width:100%; height:${H}px; transform: rotate(${tilt.toFixed(2)}deg)">
        <div class="sd-handle" style="top:${handleTop + 30}px; height:${top0 + 40}px"></div>
        <div class="sd-knob" style="top:${top0 - knobH + 6}px"></div>
        ${tiers}
        <div class="sd-tier sd-lid" style="top:${top0}px; height:${lidH}px"></div>
        <div class="sd-sticker" style="top:${stickerTop}px">${p.label ? `<div class="sd-lab">${CH.esc(p.label)}</div>` : ""}${old ? `<div>${old}</div>` : ""}<span class="sd-price">₹${CH.inr(+p.price || 0)}</span></div></div></div>`;
    const body = el.querySelector(".sd-body"), st = el.querySelector(".sd-sticker");
    CH.toss(tl, body, t, tilt);
    tl.fromTo(st, { opacity: 0, scale: 1.25 }, { opacity: 1, scale: 1, duration: 0.2, ease: "power3.out" }, t + 0.4);
    if (+p.oldPrice) CH.draw(tl, st, t + 0.7, 0.3);
  },
});
