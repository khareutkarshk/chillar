/* glyph-character — a big typographic glyph ("*", "%", "₹", "0%", "T&C") turned into a deadpan
 * character: half-closed eyes, stick limbs and an ink costume drawn as SVG lines.
 * Layout is measured once at build (fonts are ready): canvas ink metrics centre the glyph on (x, y)
 * and a low-res pixel probe finds where legs, arms and hats attach, so any glyph works. */
// Ask for the headline face now (script load), so the bootstrap's document.fonts.ready waits for it and
// the build-time ink measurements below never see a fallback font.
if (document.fonts && document.fonts.load) document.fonts.load('800 100px "Bricolage Grotesque"', "*%₹T&C0");
CH.define("glyph-character", {
  build({ el, p, t, d, tl, id, rng }) {
    const FONT = `"Bricolage Grotesque", "Mukta", sans-serif`;
    const glyph = String(p.glyph ?? "*") || "*";
    const X = +p.x, Y = +p.y, maxW = +p.maxWidth || 620;
    const tone = p.tone === "red" ? "var(--red)" : "var(--on-field)";
    const bs = p.bubbleSide === "left" ? -1 : 1;             // bubble side; the busy arm goes opposite
    const s = -bs;
    const J = (v) => (rng() * 2 - 1) * v;                     // seeded hand wobble
    const f1 = (n) => n.toFixed(1);

    // ---- ink metrics (em) -> font size so the glyph's INK is `size` px tall (wide glyphs capped at maxWidth)
    const cx2 = document.createElement("canvas").getContext("2d");
    cx2.font = `800 100px ${FONT}`;
    const m = cx2.measureText(glyph);
    const L = m.actualBoundingBoxLeft / 100, R = m.actualBoundingBoxRight / 100;
    const A = m.actualBoundingBoxAscent / 100, D = m.actualBoundingBoxDescent / 100;
    let fs = +p.size / Math.max(0.05, A + D);
    if (fs * (L + R) > maxW) fs = maxW / (L + R);
    const h = fs * (A + D), w = fs * (L + R);
    const tx = -w / 2 + L * fs, ty = -h / 2 + A * fs;        // text origin that centres the ink on 0,0

    // ---- pixel probe (quarter scale) of the ink, in glyph-centred px
    const S = 0.25, pad = 4;
    const pc = document.createElement("canvas");
    pc.width = Math.ceil(w * S) + 2 * pad; pc.height = Math.ceil(h * S) + 2 * pad;
    const pg = pc.getContext("2d");
    pg.font = `800 ${fs * S}px ${FONT}`; pg.fillStyle = "#000";
    pg.fillText(glyph, pad + L * fs * S, pad + A * fs * S);
    const px = pg.getImageData(0, 0, pc.width, pc.height).data;
    const ink = (gx, gy) => {
      const i = Math.round((gx + w / 2) * S + pad), j = Math.round((gy + h / 2) * S + pad);
      return i >= 0 && j >= 0 && i < pc.width && j < pc.height && px[(j * pc.width + i) * 4 + 3] > 120;
    };
    const step = 1 / S;
    const lowest = (x0, x1) => { for (let gy = h / 2; gy > -h / 2; gy -= step) for (let gx = x0; gx <= x1; gx += step) if (ink(gx, gy)) return gy; return h / 2; };
    const highest = (x0, x1) => { for (let gy = -h / 2; gy < h / 2; gy += step) for (let gx = x0; gx <= x1; gx += step) if (ink(gx, gy)) return gy; return -h / 2; };
    const edge = (y0, y1, side) => {                         // outermost ink point [x, y] on one side within a row band
      for (let gx = side * w / 2; side > 0 ? gx > 0 : gx < 0; gx -= side * step)
        for (let gy = y0; gy <= y1; gy += step) if (ink(gx, gy)) return [gx, gy];
      return [side * w * 0.3, (y0 + y1) / 2];
    };

    const lw = Math.max(8, h * 0.032);                        // limb stroke
    const seam = Math.max(3, h * 0.011);
    const cos = p.costume || "none";
    const u = h;                                              // unit for every accessory

    // ---- eyes (deadpan half-closed like Chillar)
    const erx = Math.max(22, Math.min(72, Math.max(u, w * 0.55) * 0.13)), ery = erx * 0.84, ey = -u * 0.07;
    const eyeKind = p.eyes || "deadpan";
    const eye = (side) => {
      const ex = side * erx * 1.12 + (p.costume === "detective" ? 0 : 0);
      const cover = (eyeKind === "side-eye" ? 0.56 : 0.5) + J(0.03);
      const top = ey - ery, lidL = top + 2 * ery * (cover + (side < 0 ? 0.04 : -0.02)), lidR = top + 2 * ery * (cover + (side < 0 ? -0.02 : 0.04));
      const pdx = eyeKind === "side-eye" ? bs * erx * 0.42 : side * -erx * 0.06;
      const clip = `${id}-ec${side < 0 ? "l" : "r"}`;
      const sw = Math.max(4, erx * 0.16);
      return `<g class="gc-eye">
        <clipPath id="${clip}"><ellipse cx="${f1(ex)}" cy="${f1(ey)}" rx="${f1(erx)}" ry="${f1(ery)}"/></clipPath>
        <ellipse cx="${f1(ex)}" cy="${f1(ey)}" rx="${f1(erx)}" ry="${f1(ery)}" fill="var(--paper)"/>
        <circle cx="${f1(ex + pdx)}" cy="${f1(ey + ery * 0.36)}" r="${f1(erx * 0.34)}" fill="var(--ink)"/>
        <g clip-path="url(#${clip})">
          <polygon points="${f1(ex - erx - 4)},${f1(top - 4)} ${f1(ex + erx + 4)},${f1(top - 4)} ${f1(ex + erx + 4)},${f1(lidR)} ${f1(ex - erx - 4)},${f1(lidL)}" fill="${tone}"/>
          <line x1="${f1(ex - erx - 4)}" y1="${f1(lidL)}" x2="${f1(ex + erx + 4)}" y2="${f1(lidR)}" stroke="var(--ink)" stroke-width="${f1(sw * 1.15)}"/>
        </g>
        <ellipse cx="${f1(ex)}" cy="${f1(ey)}" rx="${f1(erx)}" ry="${f1(ery)}" fill="none" stroke="var(--ink)" stroke-width="${f1(sw)}"/>
      </g>`;
    };
    const eyes = eyeKind === "none" ? "" : `<g class="gc-eyes">${eye(-1)}${eye(1)}</g>`;

    // ---- limbs (stick lines in the field's ink, like Chillar's)
    const line = (pts, j = u * 0.008) => "M" + pts.map(([a, b], i) => `${f1(a + (i ? J(j) : 0))} ${f1(b + (i ? J(j) : 0))}`).join(" L");
    const limb = (pts, hand = true) => {
      const e = pts[pts.length - 1];
      return `<path d="${line(pts)}" class="gc-limb" stroke-width="${f1(lw)}"/>` +
        (hand ? glove(e) : "");
    };
    // cartoon glove hands: paper with an ink line, so they read on the glyph and on the field
    const glove = ([a, b], r = lw * 1.15) => `<circle cx="${f1(a)}" cy="${f1(b)}" r="${f1(r)}" fill="var(--paper)" stroke="var(--ink)" stroke-width="${f1(seam)}"/>`;
    // coat sleeve: ink with a paper seam (reads over the glyph), glove at the end
    const sleeve = (pts, finger = false) => {
      const d = line(pts), e = pts[pts.length - 1];
      return `<path d="${d}" fill="none" stroke="var(--paper)" stroke-width="${f1(lw * 1.9 + 2 * seam)}" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="${d}" fill="none" stroke="var(--ink)" stroke-width="${f1(lw * 1.9)}" stroke-linecap="round" stroke-linejoin="round"/>` +
        (finger ? `<rect x="${f1(e[0] - lw * 0.42)}" y="${f1(e[1] - lw * 2.6)}" width="${f1(lw * 0.84)}" height="${f1(lw * 2.4)}" rx="${f1(lw * 0.42)}" fill="var(--paper)" stroke="var(--ink)" stroke-width="${f1(seam)}"/>` : "") + glove(e);
    };
    let coatBottom = null, coatW = 0;
    const legs = () => {
      const out = [];
      for (const side of [-1, 1]) {
        let lx = side * Math.max(u * 0.11, Math.min(w * 0.2, u * 0.2)), y0;
        if (coatBottom !== null) { lx = side * Math.min(coatW * 0.26, u * 0.16); y0 = coatBottom - lw; }
        else {
          // walk outward from the preferred spot until the ink actually reaches the bottom (no legs from mid-air)
          const low = (x) => lowest(x - u * 0.03, x + u * 0.03);
          let best = lx, bestY = low(lx);
          for (let k = 0; k < 40 && bestY < h / 2 - u * 0.1; k++) {
            const x = lx + side * k * u * 0.02;
            if (Math.abs(x) > w / 2) break;
            const yy = low(x); if (yy > bestY) { best = x; bestY = yy; }
          }
          lx = best; y0 = bestY - lw * 0.6;
        }
        const yf = Math.max(h / 2, coatBottom ?? 0) + u * 0.2;
        out.push(`<path d="${line([[lx, y0], [lx + side * u * 0.012, yf], [lx + side * u * 0.085, yf + J(3)]])}" class="gc-limb" stroke-width="${f1(lw)}"/>`);
      }
      return out.join("");
    };
    const armY = u * 0.06;
    const sideP = (side) => { const [ex, eyy] = edge(armY - u * 0.06, armY + u * 0.18, side); return [ex - side * lw * 0.5, eyy]; };
    const restArm = (side, [x0, y0] = sideP(side)) =>
      limb([[x0, y0], [x0 + side * u * 0.1, y0 + u * 0.14], [x0 + side * u * 0.12, y0 + u * 0.27]]);

    // ---- costumes
    const topY = highest(-u * 0.12, u * 0.12);
    let back = "", front = "";
    if (cos === "lawyer") {
      coatW = Math.max(u * 0.42, Math.min(w * 0.62, u * 0.54));
      const c0 = u * 0.08, c1 = h / 2 + u * 0.03, r = u * 0.08, cw = coatW, nw = u * 0.075, vt = c0 + u * 0.19;
      coatBottom = c1;
      const coat = `M${f1(-nw)} ${f1(c0)} L${f1(-cw / 2 + r)} ${f1(c0 + J(2))} Q${f1(-cw / 2)} ${f1(c0)} ${f1(-cw / 2)} ${f1(c0 + r)}
        L${f1(-cw * 0.54)} ${f1(c1)} L${f1(cw * 0.54)} ${f1(c1 + J(2))} L${f1(cw / 2)} ${f1(c0 + r)} Q${f1(cw / 2)} ${f1(c0)} ${f1(cw / 2 - r)} ${f1(c0 + J(2))}
        L${f1(nw)} ${f1(c0)} L0 ${f1(vt)} Z`;
      const bw = u * 0.05, b0 = vt - u * 0.035, b1 = vt + u * 0.12;
      const band = (side) => `<polygon points="${f1(side * u * 0.006)},${f1(b0)} ${f1(side * (u * 0.006 + bw))},${f1(b0)} ${f1(side * (u * 0.018 + bw * 1.18))},${f1(b1)} ${f1(side * u * 0.016)},${f1(b1 + J(2))}"
        fill="var(--paper)" stroke="var(--ink)" stroke-width="${f1(seam * 0.8)}" stroke-linejoin="round"/>`;
      const sx = cw * 0.44;
      const arms = sleeve([[-s * sx, c0 + u * 0.1], [-s * (sx + u * 0.08), c0 + u * 0.24], [-s * (sx + u * 0.1), c0 + u * 0.36]]) +
        // the objection arm: raised hand
        sleeve([[s * sx, c0 + u * 0.1], [s * (sx + u * 0.13), c0 + u * 0.02], [s * (sx + u * 0.17), c0 - u * 0.17]]);
      front = `<path d="M${f1(-nw)} ${f1(c0)} L${f1(nw)} ${f1(c0)} L0 ${f1(vt)} Z" fill="var(--paper)"/>
        <path d="${coat}" fill="var(--ink)" stroke="var(--paper)" stroke-width="${f1(seam)}" stroke-linejoin="round"/>
        <path d="${line([[-nw - u * 0.06, c0 + seam], [-u * 0.05, vt + u * 0.07]], 1)} M${f1(nw + u * 0.06)} ${f1(c0 + seam)} L${f1(u * 0.05)} ${f1(vt + u * 0.07)}"
          fill="none" stroke="var(--paper)" stroke-width="${f1(seam)}" stroke-linecap="round" opacity=".8"/>
        ${band(-1)}${band(1)}
        <circle cx="0" cy="${f1(vt + u * 0.2)}" r="${f1(u * 0.016)}" fill="var(--paper)"/>
        ${c1 - vt > u * 0.32 ? `<circle cx="0" cy="${f1(vt + u * 0.29)}" r="${f1(u * 0.016)}" fill="var(--paper)"/>` : ""}` + arms;
    } else if (cos === "crown") {
      const cw = Math.max(u * 0.4, Math.min(w * 0.6, u * 0.5)), ch = u * 0.24, by = topY + u * 0.05;
      const tip = (x, y) => `<circle cx="${f1(x)}" cy="${f1(y)}" r="${f1(u * 0.026)}" fill="var(--haldi)" stroke="var(--ink)" stroke-width="${f1(seam)}"/>`;
      front = `<g transform="translate(${f1(bs * u * 0.04)} ${f1(by)}) rotate(${f1(-bs * 9 + J(2))})">
        <path d="M${f1(-cw / 2)} 0 L${f1(-cw / 2 - u * 0.02)} ${f1(-ch)} L${f1(-cw / 4)} ${f1(-ch * 0.45)} L${f1(J(3))} ${f1(-ch * 1.08)} L${f1(cw / 4)} ${f1(-ch * 0.45)} L${f1(cw / 2 + u * 0.02)} ${f1(-ch)} L${f1(cw / 2)} 0 Z"
          fill="var(--haldi)" stroke="var(--ink)" stroke-width="${f1(seam * 1.5)}" stroke-linejoin="round"/>
        <path d="${line([[-cw / 2 + seam, -ch * 0.2], [cw / 2 - seam, -ch * 0.2]], 1.5)}" fill="none" stroke="var(--ink)" stroke-width="${f1(seam)}" stroke-linecap="round"/>
        ${tip(-cw / 2 - u * 0.02, -ch)}${tip(0, -ch * 1.08)}${tip(cw / 2 + u * 0.02, -ch)}</g>`;
      back = restArm(-1) + restArm(1);
    } else if (cos === "detective") {
      const bw = Math.max(u * 0.56, Math.min(w * 0.8, u * 0.7)), by = topY + u * 0.08, hw = bw * 0.32, hh = u * 0.22;
      front = `<g transform="translate(${f1(-s * u * 0.03)} ${f1(by)}) rotate(${f1(s * 7 + J(2))})">
        <path d="M${f1(-hw)} 0 L${f1(-hw * 0.86)} ${f1(-hh)} Q${f1(-hw * 0.3)} ${f1(-hh * 0.9)} 0 ${f1(-hh * 0.72)} Q${f1(hw * 0.3)} ${f1(-hh * 0.9)} ${f1(hw * 0.86)} ${f1(-hh)} L${f1(hw)} 0 Z"
          fill="var(--ink)" stroke="var(--paper)" stroke-width="${f1(seam)}" stroke-linejoin="round"/>
        <path d="M${f1(-hw * 0.98)} ${f1(-u * 0.012)} L${f1(hw * 0.98)} ${f1(-u * 0.012)} L${f1(hw * 0.95)} ${f1(-u * 0.065)} L${f1(-hw * 0.95)} ${f1(-u * 0.065)} Z" fill="var(--red)"/>
        <path d="M${f1(-bw / 2)} ${f1(u * 0.012)} Q0 ${f1(-u * 0.05)} ${f1(bw / 2)} ${f1(u * 0.012)} Q0 ${f1(u * 0.05)} ${f1(-bw / 2)} ${f1(u * 0.012)} Z"
          fill="var(--ink)" stroke="var(--paper)" stroke-width="${f1(seam)}" stroke-linejoin="round"/></g>`;
      const [x0, ay0] = sideP(s), lr = u * 0.135;
      const hx = s * Math.max(Math.abs(x0) + u * 0.2, w / 2 + u * 0.06), hy = armY + u * 0.04;
      const lx = s * Math.max(Math.abs(hx) + u * 0.07, w / 2 + lr + u * 0.04), ly = hy - u * 0.24;
      const ang = Math.atan2(hy - ly, hx - lx), ex2 = lx + Math.cos(ang) * lr, ey2 = ly + Math.sin(ang) * lr;
      back = restArm(-s) + limb([[x0, ay0], [x0 + s * u * 0.09, ay0 + u * 0.06], [hx, hy]], false);
      front += `<path d="M${f1(hx - Math.cos(ang) * u * 0.02)} ${f1(hy - Math.sin(ang) * u * 0.02 + u * 0.04)} L${f1(ex2)} ${f1(ey2)}" class="gc-limb" stroke="var(--ink)" stroke-width="${f1(lw * 1.5)}"/>
        ${glove([hx, hy])}
        <circle cx="${f1(lx)}" cy="${f1(ly)}" r="${f1(lr)}" fill="var(--paper)" fill-opacity=".55" stroke="var(--ink)" stroke-width="${f1(lw * 0.95)}"/>
        <path d="M${f1(lx - lr * 0.55)} ${f1(ly - lr * 0.15)} A${f1(lr * 0.6)} ${f1(lr * 0.6)} 0 0 1 ${f1(lx - lr * 0.1)} ${f1(ly - lr * 0.58)}" fill="none" stroke="var(--paper)" stroke-width="${f1(seam * 1.4)}" stroke-linecap="round"/>`;
    } else if (p.arms !== false) {
      back = restArm(-1) + restArm(1);
    }
    const legSvg = p.legs === false ? "" : legs();

    // ---- assemble (svg viewBox centred on the glyph's ink centre, so transform-origin = the glyph)
    const W = Math.ceil(w + 1.6 * u), H = Math.ceil(h + 1.6 * u);
    const tilt = CH.tilt(rng, 2);
    el.innerHTML = `
      ${p.line ? `<div class="gc-slip torn-wrap" style="top:${+p.lineY}px"><div class="gc-slip-in paper-torn t-body">
        <span class="gc-line">${CH.esc(p.line)}</span><span class="gc-tiny"></span></div></div>` : ""}
      <div class="gc-wrap" style="left:${f1(X - W / 2)}px; top:${f1(Y - H / 2)}px; width:${W}px; height:${H}px">
        <svg class="gc-svg" viewBox="${f1(-W / 2)} ${f1(-H / 2)} ${W} ${H}" width="${W}" height="${H}" style="--gc:${tone}">
          <g class="gc-cos">${legSvg}</g>
          <text class="gc-glyph" x="${f1(tx)}" y="${f1(ty)}" font-size="${f1(fs)}" fill="${tone}">${CH.esc(glyph)}</text>
          <g class="gc-cos gc-front">${back}${front}</g>
          ${eyes}
        </svg>
      </div>
      ${p.bubble ? `<div class="gc-bubble t-body ${bs > 0 ? "r" : "l"}">${CH.rich(p.bubble)}</div>` : ""}`;

    // bubble beside the head, on bubbleSide, kept inside x 60–940
    const bub = el.querySelector(".gc-bubble");
    if (bub) {
      // beside the glyph's top corner on bubbleSide; above the glyph when the side has < 300 px of room
      const hat = (cos === "crown" || cos === "detective") ? u * 0.3 : 0;
      const sideRoom = bs > 0 ? 940 - (X + w / 2) : (X - w / 2) - 60;
      let edgeX, bottom;
      if (sideRoom >= 300) { edgeX = X + bs * (w / 2 - u * 0.04); bottom = 1920 - (Y - h / 2 + u * 0.16); }
      else { edgeX = X + bs * w * 0.05; bottom = 1920 - (Y - h / 2 - u * 0.08 - hat); }
      if (bs > 0) Object.assign(bub.style, { left: `${f1(edgeX)}px`, maxWidth: `${f1(Math.min(+p.bubbleWidth || 520, 940 - edgeX))}px` });
      else Object.assign(bub.style, { right: `${f1(1080 - edgeX)}px`, maxWidth: `${f1(Math.min(+p.bubbleWidth || 520, edgeX - 60))}px` });
      bub.style.bottom = `${f1(bottom)}px`;
    }

    const wrap = el.querySelector(".gc-wrap");
    const cosEls = [...el.querySelectorAll(".gc-cos")];
    let landed = t + 7 * CH.F;
    const slip = el.querySelector(".gc-slip");
    if (p.anim === "grow" && slip) {
      // tiny glyph sits after the line like a footnote mark, then grows into the character
      const tiny = slip.querySelector(".gc-tiny"), inner = slip.querySelector(".gc-slip-in");
      const tfs = 92, th = tfs * (A + D), tw = tfs * (L + R);
      tiny.style.width = `${f1(tw)}px`; tiny.style.height = `${f1(th)}px`;
      tiny.innerHTML = `<svg viewBox="${f1(-tw / 2)} ${f1(-th / 2)} ${f1(tw)} ${f1(th)}" width="${f1(tw)}" height="${f1(th)}" style="overflow:visible">
        <text class="gc-glyph" x="${f1(-tw / 2 + L * tfs)}" y="${f1(-th / 2 + A * tfs)}" font-size="${tfs}" fill="${tone}">${CH.esc(glyph)}</text></svg>`;
      const st = CH.tilt(rng, 1.6);
      slip.style.transform = `rotate(${f1(st)}deg)`;
      // tiny centre in frame px (slip rotates about its own centre)
      const sl = slip.offsetLeft, stp = slip.offsetTop, sw = slip.offsetWidth, sh = slip.offsetHeight;
      const lx0 = inner.offsetLeft + tiny.offsetLeft + tw / 2 - sw / 2, ly0 = inner.offsetTop + tiny.offsetTop + th / 2 - sh / 2;
      const a = st * Math.PI / 180;
      const gx = sl + sw / 2 + lx0 * Math.cos(a) - ly0 * Math.sin(a), gy = stp + sh / 2 + lx0 * Math.sin(a) + ly0 * Math.cos(a);
      CH.toss(tl, slip, t, st);
      const g0 = t + (+p.growAt || 0.45);
      tl.fromTo(wrap, { opacity: 0 }, { opacity: 1, duration: CH.F, ease: "none" }, g0 - CH.F);
      tl.fromTo(tiny, { opacity: 1 }, { opacity: 0, duration: CH.F, ease: "none" }, g0 - CH.F);
      tl.fromTo(wrap, { x: gx - X, y: gy - Y, scale: th / h, rotation: 0 },
        { x: 0, y: 0, scale: 1, rotation: tilt, duration: 9 * CH.F, ease: "power3.out" }, g0 - CH.F);
      tl.fromTo(cosEls, { opacity: 0, scale: 0.8, transformOrigin: "50% 50%" },
        { opacity: 1, scale: 1, duration: 5 * CH.F, ease: "power3.out" }, g0 + 7 * CH.F);
      landed = g0 + 10 * CH.F;
    } else {
      if (slip) { const st = CH.tilt(rng, 1.6); slip.style.transform = `rotate(${f1(st)}deg)`; CH.toss(tl, slip, t, st); }
      CH.toss(tl, wrap, t, tilt, { y: 120 });
    }
    if (bub) CH.pop(tl, bub, landed, { from: 0.8, y: 20, rot: bs * 1.2, rotTo: bs * 1.2 });
    // deadpan blinks
    const eyeEls = [...el.querySelectorAll(".gc-eye")];
    for (let b = landed + 0.7; b < t + d - 0.25; b += 2.3) {
      tl.fromTo(eyeEls, { scaleY: 1 }, { scaleY: 0.12, duration: CH.F, transformOrigin: "50% 50%", ease: "none" }, b);
      tl.to(eyeEls, { scaleY: 1, duration: CH.F, ease: "none" }, b + 3 * CH.F);
    }
  },
});
