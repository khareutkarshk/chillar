/* photo-frame — a framed photo of a family character + a speech bubble from someone off-screen.
 * The portrait is drawn, not fetched: a paper face with an ink outline, Chillar's half-closed deadpan
 * eyes and a costume per character (didi, mummy, papa …). Hair shape, outfit colour and accessories
 * are seeded, so every reel's didi is her own didi and renders stay deterministic. */
const PF_WHO = {                                                   // caption word -> character
  didi: "didi", sister: "didi", behen: "didi", mummy: "mummy", mom: "mummy", maa: "mummy", mumma: "mummy",
  papa: "papa", dad: "papa", pitaji: "papa", chacha: "chacha", mama: "chacha", tauji: "chacha",
  dadi: "dadi", nani: "dadi", bhai: "bhai", bhaiya: "bhai", brother: "bhai", mausi: "mausi", bua: "mausi",
  chachi: "mausi", aunty: "mausi", uncle: "uncle", "sharma ji": "uncle", hr: "hr", boss: "hr", manager: "hr",
  dost: "dost", friend: "dost", yaar: "dost",
};
// per character: hair options, outfit options, default expression and what they wear
const PF_CAST = {
  didi:   { hair: ["long", "plait"], cloth: ["--green", "--red", "--note2000"], expr: "smug", bindi: 3.5, earrings: true, wear: "dupatta" },
  mummy:  { hair: ["bun"], cloth: ["--red", "--green"], expr: "side-eye", bindi: 6, sindoor: true, earrings: true, wear: "saree" },
  papa:   { hair: ["short"], cloth: ["--note50", "--note20", "--paper"], expr: "deadpan", grey: true, specs: "rect", tache: "neat", wear: "shirt" },
  chacha: { hair: ["bald"], cloth: ["--haldi", "--green"], expr: "smug", specs: "round", tache: "thick", wear: "kurta" },
  dadi:   { hair: ["bun"], hairTone: "--paper", cloth: ["--green", "--note10"], expr: "deadpan", bindi: 5, specs: "round", wrinkles: true, wear: "saree" },
  bhai:   { hair: ["spiky", "messy"], cloth: ["--red", "--green", "--ink"], expr: "side-eye", wear: "hoodie" },
  mausi:  { hair: ["curly"], cloth: ["--red", "--note2000", "--haldi"], expr: "smug", bindi: 6, earrings: true, wear: "saree" },
  uncle:  { hair: ["short"], cloth: ["--green", "--note500"], expr: "proud", tache: "neat", wear: "shirt" },
  hr:     { hair: ["short", "long"], cloth: ["--ink"], expr: "deadpan", specs: "rect", wear: "blazer" },
  dost:   { hair: ["cap"], cloth: ["--green", "--note50", "--red"], expr: "side-eye", wear: "tee" },
};

CH.define("photo-frame", {
  build({ el, p, t, d, tl, id, rng }) {
    const tilt = CH.tilt(rng), side = p.side === "right" ? "right" : "left";
    const fw = Math.min(860, +p.frameWidth || 620);
    const pick = (a) => a[Math.floor(rng() * a.length) % a.length];
    const J = (v) => (rng() * 2 - 1) * v;
    const f1 = (n) => n.toFixed(1);
    const cap = String(p.caption || "").toLowerCase();
    const key = p.who && PF_CAST[p.who] ? p.who
      : PF_WHO[Object.keys(PF_WHO).find((k) => new RegExp(`(^|[^a-z])${k}([^a-z]|$)`).test(cap))] || pick(["didi", "papa", "dost"]);
    const c = PF_CAST[key];
    const expr = p.expr || c.expr;
    const hair = pick(c.hair), cloth = `var(${pick(c.cloth)})`;
    const hairFill = `var(${c.hairTone || "--ink"})`;
    const bg = `color-mix(in srgb, var(--paper) 52%, var(${pick(["--note10", "--note20", "--note50", "--note2000"])}))`;
    const SW = 5, ink = "var(--ink)", paper = "var(--paper)";
    const st = (w = SW) => `stroke="${ink}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
    const look = expr === "side-eye" ? (side === "right" ? 1 : -1) : 0;   // side-eye glances toward the bubble's tail

    // ---- body (back to front: back hair, clothes, neck, ears, face, front hair, features, accessories)
    let back = "", body = "", over = "", head = "", top = "", feat = "", acc = "";
    const hx = 200 + J(4), hy = 132, rx = 56, ry = 63;
    body = `<path d="M84 304 Q92 226 162 212 L238 212 Q308 226 316 304 Z" fill="${cloth}" ${st()}/>`;
    const neck = `<path d="M182 186 L182 216 Q200 226 218 216 L218 186 Z" fill="${paper}" ${st()}/>`;
    const ears = `<ellipse cx="${f1(hx - rx + 2)}" cy="140" rx="10" ry="15" fill="${paper}" ${st()}/><ellipse cx="${f1(hx + rx - 2)}" cy="140" rx="10" ry="15" fill="${paper}" ${st()}/>`;
    const face = `<ellipse cx="${f1(hx)}" cy="${hy}" rx="${rx}" ry="${ry}" fill="${paper}" ${st()}/>`;

    // hair
    const cap0 = (part) => `M${f1(hx - 57)} 132 Q${f1(hx - 60)} 64 ${f1(hx)} 64 Q${f1(hx + 60)} 64 ${f1(hx + 57)} 132 ` +
      `Q${f1(hx + 50)} 92 ${f1(hx + part)} 86 Q${f1(hx - 40)} 90 ${f1(hx - 57)} 132 Z`;
    if (hair === "long") {
      back = `<path d="M${f1(hx - 66)} 120 Q${f1(hx - 74)} 52 ${f1(hx)} 54 Q${f1(hx + 74)} 52 ${f1(hx + 66)} 120 L${f1(hx + 74)} 246 Q${f1(hx)} 262 ${f1(hx - 74)} 246 Z" fill="${hairFill}" ${st()}/>`;
      top = `<path d="${cap0(J(10) - 18)}" fill="${hairFill}" ${st()}/>`;
    } else if (hair === "plait") {
      const s = rng() < 0.5 ? -1 : 1;
      let beads = "";
      for (let i = 0; i < 5; i++) beads += `<ellipse cx="${f1(hx + s * (52 + i * 4))}" cy="${f1(196 + i * 22)}" rx="15" ry="13" fill="${hairFill}" ${st(4)}/>`;
      back = `<circle cx="${f1(hx)}" cy="104" r="62" fill="${hairFill}" ${st()}/>`;
      top = `<path d="${cap0(s * 14)}" fill="${hairFill}" ${st()}/>${beads}<circle cx="${f1(hx + s * 70)}" cy="300" r="6" fill="var(--red)" ${st(3)}/>`;
    } else if (hair === "bun") {
      back = `<circle cx="${f1(hx + J(6))}" cy="66" r="${f1(27 + J(3))}" fill="${hairFill}" ${st()}/>`;
      top = `<path d="${cap0(0)}" fill="${hairFill}" ${st()}/><path d="M${f1(hx)} 66 L${f1(hx)} 87" stroke="${c.sindoor ? "var(--red)" : paper}" stroke-width="${c.sindoor ? 5 : 3}" stroke-linecap="round"/>`;
    } else if (hair === "short") {
      top = `<path d="M${f1(hx - 57)} 124 Q${f1(hx - 60)} 66 ${f1(hx)} 64 Q${f1(hx + 60)} 66 ${f1(hx + 57)} 124 Q${f1(hx + 44)} 92 ${f1(hx + 14)} 96 Q${f1(hx - 12)} 80 ${f1(hx - 40)} 98 Q${f1(hx - 52)} 108 ${f1(hx - 57)} 124 Z" fill="${hairFill}" ${st()}/>` +
        (c.grey ? `<path d="M${f1(hx - 55)} 116 L${f1(hx - 49)} 100 M${f1(hx + 55)} 116 L${f1(hx + 49)} 100" stroke="var(--paper)" stroke-width="4" stroke-linecap="round"/>` : "");
    } else if (hair === "bald") {
      top = `<path d="M${f1(hx - 58)} 142 Q${f1(hx - 62)} 112 ${f1(hx - 44)} 98 L${f1(hx - 38)} 120 Z M${f1(hx + 58)} 142 Q${f1(hx + 62)} 112 ${f1(hx + 44)} 98 L${f1(hx + 38)} 120 Z" fill="${hairFill}" ${st(4)}/>` +
        `<path d="M${f1(hx - 22)} 84 Q${f1(hx - 6)} 76 ${f1(hx + 8)} 80" fill="none" ${st(3.5)}/><path d="M${f1(hx + 18)} 86 Q${f1(hx + 30)} 82 ${f1(hx + 36)} 92" fill="none" stroke="var(--paper)" stroke-width="5" stroke-linecap="round" opacity=".9"/>`;
    } else if (hair === "spiky" || hair === "messy") {
      let d = `M${f1(hx - 58)} 128 `;
      const n = hair === "spiky" ? 7 : 5;
      for (let i = 0; i <= n; i++) {
        const x = hx - 58 + (116 * i) / n, tipY = 50 + J(10) + (hair === "messy" ? 8 : 0);
        d += `L${f1(x - 116 / n / 2)} ${f1(i === 0 ? 92 : tipY)} L${f1(x)} ${f1(i === 0 || i === n ? 100 : 82)} `;
      }
      top = `<path d="${d}Q${f1(hx + 40)} 96 ${f1(hx)} 94 Q${f1(hx - 40)} 96 ${f1(hx - 58)} 128 Z" fill="${hairFill}" ${st()}/>`;
    } else if (hair === "curly") {
      let curls = "";
      for (let i = 0; i < 9; i++) {
        const a = Math.PI * (1.02 + (0.96 * i) / 8);
        curls += `<circle cx="${f1(hx + Math.cos(a) * 60)}" cy="${f1(124 + Math.sin(a) * 66)}" r="${f1(19 + J(3))}" fill="${hairFill}" ${st(4)}/>`;
      }
      back = curls;
      top = `<path d="${cap0(-10)}" fill="${hairFill}"/>`;
    } else if (hair === "cap") {
      top = `<path d="M${f1(hx - 60)} 112 Q${f1(hx - 58)} 58 ${f1(hx)} 56 Q${f1(hx + 58)} 58 ${f1(hx + 60)} 112 Z" fill="var(--red)" ${st()}/>` +
        `<path d="M${f1(hx + 30)} 64 Q${f1(hx + 78)} 70 ${f1(hx + 88)} 92 L${f1(hx + 56)} 96 Z" fill="var(--red)" ${st(4)}/>` +
        `<path d="M${f1(hx - 60)} 112 L${f1(hx + 60)} 112" ${st()}/><circle cx="${f1(hx)}" cy="58" r="5" fill="${ink}"/>`;
    }

    // eyes: Chillar's half-closed lids, in face paper
    const ey = 140 + (hair === "cap" ? 4 : 0), erx = 13, ery = 11;
    const cover = { deadpan: 0.5, "side-eye": 0.56, smug: 0.55, proud: 0.42, shocked: 0.08 }[expr] ?? 0.5;
    const eye = (s) => {
      const ex = hx + s * 22, top0 = ey - ery, tiltLid = expr === "smug" ? s * 2.5 : 0;
      const lidL = top0 + 2 * ery * cover - tiltLid, lidR = top0 + 2 * ery * cover + tiltLid;
      const pr = expr === "shocked" ? 3.2 : 4.6, px = ex + look * 5, py = ey + (expr === "shocked" ? 0 : ery * 0.35);
      const clip = `${id}-pf${s < 0 ? "l" : "r"}`;
      return `<g class="pf-eye"><clipPath id="${clip}"><ellipse cx="${f1(ex)}" cy="${ey}" rx="${erx}" ry="${ery}"/></clipPath>
        <ellipse cx="${f1(ex)}" cy="${ey}" rx="${erx}" ry="${ery}" fill="${paper}"/>
        <circle cx="${f1(px)}" cy="${f1(py)}" r="${pr}" fill="${ink}"/>
        <g clip-path="url(#${clip})"><polygon points="${f1(ex - erx - 3)},${top0 - 3} ${f1(ex + erx + 3)},${top0 - 3} ${f1(ex + erx + 3)},${f1(lidR)} ${f1(ex - erx - 3)},${f1(lidL)}" fill="${paper}"/>
        <line x1="${f1(ex - erx - 3)}" y1="${f1(lidL)}" x2="${f1(ex + erx + 3)}" y2="${f1(lidR)}" ${st(3.5)}/></g>
        <ellipse cx="${f1(ex)}" cy="${ey}" rx="${erx}" ry="${ery}" fill="none" ${st(3)}/></g>`;
    };
    const brow = (s) => {
      const raise = (expr === "side-eye" && s === look) || (expr === "smug" && s > 0) ? -6 : expr === "shocked" ? -8 : 0;
      const bx = hx + s * 22, by = ey - 20 + raise;
      return `<path d="M${f1(bx - 12)} ${f1(by + 2 + J(1))} Q${f1(bx)} ${f1(by - 3)} ${f1(bx + 12)} ${f1(by + 2 + J(1))}" fill="none" ${st(4.5)}/>`;
    };
    const my = 178;
    const mouth = {
      deadpan: `<path d="M${f1(hx - 12)} ${my} L${f1(hx + 12)} ${my + J(1.5)}" fill="none" ${st(4)}/>`,
      "side-eye": `<path d="M${f1(hx - 12)} ${my + 1} Q${f1(hx)} ${my - 1} ${f1(hx + 12)} ${my - 2}" fill="none" ${st(4)}/>`,
      smug: `<path d="M${f1(hx - 12)} ${my} Q${f1(hx + 4)} ${my + 5} ${f1(hx + 15)} ${my - 5}" fill="none" ${st(4)}/>`,
      proud: `<path d="M${f1(hx - 14)} ${my - 2} Q${f1(hx)} ${my + 8} ${f1(hx + 14)} ${my - 2}" fill="none" ${st(4)}/>`,
      shocked: `<ellipse cx="${f1(hx)}" cy="${my + 2}" rx="7" ry="9" fill="${ink}"/>`,
    }[expr] || "";
    feat = brow(-1) + brow(1) + `<g class="pf-eyes">${eye(-1)}${eye(1)}</g>` +
      `<path d="M${f1(hx + 1)} 148 Q${f1(hx - 6)} 160 ${f1(hx + 3)} 163" fill="none" ${st(3.5)}/>` + mouth;
    if (c.tache) feat += c.tache === "thick"
      ? `<path d="M${f1(hx - 26)} 172 Q${f1(hx - 14)} 158 ${f1(hx)} 166 Q${f1(hx + 14)} 158 ${f1(hx + 26)} 172 Q${f1(hx + 12)} 170 ${f1(hx)} 172 Q${f1(hx - 12)} 170 ${f1(hx - 26)} 172 Z" fill="${ink}" ${st(3)}/>`
      : `<path d="M${f1(hx - 17)} 170 Q${f1(hx)} 162 ${f1(hx + 17)} 170 Q${f1(hx)} 168 ${f1(hx - 17)} 170 Z" fill="${ink}" ${st(3)}/>`;
    if (c.bindi) feat += `<circle cx="${f1(hx)}" cy="${f1(ey - 30)}" r="${c.bindi}" fill="var(--red)"/>`;
    if (c.wrinkles) feat += `<path d="M${f1(hx - 42)} 136 l-6 -3 M${f1(hx - 42)} 142 l-7 1 M${f1(hx + 42)} 136 l6 -3 M${f1(hx + 42)} 142 l7 1" ${st(2.5)}/>`;
    if (c.specs === "rect") acc += `<rect x="${f1(hx - 39)}" y="${ey - 13}" width="34" height="25" rx="6" fill="none" ${st(4)}/><rect x="${f1(hx + 5)}" y="${ey - 13}" width="34" height="25" rx="6" fill="none" ${st(4)}/><path d="M${f1(hx - 5)} ${ey - 3} L${f1(hx + 5)} ${ey - 3}" ${st(4)}/>`;
    if (c.specs === "round") acc += `<circle cx="${f1(hx - 22)}" cy="${ey}" r="17" fill="none" ${st(4)}/><circle cx="${f1(hx + 22)}" cy="${ey}" r="17" fill="none" ${st(4)}/><path d="M${f1(hx - 5)} ${ey - 2} L${f1(hx + 5)} ${ey - 2}" ${st(4)}/>`;
    if (c.earrings) for (const s of [-1, 1]) acc += `<path d="M${f1(hx + s * 54)} 154 L${f1(hx + s * 54)} 160" ${st(2.5)}/><circle cx="${f1(hx + s * 54)}" cy="166" r="6" fill="var(--haldi)" ${st(2.5)}/>`;

    // outfit details over the body
    const s2 = rng() < 0.5 ? -1 : 1;
    if (c.wear === "saree") {
      over = `<path d="M${200 + s2 * 116} 304 L${200 + s2 * 54} 216 L${200 + s2 * 18} 222 L${200 - s2 * 60} 304 Z" fill="var(--haldi)" ${st()}/>` +
        `<path d="M${200 + s2 * 98} 304 L${200 + s2 * 46} 228 L${200 + s2 * 26} 232 L${200 - s2 * 36} 304 Z" fill="${cloth}" stroke="none"/>`;
    } else if (c.wear === "dupatta") {
      over = `<path d="M${200 + s2 * 70} 216 Q${200 + s2 * 20} 250 ${200 - s2 * 30} 304 L${200 - s2 * 4} 304 Q${200 + s2 * 36} 260 ${200 + s2 * 92} 224 Z" fill="var(--haldi)" ${st(4)}/>`;
    } else if (c.wear === "shirt") {
      over = `<path d="M182 212 L170 236 L196 226 Z M218 212 L230 236 L204 226 Z" fill="${paper}" ${st(4)}/><path d="M200 228 L200 304" ${st(3)}/><circle cx="200" cy="252" r="3" fill="${ink}"/><circle cx="200" cy="278" r="3" fill="${ink}"/>`;
    } else if (c.wear === "kurta") {
      over = `<path d="M188 214 L188 262 M212 214 L212 262" ${st(3)}/><circle cx="200" cy="236" r="3" fill="${ink}"/><circle cx="200" cy="254" r="3" fill="${ink}"/><path d="M84 304 Q92 240 140 222 L160 304 Z M316 304 Q308 240 260 222 L240 304 Z" fill="${ink}" ${st()}/>`;
    } else if (c.wear === "hoodie") {
      body = `<path d="M150 216 Q200 196 250 216 L242 232 Q200 214 158 232 Z" fill="${cloth}" ${st()}/>` + body;
      over = `<path d="M186 226 L182 266 M214 226 L218 266" stroke="var(--paper)" stroke-width="4" stroke-linecap="round"/><circle cx="182" cy="268" r="4" fill="var(--paper)" ${st(2)}/><circle cx="218" cy="268" r="4" fill="var(--paper)" ${st(2)}/>`;
    } else if (c.wear === "blazer") {
      over = `<path d="M182 212 L200 250 L218 212 Z" fill="${paper}" ${st(4)}/><path d="M194 222 L206 222 L210 280 L200 292 L190 280 Z" fill="var(--red)" ${st(3.5)}/>` +
        `<path d="M164 214 L192 262 L178 270 Z M236 214 L208 262 L222 270 Z" fill="${cloth}" stroke="var(--paper)" stroke-width="3" stroke-linejoin="round"/>` +
        `<path d="M168 216 L150 290 M232 216 L250 290" stroke="var(--paper)" stroke-width="2.5" opacity=".7"/><rect x="${200 + s2 * 52 - 17}" y="262" width="34" height="42" rx="4" fill="${paper}" ${st(3)}/><rect x="${200 + s2 * 52 - 9}" y="270" width="18" height="12" fill="var(--haldi)"/>`;
    } else if (c.wear === "tee") {
      over = `<path d="M176 213 Q200 236 224 213" fill="none" ${st(4)}/>`;
    }
    if (key === "mummy") over += `<path d="M172 214 Q200 262 228 214" fill="none" stroke="${ink}" stroke-width="3" stroke-dasharray="1 7" stroke-linecap="round"/><path d="M200 252 L194 262 L200 272 L206 262 Z" fill="var(--haldi)" ${st(2.5)}/>`;

    const rot = J(3.5);
    const portrait = `<svg class="pf-svg" viewBox="50 36 300 225" preserveAspectRatio="xMidYMid slice">
      <rect x="0" y="0" width="400" height="300" fill="${bg}"/>
      <g transform="rotate(${f1(rot)} 200 300)">${back}${body}${over}${neck}${ears}${face}${top}${feat}${acc}</g></svg>`;

    el.innerHTML = `<div class="zone"><div class="pf-stack">
      <div class="pf-bubble ${side} t-body">${CH.rich(p.speech || "")}${p.speaker ? `<div class="pf-who">${CH.esc(p.speaker)}</div>` : ""}</div>
      <div class="pf-frame paper-obj" style="width:${fw}px; transform: rotate(${tilt.toFixed(2)}deg)"><div class="pf-mat"><div class="pf-photo">${portrait}</div></div>
      ${p.caption ? `<div class="pf-cap">${CH.esc(p.caption)}</div>` : ""}</div></div></div>`;
    CH.toss(tl, el.querySelector(".pf-frame"), t, tilt);
    CH.pop(tl, el.querySelector(".pf-bubble"), t + 4 * CH.F);
    // deadpan blinks, like Chillar
    const eyes = [...el.querySelectorAll(".pf-eye")];
    for (let b = t + 0.9 + rng() * 0.4; b < t + (d || 2) - 0.25; b += 2.4) {
      tl.fromTo(eyes, { scaleY: 1 }, { scaleY: 0.12, duration: CH.F, transformOrigin: "50% 50%", ease: "none" }, b);
      tl.to(eyes, { scaleY: 1, duration: CH.F, ease: "none" }, b + 3 * CH.F);
    }
  },
});
