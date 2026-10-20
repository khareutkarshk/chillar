CH.define("outro", {
  build({ el, p, t, d, tl, id, rng }) {
    const tilt = CH.tilt(rng, 1.6);
    el.innerHTML = `
      <div class="zone">
        <div class="ou-receipt torn-wrap" style="transform: rotate(${tilt.toFixed(2)}deg)">
          <div class="ou-main paper-torn">
            <div class="ou-title t-print ou-line">CHILLAR RECEIPT</div>
            <div class="ou-rule ou-line"></div>
            <div class="ou-big t-body ou-line">${CH.rich(p.line1)}</div>
            <div class="ou-big t-body ou-line">${CH.rich(p.line2)}</div>
            <div class="ou-disc t-body ou-line">${CH.esc(p.disclaimer)}</div>
          </div>
          <div class="ou-perf"></div>
          <div class="ou-stub paper-torn">
            <div class="ou-follow t-head">${CH.esc(p.follow)}</div>
            <div class="ou-sub t-body t-sub">${CH.esc(p.sub)}</div>
          </div>
        </div>
        ${p.mascot ? `<div class="ou-mascot">${CH.mascot(p.mascot, id + "-m", 260)}</div>` : ""}
      </div>`;
    CH.toss(tl, el.querySelector(".ou-receipt"), t, tilt, { frames: 6 });
    // header + rule land with the paper; the body prints fast right after (a blank receipt on the cut read as an
    // empty frame in 3 reels), THEN the follow stub, then it tears
    const printed = CH.print(tl, [...el.querySelectorAll(".ou-line")].slice(2), t + 2 * CH.F, 0.12);
    tl.fromTo([el.querySelector(".ou-perf"), el.querySelector(".ou-stub")], { opacity: 0 }, { opacity: 1, duration: 2 * CH.F, ease: "none" }, Math.min(printed, t + (+p.tearAt) - 0.2));
    const tear = t + (+p.tearAt);
    tl.fromTo(el.querySelector(".ou-stub"), { y: 0, rotation: 0 }, { y: 80, rotation: -7, duration: 7 * CH.F, ease: "power3.out", transformOrigin: "100% 0%" }, tear);
    const m = el.querySelector(".ou-mascot");
    if (m) {
      tl.fromTo(m, { y: 260, opacity: 0 }, { y: 0, opacity: 1, duration: 8 * CH.F, ease: "back.out(1.8)" }, t + 2.1);
      CH.mascotAnim(tl, m.querySelector("svg"), "blink", t + 2.4, Math.max(0.5, d - 2.4));
    }
  },
});
