/* chat-screen — a generic phone chat, printed out and lying on the field: no app colours, no logos.
 * Messages type in one by one ("them" after a typing-dots bubble, "me" slides in from the right);
 * optional pinned bar; optional blue-ballpoint circle on one message. The final layout is reserved
 * from the cut, so nothing reflows while messages arrive. */
// Ask for the faces now (script load) so document.fonts.ready waits and bubble sizes are final at build.
if (document.fonts && document.fonts.load) {
  document.fonts.load('800 44px "Mukta"');
  document.fonts.load('600 28px "JetBrains Mono"', "0123456789:");
}
CH.define("chat-screen", {
  build({ el, p, t, tl, rng, id }) {
    const msgs = (Array.isArray(p.messages) ? p.messages : []).slice(0, 6);
    const width = Math.min(880, Math.max(560, +p.width || 820));
    const tilt = (p.tilt !== null && p.tilt !== undefined && p.tilt !== "") ? +p.tilt : CH.tilt(rng, 1.6);
    const stagger = +p.stagger || 0.5, first = 0.3;
    // timestamps: seeded clock, a minute here and there (or msg.time); JetBrains Mono like printout metadata
    let hh = 9 + Math.floor(rng() * 3), mm = 2 + Math.floor(rng() * 48);
    const stamp = (m) => {
      if (m.time) return String(m.time);
      const s = `${hh}:${String(mm).padStart(2, "0")}`;
      if (rng() < 0.45) { mm += 1; if (mm > 59) { mm = 0; hh += 1; } }
      return s;
    };
    const showTimes = p.times !== false;
    const name = String(p.name || "");
    el.innerHTML = `
      <div class="zone">
        <div class="cs-phone" style="width:${width}px; transform: rotate(${tilt.toFixed(2)}deg)">
          ${name ? `<div class="cs-head">
            <svg class="cs-back" viewBox="0 0 30 48" width="22" height="36"><path d="M24 4 L6 24 L24 44"/></svg>
            <div class="cs-ava t-body">${CH.esc([...name.trim()][0] || "")}</div>
            <div class="cs-name t-body">${CH.esc(name)}</div></div>` : ""}
          ${p.pinned ? `<div class="cs-pin${name ? "" : " top"}">
            <svg class="cs-pin-i" viewBox="0 0 40 48" width="30" height="36"><path d="M13 4 H27 M15 4 V18 L7 28 H33 L25 18 V4 M20 28 V44"/></svg>
            <div class="cs-pin-t t-body">${CH.rich(p.pinned)}</div></div>` : ""}
          <div class="cs-list${showTimes ? "" : " notime"}">
            ${msgs.map((m, i) => {
              const me = m.from === "me";
              return `<div class="cs-row ${me ? "me" : "them"}" data-i="${i}">
                <div class="cs-bub t-body">${CH.rich(m.text)}${showTimes ? `<span class="cs-time">${CH.esc(stamp(m))}</span>` : ""}</div>
                ${me ? "" : `<div class="cs-dots"><i></i><i></i><i></i></div>`}
              </div>`;
            }).join("")}
          </div>
        </div>
      </div>`;

    const phone = el.querySelector(".cs-phone");
    CH.toss(tl, phone, t, tilt);
    const rows = [...el.querySelectorAll(".cs-row")];
    const hi = (p.highlight === null || p.highlight === undefined || p.highlight === "") ? -1 : +p.highlight;
    rows.forEach((row, i) => {
      const at = t + first + i * stagger;
      const bub = row.querySelector(".cs-bub"), dots = row.querySelector(".cs-dots");
      const me = row.classList.contains("me");
      if (dots) {                                    // "them" is typing…
        const d0 = Math.max(t + 2 * CH.F, at - Math.min(0.42, stagger * 0.7));
        tl.fromTo(dots, { opacity: 0 }, { opacity: 1, duration: CH.F, ease: "none" }, d0);
        tl.fromTo(dots, { opacity: 1 }, { opacity: 0, duration: CH.F, ease: "none", immediateRender: false }, at - CH.F);
        [...dots.children].forEach((dot, k) => {
          for (let b = d0 + k * 0.08; b < at - 0.05; b += 0.3)
            tl.fromTo(dot, { y: 0 }, { y: -7, duration: 0.12, ease: "sine.out", yoyo: true, repeat: 1, immediateRender: false }, b);
        });
      }
      tl.fromTo(bub, { opacity: 0 }, { opacity: 1, duration: CH.F, ease: "none" }, at - CH.F);
      tl.fromTo(bub, { x: me ? 36 : 0, y: me ? 0 : 18, scale: 0.94, transformOrigin: me ? "100% 100%" : "0% 100%" },
        { x: 0, y: 0, scale: 1, duration: 5 * CH.F, ease: "power3.out" }, at);
      CH.markers(tl, bub, at + 0.2);
      if (i === hi) {                                // blue-ballpoint circle, drawn at hand speed
        const bw = bub.offsetWidth, bh = bub.offsetHeight, bx = me ? row.offsetWidth - bw : 0;
        row.insertAdjacentHTML("beforeend", CH.scribble("circle", { x: bx - 22, y: -16, w: bw + 44, h: bh + 32, rng, stroke: 7, cls: "cs-circ" }));
        CH.draw(tl, row, at + 0.3, 0.45);
      }
      if (p.grow) {                                  // paper grows: a row takes no space until it arrives
        row.style.display = "none";
        const d = dots ? Math.max(t + 2 * CH.F, at - Math.min(0.42, stagger * 0.7)) : at - CH.F;
        tl.fromTo(row, { display: "none" }, { display: "flex", duration: 0, immediateRender: false }, Math.min(d, at - CH.F));
      }
    });
  },
});
