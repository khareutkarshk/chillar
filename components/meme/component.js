CH.define("meme", {
  build({ el, p, t, d, tl, id, rng }) {
    // _src/_w/_h (+ _frames/_cols/_rows/_fps for a GIF sprite) are filled by validate_scenes from pipeline/memes.py
    const W = Math.min(860, Math.max(560, +p.width || 860)), PAD = 18, headH = p.headline ? 130 : 0;
    const maxPicH = 880 - headH - 2 * PAD;
    let pw = W - 2 * PAD, ph = pw * (+p._h || 1) / (+p._w || 1);
    if (p.wide && p.kind !== "video") ph = Math.min(maxPicH, Math.max(420, +p.height || 700));
    else if (ph > maxPicH) { pw = pw * maxPicH / ph; ph = maxPicH; }
    const tilt = CH.tilt(rng, 1.8);
    const sprite = p.kind === "video" && +p._frames > 1;
    const bg = sprite ? `background-size:${p._cols * 100}% ${p._rows * 100}%;background-position:0 0;` : "";
    el.innerHTML = `
      <div class="zone">
        ${p.headline ? `<div class="mm-head t-head">${CH.rich(p.headline)}</div>` : ""}
        <div class="mm-photo paper-obj" style="width:${(pw + 2 * PAD).toFixed(0)}px">
          <div class="mm-pic" style="width:${pw.toFixed(0)}px;height:${ph.toFixed(0)}px;background-image:url('${CH.esc(p._src || "")}');${p.wide ? `background-position:${CH.esc(p.position || "center")};` : ""}${bg}">
            ${(p.labels || []).map((l) => `<div class="mm-label" style="left:${+l.x}%;top:${+l.y}%">${CH.rich(l.text)}</div>`).join("")}
          </div>
        </div>
      </div>`;
    const photo = el.querySelector(".mm-photo"), head = el.querySelector(".mm-head");
    if (head) CH.pop(tl, head, t);
    CH.toss(tl, photo, t, tilt);
    if (sprite) {          // step the GIF frames on the master timeline: seek-safe, loops for the whole shot
      const pic = el.querySelector(".mm-pic"), n = +p._frames, cols = +p._cols, rows = +p._rows, st = { f: 0 };
      const show = () => {
        const i = Math.floor(st.f) % n, c = i % cols, r = Math.floor(i / cols);
        pic.style.backgroundPosition = `${cols > 1 ? (c / (cols - 1)) * 100 : 0}% ${rows > 1 ? (r / (rows - 1)) * 100 : 0}%`;
      };
      tl.fromTo(st, { f: 0 }, { f: d * (+p._fps || 12), duration: d, ease: "none", onUpdate: show }, t);
    }
    CH.markers(tl, el, t + 0.2);
  },
});
