CH.define("salary-slip", {
  build({ el, p, t, tl, rng }) {
    const rows = p.rows || [];
    const tilt = CH.tilt(rng, 1.6);
    const net = rows.reduce((s, r) => s + (r.type === "deduct" ? -1 : 1) * +r.amount, 0);
    const netW = ("₹" + CH.inr(net)).length * 58;
    el.innerHTML = `
      <div class="zone">
        <div class="ss-sheet paper-obj" style="transform: rotate(${tilt.toFixed(2)}deg)">
          <div class="ss-head ss-line"><span class="t-head">${CH.esc(p.title)}</span><span class="t-print">${CH.esc(p.month)}</span></div>
          ${rows.map((r) => `
            <div class="ss-row ss-line ${r.type === "deduct" ? "neg" : "pos"}">
              <span class="t-body">${CH.esc(r.label)}</span>
              <span class="num">${r.type === "deduct" ? "−" : "+"}₹${CH.inr(+r.amount)}</span>
            </div>`).join("")}
          <div class="ss-net ss-line"><span class="t-head">${CH.esc(p.netLabel)}</span>
            <span class="ss-netnum">${CH.odometer(net, { prefix: "₹" })}${CH.scribble("underline", { x: 0, y: 100, w: netW, h: 22, rng, stroke: 9 })}</span></div>
        </div>
      </div>`;
    CH.toss(tl, el.querySelector(".ss-sheet"), t, tilt, { frames: 6 });
    const lines = [...el.querySelectorAll(".ss-line")];
    const end = CH.print(tl, lines, t + 0.15, +p.step);
    const landed = CH.roll(tl, el.querySelector(".odo"), end, 0.8);
    CH.draw(tl, el.querySelector(".ss-netnum"), landed + 0.05, 0.3);
  },
});
