CH.define("passbook-page", {
  build({ el, p, t, tl, rng }) {
    const tilt = CH.tilt(rng, 1.4);
    let bal = +p.opening || 0;
    const rows = (p.rows || []).map((r) => {
      bal += (r.type === "dr" ? -1 : 1) * +r.amount;
      return { ...r, bal };
    });
    const last = rows.length - 1;
    const balTxt = (b) => CH.inr(b);
    const grow = !p.printed && p.grow !== false;
    const body = (live) => `
          <div class="pb-stitch"></div>
          <div class="pb-row pb-headrow"><span>Date</span><span>Particulars</span><span class="pb-r">Amount</span><span class="pb-r">Balance</span></div>
          <div class="pb-row pb-line"><span></span><span class="pb-text">B/F</span><span></span><span class="pb-r">${balTxt(+p.opening || 0)}</span></div>
          ${rows.map((r, i) => `
            <div class="pb-row pb-line ${r.type === "dr" ? "dr" : "cr"}">
              <span>${CH.esc(r.date)}</span><span class="pb-text">${CH.esc(r.text)}</span>
              <span class="pb-r pb-amt">${r.type === "dr" ? "−" : "+"}${CH.inr(+r.amount)}</span>
              <span class="pb-r pb-bal">${balTxt(r.bal)}${i === last && p.circleBalance
                ? CH.scribble("circle", { x: 214 - balTxt(r.bal).length * 23 - 34, y: 6, w: balTxt(r.bal).length * 23 + 48, h: 70, rng }) : ""}</span>
            </div>`).join("")}`;
    const fs = `--pb-fs: ${+p.size || 38}px`;
    // grow (default unless printed:true): an invisible ghost page reserves the final layout; the live paper lengthens as each line prints
    el.innerHTML = grow
      ? `<div class="zone"><div class="pb-stack">
          <div class="pb-page pb-ghost t-print" aria-hidden="true" style="${fs}">${body(false)}</div>
          <div class="pb-page pb-live paper-obj t-print" style="transform: rotate(${tilt.toFixed(2)}deg); ${fs}">${body(true)}</div></div></div>`
      : `<div class="zone"><div class="pb-page paper-obj t-print" style="transform: rotate(${tilt.toFixed(2)}deg); ${fs}">${body(true)}</div></div>`;
    const page = el.querySelector(".pb-page.paper-obj");
    if (!p.printed) {
      CH.toss(tl, page, t, tilt, { frames: 6 });
      const lines = [...el.querySelectorAll(".pb-page.paper-obj .pb-line")];
      const end = CH.print(tl, lines, t + 0.25, +p.step);
      if (grow) lines.forEach((ln, i) => { if (i > 1) tl.fromTo(ln, { height: 0 }, { height: 85, duration: 2 * CH.F, ease: "steps(2)" }, t + 0.25 + i * (+p.step)); });
      CH.draw(tl, page, end + 0.05, 0.3);
    } else {
      CH.draw(tl, page, t + 0.3, 0.3);
    }
  },
});
