// calculator — paper desk calculator; keys tapped in sequence, result strip prints on '='.
CH.define("calculator", {
  build({ el, p, t, tl, rng }) {
    const tilt = CH.tilt(rng);
    const taps = (p.taps && p.taps.length ? p.taps : ["2", "5", "×", "4", "="]).map(String);
    const keys = ["7", "8", "9", "÷", "4", "5", "6", "×", "1", "2", "3", "−", "0", ".", "+", "="];
    const isOp = (k) => "÷×−+=".includes(k);
    const keyHtml = keys.map((k) => `<div class="ca-key${isOp(k) ? " op" : ""}" data-k="${CH.esc(k)}">${k}</div>`).join("");
    const result = p.result == null ? "" : String(p.result);
    el.innerHTML = `<div class="zone ca-wrap">
      <div class="ca-body paper-obj" style="transform: rotate(${tilt.toFixed(2)}deg)"><div class="ca-disp">&nbsp;</div><div class="ca-keys">${keyHtml}</div></div>
      <div class="ca-strip paper-obj" style="transform: rotate(${(-tilt).toFixed(2)}deg)">${CH.esc(result)}</div></div>`;
    CH.toss(tl, el.querySelector(".ca-body"), t, tilt);
    const disp = el.querySelector(".ca-disp"), strip = el.querySelector(".ca-strip");
    const gap = +p.tapGap || 0.28, t0 = t + (p.tapStart == null ? 0.3 : +p.tapStart);
    // strip starts closed (height 0) and prints open on '='
    tl.set(strip, { clipPath: "inset(0 0 100% 0)" }, 0);
    tl.call(() => { disp.innerHTML = "&nbsp;"; }, null, t);
    let expr = "";
    taps.forEach((k, i) => {
      const at = t0 + i * gap, last = i === taps.length - 1 && k === "=";
      const node = el.querySelector(`.ca-key[data-k="${k}"]`);
      expr = last ? result : expr + k;
      const shown = expr;
      tl.call(() => { disp.textContent = shown; }, null, at);
      if (node) {
        tl.to(node, { y: 6, duration: 2 * CH.F, ease: "power3.out" }, at);
        tl.to(node, { y: 0, duration: 3 * CH.F, ease: "power3.out" }, at + 2 * CH.F);
      }
      if (last) tl.to(strip, { clipPath: "inset(0 0 0% 0)", duration: 6 * CH.F, ease: "power3.out" }, at + 2 * CH.F);
    });
  },
});
