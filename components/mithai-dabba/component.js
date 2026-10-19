/* mithai-dabba — Mummy's box of laddoos. Each laddoo is 1/count of the whole, so the share that
 * leaves the box is always honest. Coordinates are inside .md-stage (= content zone, 880x890 at
 * x 60, y 236). Layouts:
 *   hero    big box (offer letter under it, Mummy's hand, sticker, static Chillar). Frame-1 safe.
 *           closeAt: the lid (standing open behind the box) folds shut, Chillar leans in and pushes it.
 *   slip    big box on top, payslip below; a laddoo:true line pulls a laddoo that arcs onto its row.
 *   close   push-in on the slip: one or two big rows, the box corner peeking in top-left.
 *   locker  box top-left, a steel PF locker: the laddoo goes in, the door shuts, padlock + tag. */
CH.define("mithai-dabba", {
  build({ el, p, t, d, tl, id, rng }) {
    const F = CH.F;
    const count = Math.max(1, +p.count || 22);
    const P = 104, V = 92, PAD = 42;
    const cells = [];
    for (let r = 0; cells.length < count; r++) {
      const n = r % 2 ? 5 : 6;
      for (let c = 0; c < n && cells.length < count; c++)
        cells.push({ x: PAD + (r % 2 ? P / 2 : 0) + c * P + P / 2, y: PAD + r * V + P / 2 });
    }
    const BW = 6 * P + 2 * PAD, BH = Math.max(...cells.map((c) => c.y)) + P / 2 + PAD;
    // removal order: bottom row first, spread out, so the gap reads at a glance
    const order = [...cells.keys()].sort((a, b) => (cells[b].y - cells[a].y) || ((a * 7) % 11) - ((b * 7) % 11));
    const pre = Math.min(+p.removed || 0, count);
    const gone = new Set(order.slice(0, pre));
    const lay = ["hero", "slip", "close", "locker"].includes(p.layout) ? p.layout : "hero";

    // box placement per layout (scale from the top-left corner)
    const BOX = {
      hero: p.closeAt != null ? { s: 0.85, x: 40, y: 300, tilt: -0.8 }
                              : { s: 1, x: p.hand ? 120 : 64, y: p.letter ? 300 : 250, tilt: CH.tilt(rng, 1.2) },
      slip: { s: 0.86, x: 20, y: 0, tilt: -1.2 },
      close: { s: 1.2, x: -330, y: -380, tilt: -4 },
      locker: { s: 0.6, x: 0, y: 40, tilt: -2 },
    }[lay];
    const { s, x: bx, y: by, tilt } = BOX;

    const laddoo = (k, size) => {
      const r2 = CH.rng(id + "-l" + k);
      const dots = Array.from({ length: 9 }, () => {
        const a = r2() * Math.PI * 2, rr = 8 + r2() * 24;
        return `<circle cx="${(50 + rr * Math.cos(a)).toFixed(1)}" cy="${(50 + rr * Math.sin(a)).toFixed(1)}" r="${(2.6 + r2() * 1.6).toFixed(1)}"/>`;
      }).join("");
      return `<svg class="md-laddoo-svg" viewBox="0 0 100 100" width="${size}" height="${size}">
        <circle class="ball" cx="50" cy="50" r="44"/><g class="boondi">${dots}</g><path class="shine" d="M26 40 Q30 27 43 23"/></svg>`;
    };
    // the paper cup: fluted pencil edge + a clear ink ring, so an empty slot reads as empty
    const cup = `<svg class="md-cup" viewBox="0 0 120 120" width="${P + 4}" height="${P + 4}"><circle class="flute" cx="60" cy="60" r="55"/><circle class="ring" cx="60" cy="60" r="43"/></svg>`;
    const cellsHtml = cells.map((c, k) => `
      <div class="md-cell" style="left:${c.x - P / 2}px; top:${c.y - P / 2}px; width:${P}px; height:${P}px">
        ${cup}${gone.has(k) ? "" : `<div class="md-laddoo" data-k="${k}">${laddoo(k, P - 6)}</div>`}</div>`).join("");

    const closing = lay === "hero" && p.closeAt != null;
    const box = `
      <div class="md-box" style="left:${bx}px; top:${by}px; width:${BW}px; height:${BH}px; transform: scale(${s}) rotate(${tilt.toFixed(2)}deg)">
        ${closing ? `<div class="md-lid-up"><div class="md-lid-trim"></div></div>` : ""}
        <div class="md-trim"></div><div class="md-tray">${cellsHtml}</div>
        ${closing ? `<div class="md-lid"><div class="md-lid-trim"></div><div class="md-seal"></div></div>` : ""}
      </div>`;

    // ---------------------------------------------------------------- hero extras
    const L = p.letter;
    const letter = lay === "hero" && L ? `
      <div class="md-letter paper-obj" style="transform: rotate(-2.4deg)">
        <div class="md-letter-top"><span class="t-head md-letter-title">${CH.esc(L.title || "")}</span>${L.note ? `<span class="md-letter-note t-body">${CH.esc(L.note)}</span>` : ""}</div>
        <div class="md-letter-line"><span class="t-body">${CH.esc(L.line || "")}</span>
          <span class="md-letter-amt t-num">${CH.esc(L.amount || "")}${CH.scribble("circle", { x: -22, y: -14, w: 34 * String(L.amount || "").length + 50, h: 120, rng, stroke: 7 })}</span></div>
      </div>` : "";
    const stk = p.sticker ? `
      <div class="md-sticker t-head" style="left:${p.closeAt != null && lay === "hero" ? bx + 30 : bx + BW * s - 330}px; top:${by - 30}px">${CH.esc(p.sticker)}
        ${p.stickerStrike != null ? CH.scribble("strike", { x: 4, y: 20, w: 310, h: 26, rng, stroke: 7 }) : ""}</div>` : "";
    const hy = by + BH * 0.62;
    const hand = lay === "hero" && p.hand ? `
      <svg class="md-arm" viewBox="-300 -80 340 160" width="340" height="160" style="left:${bx - 300}px; top:${hy - 80}px">
        <path class="skin" d="M-320 -30 C-220 -40 -110 -50 20 -56 L20 60 C-110 56 -220 52 -320 50 Z"/>
        <path class="bangle b1" d="M-196 -40 L-196 54"/><path class="bangle b2" d="M-174 -42 L-174 54"/><path class="bangle b3" d="M-152 -44 L-152 55"/>
      </svg>
      <svg class="md-fingers" viewBox="-20 -80 110 160" width="110" height="160" style="left:${bx - 20}px; top:${hy - 80}px">
        ${[-62, -30, 2, 34].map((y, i) => `<path class="skin" d="M-12 ${y} L${40 - i * 3} ${y} C${62 - i * 3} ${y} ${62 - i * 3} ${y + 30} ${40 - i * 3} ${y + 30} L-12 ${y + 30} Z"/>`).join("")}
      </svg>` : "";
    const msz = closing ? 240 : 270;
    const mLeft = closing ? bx + BW * s - 50 : 880 - msz + 20, mTop = closing ? by - 70 : 890 - msz * 1.1 + 6;
    const mascot = lay === "hero" && p.mascot ? `<div class="md-mascot" style="left:${mLeft}px; top:${mTop}px; width:${msz}px">${CH.mascot(p.mascot, id + "-m", msz)}</div>` : "";

    // ---------------------------------------------------------------- slip rows (slip + close)
    const lines = p.lines || [];
    const SL = p.slip || {};
    const big = lay === "close";
    const G = big ? { x: 0, y: 420, w: 880, head: 64, row: 150, dot: 66 } : { x: 0, y: BH * s + 30, w: 880, head: 92, row: 82, dot: 48 };
    const nrows = Math.max(lines.length, +SL.rows || 1);
    const rowTop = (i) => 26 + G.head + i * G.row;
    const lock = `<svg class="md-lock" viewBox="0 0 24 28" width="22" height="26"><path d="M6 12 V8 a6 6 0 0 1 12 0 V12"/><rect x="2.5" y="12" width="19" height="14" rx="2.5"/></svg>`;
    const subHtml = (ln) => ln.sub ? `<span class="t-print md-sub">${ln.icon === "lock" ? lock : ""}${CH.esc(ln.sub)}</span>` : "";
    const amtHtml = (ln) => `<span class="md-amt t-print ${ln.tone === "green" ? "t-green" : ln.tone === "ink" ? "" : "t-red"}">${CH.esc(ln.amount)}${
      ln.circle ? (big ? CH.scribble("circle", { x: -14, y: 4, w: 36 * String(ln.amount).length + 30, h: 62, rng, stroke: 7 })
                   : CH.scribble("circle", { x: -24, y: -14, w: 26 * String(ln.amount).length + 44, h: 76, rng, stroke: 7 })) : ""}</span>`;
    const rowHtml = (ln, i) => `
      <div class="md-line" style="top:${rowTop(i)}px; height:${G.row}px">
        <span class="md-dot" style="width:${G.dot}px; height:${G.dot}px">${ln.laddoo ? `<span class="md-mini">${laddoo("m" + i, G.dot - 4)}</span>` : ""}</span>
        ${big ? `<span class="md-lab"><span class="t-body">${CH.esc(ln.label)}</span><span class="md-amtrow">${amtHtml(ln)}${subHtml(ln)}</span></span>`
              : `<span class="md-lab"><span class="t-body">${CH.esc(ln.label)}</span>${subHtml(ln)}</span>${amtHtml(ln)}`}
      </div>`;
    const ghosts = Array.from({ length: Math.max(0, nrows - lines.length) }, (_, j) =>
      `<div class="md-ghost" style="top:${rowTop(lines.length + j) + G.row / 2 - 7}px"><i style="width:${38 - j * 6}%"></i><i style="width:22%"></i></div>`).join("");
    const slip = (lay === "slip" || lay === "close") ? `
      <div class="md-slip paper-obj ${big ? "big" : ""}" style="left:${G.x}px; top:${G.y}px; width:${G.w}px; height:${26 + G.head + nrows * G.row + 26}px; transform: rotate(${big ? -1.2 : 0.8}deg)">
        <div class="md-slip-head"><span class="t-head">${big ? "" : CH.esc(SL.title || "Salary slip")}</span><span class="t-print t-sub">${CH.esc(SL.meta || "")}</span></div>
        ${lines.map(rowHtml).join("")}${ghosts}
      </div>` : "";

    // ---------------------------------------------------------------- locker
    const K = p.locker || {};
    const solo = lay === "locker" && p.box === false;   // box:false = no dabba; the locker alone, centred and bigger
    const LX = solo ? 230 : 450, LY = 30, LW = 410, LH = 660;
    const locker = lay === "locker" ? `
      <div class="md-locker" style="left:${LX}px; top:${LY}px; width:${LW}px; height:${LH}px${solo ? "; transform: scale(1.3); transform-origin: 50% 0" : ""}">
        <div class="md-locker-body"><i class="v"></i><i class="v"></i><i class="v"></i></div>
        <div class="md-locker-in"><div class="md-shelf"></div>${K.inside ? `<div class="md-inside paper-obj"><span class="t-print">${CH.esc(K.inside)}</span></div>` : ""}</div>
        <div class="md-door">
          <div class="md-plate"><span class="t-head">${CH.esc(K.label || "")}</span><span class="t-print">${CH.esc(K.amount || "")}</span>${K.sub ? `<span class="t-body t-sub">${CH.esc(K.sub)}</span>` : ""}</div>
          <i class="md-handle"></i><i class="v"></i><i class="v"></i><i class="v"></i>
        </div>
        <div class="md-padlock">
          <svg viewBox="0 0 80 100" width="96" height="120"><path class="sh" d="M20 46 V30 a20 20 0 0 1 40 0 V46"/><rect class="bd" x="8" y="44" width="64" height="50" rx="8"/><circle class="kh" cx="40" cy="64" r="6"/><path class="kh" d="M40 66 V80"/></svg>
          <svg class="md-string" viewBox="0 0 60 90" width="60" height="90"><path d="M6 6 C20 30 30 50 40 84"/></svg>
          <div class="md-tag t-body">${CH.esc(K.tag || "")}</div>
        </div>
      </div>` : "";

    el.innerHTML = `<div class="md-stage md-${lay}">${letter}${hand}${solo ? "" : box}${stk}${slip}${locker}${mascot}<div class="md-fly"></div></div>`;
    const fly = el.querySelector(".md-fly");
    const ladEls = {}; el.querySelectorAll(".md-laddoo").forEach((n) => { ladEls[n.dataset.k] = n; });
    const rowEls = [...el.querySelectorAll(".md-line")];

    // ---------------------------------------------------------------- motion (frame 1 = final layout)
    if (L) CH.draw(tl, el.querySelector(".md-letter-amt"), t + 0.35, 0.3);
    if (lay === "hero" && p.mascot && !closing) CH.mascotAnim(tl, el.querySelector(".md-mascot svg"), "blink", t + 0.2, d - 0.2);
    if (p.stickerStrike != null) CH.draw(tl, el.querySelector(".md-sticker"), t + +p.stickerStrike, 0.3);
    const slipEl = el.querySelector(".md-slip");
    if (slipEl && SL.at != null) tl.fromTo(slipEl, { x: 150, y: 40, rotation: 4, scale: 0.92 }, { x: 0, y: 0, rotation: 0.8, scale: 1, duration: 7 * F, ease: "back.out(1.6)" }, t + +SL.at);

    const at = (k) => ({ x: bx + cells[k].x * s, y: by + cells[k].y * s });
    let next = pre;
    // a laddoo leaves its cup: lifts, arcs high, drops onto its target (visible the whole way)
    const pull = (tt, target) => {
      if (next >= count) return null;
      const k = order[next++];
      const src = ladEls[k];
      const sz = (P - 6) * s, pos = at(k);
      const f = CH.h(`<div class="md-flyer" style="left:${pos.x - sz / 2}px; top:${pos.y - sz / 2}px; width:${sz}px; height:${sz}px">${laddoo(k, sz)}</div>`);
      fly.appendChild(f);
      const dx = target.x - pos.x, dy = target.y - pos.y, lift = 5 * F, up = 0.22, down = 0.3;
      const peak = Math.min(0, dy) - (target.arc ?? 150);
      tl.fromTo(src, { opacity: 1 }, { opacity: 0, duration: F, ease: "none" }, tt);
      tl.fromTo(f, { opacity: 0 }, { opacity: 1, duration: F, ease: "none" }, tt);
      tl.fromTo(f, { y: 0, scale: 1 }, { y: -30, scale: 1.22, duration: lift, ease: "power2.out" }, tt);
      tl.fromTo(f, { x: 0 }, { x: dx, duration: up + down, ease: "power1.inOut", immediateRender: false }, tt + lift);
      tl.fromTo(f, { y: -30 }, { y: peak, duration: up, ease: "power2.out", immediateRender: false }, tt + lift);
      tl.fromTo(f, { y: peak }, { y: dy, duration: down, ease: "power2.in", immediateRender: false }, tt + lift + up);
      tl.fromTo(f, { rotation: 0 }, { rotation: 220, duration: up + down, ease: "none", immediateRender: false }, tt + lift);
      tl.fromTo(f, { scale: 1.22 }, { scale: target.scale ?? 1, duration: up + down, ease: "power1.in", immediateRender: false }, tt + lift);
      const landed = tt + lift + up + down;
      if (target.hide) tl.fromTo(f, { visibility: "visible" }, { visibility: "hidden", duration: F, ease: "none", immediateRender: false }, landed);
      return landed;
    };
    (p.remove || []).forEach((o) => pull(t + +o, { x: 1000, y: -260, scale: 1.3, hide: true }));

    lines.forEach((ln, i) => {
      const row = rowEls[i];
      if (!row) return;
      if (ln.at != null) {
        let tt = t + +ln.at;
        const mini = row.querySelector(".md-mini");
        if (ln.laddoo) {
          const target = { x: G.x + 40 + G.dot / 2, y: G.y + rowTop(i) + G.row / 2, scale: (G.dot - 4) / ((P - 6) * s), hide: true };
          const landed = pull(tt, target);
          if (landed) {
            if (mini) tl.fromTo(mini, { opacity: 0 }, { opacity: 1, duration: F, ease: "none" }, landed);
            tt = landed - 2 * F;
          }
        }
        tl.fromTo(row, { opacity: 0, y: -8 }, { opacity: 1, y: 0, duration: 2 * F, ease: "steps(2)" }, tt);
        if (ln.circle && ln.amountAt == null) CH.draw(tl, row.querySelector(".md-amt"), tt + 0.12, 0.3);
      } else if (ln.circle && ln.amountAt == null) CH.draw(tl, row.querySelector(".md-amt"), t + 0.2, 0.01);
      if (ln.amountAt != null) {     // the amount prints later than its label (the reveal)
        const amt = row.querySelector(".md-amt");
        tl.fromTo(amt, { opacity: 0, scale: 1.3 }, { opacity: 1, scale: 1, duration: 4 * F, ease: "power3.out" }, t + +ln.amountAt);
        if (ln.circle) CH.draw(tl, amt, t + +ln.amountAt + 0.15, 0.3);
      }
    });

    // locker: laddoo in, door shuts, padlock drops with its tag
    if (lay === "locker") {
      const door = el.querySelector(".md-door");
      // doorAt / lockAt: null = already shut / already locked at the scene start (fully drawn frame 1)
      const shut = "doorAt" in K && K.doorAt === null;
      const locked = "lockAt" in K && K.lockAt === null;
      const doorAt = K.doorAt ?? 1.1;
      const pad = el.querySelector(".md-padlock");
      if (!shut) {
        if (K.laddooAt != null && pull(t + +K.laddooAt, { x: LX + LW / 2, y: LY + LH * 0.42 - 40, scale: 1.4, arc: 120 }))
          tl.fromTo(fly.lastElementChild, { visibility: "visible" }, { visibility: "hidden", duration: F, ease: "none", immediateRender: false }, t + doorAt + 5 * F);
        tl.fromTo(door, { rotationY: 78 }, { rotationY: 0, duration: 7 * F, ease: "power3.in" }, t + doorAt);   // < 90°: the open door stays on its own side of the hinge (inside the safe zone)
        tl.fromTo(door.querySelectorAll(".md-plate, .md-handle"), { opacity: 0 }, { opacity: 1, duration: F, ease: "none" }, t + doorAt + 5 * F);
        tl.fromTo(door, { x: 0 }, { x: 4, duration: F, ease: "none", immediateRender: false }, t + doorAt + 8 * F);
        tl.to(door, { x: 0, duration: 2 * F, ease: "none" }, t + doorAt + 9 * F);
      }
      if (!locked)
        tl.fromTo(pad, { opacity: 0, y: -70, rotation: -14 }, { opacity: 1, y: 0, rotation: 0, duration: 7 * F, ease: "back.out(1.6)" }, t + +(K.lockAt ?? 2));
      // openAt: the padlock pops off and falls away, then the door swings open (the reverse of the close)
      if (K.openAt != null) {
        const o = t + +K.openAt;
        tl.to(pad, { y: 90, rotation: 18, opacity: 0, duration: 6 * F, ease: "power3.in" }, o);
        tl.to(door.querySelectorAll(".md-plate, .md-handle"), { opacity: 0, duration: F, ease: "none" }, o);
        tl.to(door, { rotationY: 78, duration: 7 * F, ease: "power3.out" }, o + 5 * F);
        const inside = el.querySelector(".md-inside");
        if (inside) tl.fromTo(inside, { opacity: 0 }, { opacity: 1, duration: 3 * F, ease: "none" }, o + 6 * F);
      }
    }

    // hero close: the lid stands open behind the box; Chillar leans in and folds it shut, then holds
    if (closing) {
      const c0 = t + +p.closeAt;
      const fig = el.querySelector(".md-mascot");
      const arm = fig.querySelector(".arm-l");
      if (arm) tl.fromTo(arm, { rotation: 0 }, { rotation: 70, duration: 6 * F, ease: "power2.out", svgOrigin: "78 205" }, c0 - 10 * F);
      tl.fromTo(fig, { x: 0, y: 0, rotation: 0 }, { x: -70, y: -34, rotation: -16, duration: 6 * F, ease: "power2.out", transformOrigin: "50% 100%" }, c0 - 5 * F);
      tl.fromTo(el.querySelector(".md-lid-up"), { scaleY: 1 }, { scaleY: 0, duration: 3 * F, ease: "power2.in" }, c0);
      tl.fromTo(el.querySelector(".md-lid"), { opacity: 0 }, { opacity: 1, duration: F, ease: "none" }, c0 + 2 * F);
      tl.fromTo(el.querySelector(".md-lid"), { scaleY: 0.05 }, { scaleY: 1, duration: 6 * F, ease: "power2.in" }, c0 + 2 * F);
      tl.fromTo(el.querySelector(".md-box"), { y: 0 }, { y: 6, duration: 2 * F, ease: "none", immediateRender: false }, c0 + 8 * F);
      tl.to(el.querySelector(".md-box"), { y: 0, duration: 3 * F, ease: "power2.out" }, c0 + 10 * F);
      tl.to(fig, { x: -20, y: 0, rotation: 0, duration: 8 * F, ease: "power2.inOut" }, c0 + 10 * F);
      if (arm) tl.to(arm, { rotation: 0, duration: 8 * F, ease: "power2.inOut" }, c0 + 12 * F);
    }
  },
});
