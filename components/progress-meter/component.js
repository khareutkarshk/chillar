CH.define("progress-meter", {
  build({ el, p, t, tl }) {
    const n = Math.max(2, +p.coins || 8);
    const was = Math.round((+p.from || 0) * n), now = Math.round((+p.to || 0) * n);
    el.innerHTML = `<div class="pm-row">${[...Array(n)].map((_, i) => `<div class="pm-coin ${i < now ? "on" : ""}"></div>`).join("")}</div>`;
    [...el.querySelectorAll(".pm-coin")].slice(was, now).forEach((c, i) =>
      tl.fromTo(c, { y: -60, opacity: 0 }, { y: 0, opacity: 1, duration: 6 * CH.F, ease: "back.out(2)" }, t + 0.1 + i * 3 * CH.F));
  },
});
