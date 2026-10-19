CH.define("mascot-reaction", {
  build({ el, p, t, d, tl, id, rng }) {
    const size = +p.size, h = size * 1.1;
    const left = +p.x - size / 2, top = +p.y - h;
    const bubbleLeft = p.bubbleSide === "right";
    const tilt = CH.tilt(rng, 2);
    el.innerHTML = `
      <div class="mr-wrap" style="left:${left}px; top:${top}px; width:${size}px; height:${h}px">
        ${p.bubble ? `<div class="mr-bubble t-body ${bubbleLeft ? "r" : "l"}">${CH.rich(p.bubble)}</div>` : ""}
        <div class="mr-body">${CH.mascot(p.expr, id + "-m", size)}${p.ring ? `
          <svg class="mr-ring" viewBox="0 0 400 440" width="${size}" height="${h}">
            <defs><path id="${id}-arc" d="M50 190 A150 150 0 0 0 350 190"/></defs>
            <circle class="mr-ring-o" cx="200" cy="190" r="186"/>
            <path class="mr-ring-band" d="M50 190 A150 150 0 0 0 350 190" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1"/>
            <text class="mr-ring-t"><textPath href="#${id}-arc" startOffset="50%" text-anchor="middle" dominant-baseline="middle">${CH.esc(p.ring)}</textPath></text>
          </svg>` : ""}</div>
      </div>`;
    const body = el.querySelector(".mr-body");
    tl.fromTo(body, { y: 180, opacity: 0, rotation: -6 }, { y: 0, opacity: 1, rotation: 0, duration: 8 * CH.F, ease: "back.out(1.8)" }, t);
    const b = el.querySelector(".mr-bubble");
    if (b) CH.pop(tl, b, t + 6 * CH.F, { from: 0.7, y: 20, rotTo: tilt, rot: tilt });
    CH.mascotAnim(tl, el.querySelector("svg"), p.anim, t + 9 * CH.F, d - 9 * CH.F);
    const ring = el.querySelector(".mr-ring");
    if (ring) {
      tl.fromTo(ring.querySelector(".mr-ring-band"), { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 8 * CH.F, ease: "power2.out" }, t + 8 * CH.F);
      tl.fromTo(ring.querySelector(".mr-ring-t"), { opacity: 0 }, { opacity: 1, duration: 3 * CH.F, ease: "none" }, t + 14 * CH.F);
    }
  },
});
