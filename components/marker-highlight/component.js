CH.define("marker-highlight", {
  build({ el, p, t, tl }) {
    const c = p.align === "center";
    el.innerHTML = `
      <div class="zone ${c ? "center" : ""}" style="text-align:${c ? "center" : "left"}">
        <div class="mh-text t-head" style="font-size:${+p.size}px">${CH.rich(p.text)}</div>
        ${p.sub ? `<div class="mh-sub t-body">${CH.rich(p.sub)}</div>` : ""}
      </div>`;
    [...el.querySelectorAll(".mh-text, .mh-sub")].forEach((n, i) => CH.pop(tl, n, t + i * 4 * CH.F));
    CH.markers(tl, el, t + (+p.markerAt));
  },
});
