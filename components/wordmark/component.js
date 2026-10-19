CH.define("wordmark", {
  build({ el, p }) {
    el.innerHTML = `<div class="wm"><span class="wm-coin"></span><span>${CH.esc(p.handle)}</span></div>`;
  },
});
