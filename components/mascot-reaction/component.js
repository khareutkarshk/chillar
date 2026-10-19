CH.define("mascot-reaction", {
  build({ el, p, t, d, tl, id, rng }) {
    const size = +p.size, h = size * 1.1;
    const left = +p.x - size / 2, top = +p.y - h;
    const bubbleLeft = p.bubbleSide === "right";
    const tilt = CH.tilt(rng, 2);
    el.innerHTML = `
      <div class="mr-wrap" style="left:${left}px; top:${top}px; width:${size}px; height:${h}px">
        ${p.bubble ? `<div class="mr-bubble t-body ${bubbleLeft ? "r" : "l"}">${CH.rich(p.bubble)}</div>` : ""}
        <div class="mr-body">${CH.mascot(p.expr, id + "-m", size)}</div>
      </div>`;
    const body = el.querySelector(".mr-body");
    tl.fromTo(body, { y: 180, opacity: 0, rotation: -6 }, { y: 0, opacity: 1, rotation: 0, duration: 8 * CH.F, ease: "back.out(1.8)" }, t);
    const b = el.querySelector(".mr-bubble");
    if (b) CH.pop(tl, b, t + 6 * CH.F, { from: 0.7, y: 20, rotTo: tilt, rot: tilt });
    CH.mascotAnim(tl, el.querySelector("svg"), p.anim, t + 9 * CH.F, d - 9 * CH.F);
  },
});
