CH.define("cover", {
  build({ el, p, id }) {
    el.innerHTML = `
      <div class="cv-crop">
        <div class="cv-text t-head">${CH.rich(p.text)}</div>
        ${p.kicker ? `<div class="cv-tagline t-body"><span class="marker">${CH.esc(p.kicker)}</span></div>` : ""}
        <div class="cv-bottom">
          ${p.stamp ? `<div class="cv-stamp t-head"><div class="st-paper"></div><div class="st-ink">${CH.esc(p.stamp)}</div></div>` : "<span></span>"}
          ${p.mascot && p.mascot !== "none" ? `<div class="cv-mascot">${CH.mascot(p.mascot, id + "-m", 400)}</div>` : ""}
        </div>
      </div>`;
  },
});
