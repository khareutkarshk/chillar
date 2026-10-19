/* Captions are not a CH scene: build_composition emits one clip per caption group
 * (#cap0, #cap1, ...) and these two functions fill + animate them on the master timeline. */
window.CHCaptions = {
  build(groups) {
    (groups || []).forEach((g, i) => {
      const el = document.getElementById("cap" + i);
      if (!el) return;
      el.innerHTML = `<div class="cap-line">${g.words.map((w) => `<span class="cap-w">${CH.esc(w.text)}</span>`).join(" ")}</div>`;
    });
  },
  animate(tl, groups) {
    (groups || []).forEach((g, i) => {
      const el = document.getElementById("cap" + i);
      if (!el) return;
      tl.fromTo(el.querySelector(".cap-line"), { y: 14, opacity: 0 }, { y: 0, opacity: 1, duration: 3 * CH.F, ease: "power2.out" }, g.start);
      const spans = [...el.querySelectorAll(".cap-w")];
      g.words.forEach((w, j) => {
        const s = spans[j];
        tl.set(s, { "--on": 1, scale: 1.05 }, w.start);
        const next = g.words[j + 1];
        const off = next ? next.start : g.end;
        tl.set(s, { "--on": 0, scale: 1 }, Math.max(off, w.start + 0.05));
      });
    });
  },
};
