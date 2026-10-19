CH.define("stamp", {
  build({ el, p, t, tl }) {
    el.innerHTML = `
      <div class="st-anchor" style="left:${+p.x}px; top:${+p.y}px">
        <div class="st-stamp" style="font-size:${+p.size}px">
          <div class="st-paper"></div>
          <div class="st-ink">
            <div class="st-text">${CH.esc(p.text)}</div>
            ${p.sub ? `<div class="st-sub">${CH.esc(p.sub)}</div>` : ""}
          </div>
        </div>
      </div>`;
    CH.slam(tl, el.querySelector(".st-stamp"), t, +p.rotate);
  },
});
