/* Real cuts, not cards. Timing is relative to the cut (p.cut, absolute seconds):
 *   whip  out: x→-760 + skew over 4f before the cut · in: x 760→0 over 5f after it
 *   zoom  out: scale→1.3 over 4f before · in: scale .86→1 over 6f after
 *   wipe  next field slides up over 5f, ending on the cut (the new shot is under it)
 *   page  blank passbook page swings shut over 6f, swings away over 7f
 * The scene clips keep their own visibility windows; this only moves them. */
CH.define("transition", {
  build({ el, p, t, d, tl }) {
    const F = CH.F, cut = +p.cut || t;
    const out = p.from && document.getElementById(p.from);
    const inn = p.to && document.getElementById(p.to);
    if (p.style === "whip") {
      if (out) tl.fromTo(out, { x: 0, skewX: 0 }, { x: -760, skewX: 10, duration: 4 * F, ease: "power2.in", immediateRender: false }, cut - 4 * F);
      if (inn) tl.fromTo(inn, { x: 760, skewX: -10 }, { x: 0, skewX: 0, duration: 5 * F, ease: "power3.out", immediateRender: false }, cut);
    } else if (p.style === "zoom") {
      if (out) tl.fromTo(out, { scale: 1 }, { scale: 1.3, duration: 4 * F, ease: "power2.in", transformOrigin: "50% 36%", immediateRender: false }, cut - 4 * F);
      if (inn) tl.fromTo(inn, { scale: 0.86 }, { scale: 1, duration: 6 * F, ease: "power3.out", transformOrigin: "50% 36%", immediateRender: false }, cut);
    } else if (p.style === "wipe") {
      el.style.setProperty("--wipe-field", `var(--${p.field || "bone"})`);
      el.innerHTML = `<div class="tr-wipe"></div>`;
      tl.fromTo(el.querySelector(".tr-wipe"), { yPercent: 100 }, { yPercent: 0, duration: 5 * F, ease: "power3.in" }, cut - 5 * F);
    } else if (p.style === "page") {
      el.innerHTML = `<div class="tr-persp"><div class="tr-page"></div></div>`;
      const page = el.querySelector(".tr-page");
      tl.fromTo(page, { rotationY: -92, x: 0 }, { rotationY: 0, duration: 6 * F, ease: "power2.in", transformOrigin: "0% 50%" }, cut - 6 * F);
      tl.fromTo(page, { x: 0, rotation: 0 }, { x: -1200, rotation: -5, duration: 7 * F, ease: "power2.in", immediateRender: false }, cut);
    }
  },
});
