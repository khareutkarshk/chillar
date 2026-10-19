CH.define("avatar", {
  build({ el, p, id }) {
    el.innerHTML = `<div class="av">${CH.mascot(p.expr, id + "-m", 1032)}</div>`;
  },
});
