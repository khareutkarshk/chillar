/* Chillar — healthy, round ₹1 coin mascot (dent styles kept only as opt-in variants). Single source of truth for every expression.
 *
 *   Chillar.svg({ expr: "side-eye", id: "c1", size: 400 })  -> SVG string
 *   Chillar.EXPRESSIONS                                     -> list of expression names
 *
 * Layers (each a <g> with id "<id>-<layer>" and class "<layer>"):
 *   legs (leg-l, leg-r) · arms (arm-l, arm-r) · body (shadow, coin, rim, ticks, shine, dent)
 *   eyes (eye-l, eye-r: white, pupil, lid) · bags · brows · mouth · extras (sweat, tears, ...)
 * Palette only: haldi #FFC83D, ink #151515, paper #FAF9F6, pencil #6B675E, green #1E9E58.
 * Rule: Chillar never fully smiles.
 */
(function (g) {
  const C = { haldi: "#FFC83D", ink: "#151515", card: "#FAF9F6", pencil: "#6B675E", green: "#1E9E58", red: "#D9302C" };
  const CX = 200, CY = 190, R = 130;
  const EYE = { l: [158, 175], r: [242, 175] }, ERX = 30, ERY = 25;

  // Dented coin outline: big arc from B round to A, then a concave notch back to B.
  // A shallow, wide push-in (a dent, not a bite).
  // Dent styles: "notch" (bite-like cut), "flat" (rim knocked flat), "crater" (round outline,
  // pushed-in mark on the face), "none".
  const CIRCLE = (r) => `M${CX - r} ${CY} A${r} ${r} 0 1 1 ${CX + r} ${CY} A${r} ${r} 0 1 1 ${CX - r} ${CY} Z`;
  const DENTS = {
    notch: { body: "M326.1 158.6 A130 130 0 1 1 261.0 75.2 Q270.0 135.4 326.1 158.6 Z",
             rim: "M306.7 163.4 A110 110 0 1 1 251.6 92.9 Q258.7 144.2 306.7 163.4 Z", skip: [292, 352],
             marks: `<line x1="270" y1="116" x2="259" y2="121"/><line x1="290" y1="138" x2="281" y2="148"/>` },
    flat:  { body: "M322.2 145.5 A130 130 0 1 1 274.6 83.5 L293.7 118.2 Z",
             rim: "M303.4 152.4 A110 110 0 1 1 263.1 99.9 L280.1 128.6 Z", skip: [298, 344],
             marks: `<line x1="286" y1="112" x2="276" y2="104"/><line x1="296" y1="128" x2="286" y2="122"/>` },
    crater: { body: CIRCLE(130), rim: CIRCLE(110), skip: [400, 400],
             marks: `<path d="M240 100 Q268 106 282 134" fill="none" stroke-width="5"/>
                     <path d="M244 112 Q264 118 272 136" fill="none" stroke="${C.card}" stroke-width="5"/>
                     <line x1="268" y1="96" x2="276" y2="88"/><line x1="290" y1="140" x2="300" y2="146"/>` },
    none:  { body: CIRCLE(130), rim: CIRCLE(110), skip: [400, 400], marks: "" },
  };

  const DEFAULT = {
    lid: { l: [0.5, 0.5], r: [0.5, 0.5] },       // [outer, inner] fraction of eye covered
    pupil: { dx: 0, dy: 7, r: 11 },
    brows: { l: [-36, -40], r: [-40, -36] },     // [x-left end, x-right end] y offsets from eye centre
    mouth: "M176 250 Q200 254 224 250",
    mouthFill: false,
    arms: {
      l: "M78 205 L52 250 L56 290", hl: [56, 298],
      r: "M322 205 L348 250 L344 290", hr: [344, 298],
    },
    extras: [],
    bags: false,
  };

  const EXPR = {
    "neutral-tired": {},
    "shocked": {
      lid: { l: [0, 0], r: [0, 0] },
      pupil: { dx: 0, dy: 0, r: 7 },
      brows: { l: [-58, -62], r: [-62, -58] },
      mouth: "M200 238 m-15 0 a15 20 0 1 0 30 0 a15 20 0 1 0 -30 0", mouthFill: true,
      arms: { l: "M78 190 L40 150 L52 104", hl: [54, 96], r: "M322 190 L360 150 L348 104", hr: [346, 96] },
      extras: ["impact"], bags: false,
    },
    "side-eye": {
      lid: { l: [0.58, 0.52], r: [0.52, 0.58] },
      pupil: { dx: 15, dy: 5, r: 11 },
      brows: { l: [-38, -38], r: [-50, -44] },
      mouth: "M184 252 Q204 251 222 247",
      arms: { l: "M78 205 L52 250 L56 290", hl: [56, 298], r: "M322 212 L360 240 L326 266", hr: [320, 268] },
    },
    "smug": {
      lid: { l: [0.62, 0.55], r: [0.55, 0.62] },
      pupil: { dx: -6, dy: 4, r: 11 },
      brows: { l: [-44, -38], r: [-38, -52] },
      mouth: "M180 253 Q200 255 213 250 Q221 246 226 240",
      arms: { l: "M78 214 L40 242 L74 268", hl: [80, 270], r: "M322 214 L360 242 L326 268", hr: [320, 270] },
    },
    "crying": {
      lid: { l: [0.55, 0.42], r: [0.42, 0.55] },
      pupil: { dx: 0, dy: 6, r: 11 },
      brows: { l: [-32, -50], r: [-50, -32] },
      mouth: "M174 260 Q187 248 200 257 Q213 248 226 260",
      arms: { l: "M80 214 L66 262 L72 306", hl: [72, 312], r: "M320 214 L334 262 L328 306", hr: [328, 312] },
      extras: ["tears"],
    },
    "facepalm": {
      lid: { l: [0.9, 0.9], r: [0.9, 0.9] },
      pupil: { dx: 0, dy: 10, r: 11 },
      brows: { l: [-34, -42], r: [-42, -34] },
      mouth: "M182 254 L220 254",
      arms: { l: "M78 205 L52 250 L56 290", hl: [56, 298], r: "M318 222 L352 292 L262 196", hr: [240, 168], palm: true },
      extras: ["sweat"],
    },
    "thinking": {
      lid: { l: [0.38, 0.38], r: [0.38, 0.38] },
      pupil: { dx: 11, dy: -10, r: 11 },
      brows: { l: [-38, -40], r: [-52, -46] },
      mouth: "M180 254 Q192 250 206 253",
      arms: { l: "M78 205 L52 250 L56 290", hl: [56, 298], r: "M318 222 L318 306 L248 300", hr: [242, 298] },
      extras: ["thought"],
    },
    "counting-money": {
      lid: { l: [0.6, 0.6], r: [0.6, 0.6] },
      pupil: { dx: 0, dy: 13, r: 11 },
      brows: { l: [-40, -42], r: [-42, -40] },
      mouth: "M186 252 L214 252",
      arms: { l: "M78 214 L104 286 L150 300", hl: [156, 300], r: "M322 214 L296 286 L250 300", hr: [244, 300] },
      extras: ["notes"],
    },
  };

  const merge = (a, b) => {
    const o = { ...a };
    for (const k in b) o[k] = b[k] && typeof b[k] === "object" && !Array.isArray(b[k]) ? { ...a[k], ...b[k] } : b[k];
    return o;
  };

  function eye(side, p, id) {
    const [ex, ey] = EYE[side];
    const [fo, fi] = p.lid[side];           // outer / inner corner coverage
    const top = ey - ERY, h = 2 * ERY;
    const yLeft = top + h * (side === "l" ? fo : fi);
    const yRight = top + h * (side === "l" ? fi : fo);
    const pdx = side === "l" ? p.pupil.dx : p.pupil.dx;
    const clip = `${id}-clip-${side}`;
    return `
    <g id="${id}-eye-${side}" class="eye eye-${side}">
      <clipPath id="${clip}"><ellipse cx="${ex}" cy="${ey}" rx="${ERX}" ry="${ERY}"/></clipPath>
      <ellipse class="white" cx="${ex}" cy="${ey}" rx="${ERX}" ry="${ERY}" fill="${C.card}"/>
      <circle class="pupil" cx="${ex + pdx}" cy="${ey + p.pupil.dy}" r="${p.pupil.r}" fill="${C.ink}"/>
      <g class="lid" clip-path="url(#${clip})">
        <polygon points="${ex - 40},${top - 6} ${ex + 40},${top - 6} ${ex + 40},${yRight} ${ex - 40},${yLeft}" fill="${C.haldi}"/>
        <line x1="${ex - 40}" y1="${yLeft}" x2="${ex + 40}" y2="${yRight}" stroke="${C.ink}" stroke-width="7"/>
      </g>
      <ellipse class="outline" cx="${ex}" cy="${ey}" rx="${ERX}" ry="${ERY}" fill="none" stroke="${C.ink}" stroke-width="6"/>
    </g>`;
  }

  function brow(side, p) {
    const [ex, ey] = EYE[side];
    const [y1, y2] = p.brows[side];
    return `<path class="brow brow-${side}" d="M${ex - 30} ${ey + y1} L${ex + 30} ${ey + y2}" stroke="${C.ink}" stroke-width="10" stroke-linecap="round" fill="none"/>`;
  }

  // big mitten palm with finger creases (facepalm)
  const palm = ([x, y]) => `<g transform="translate(${x} ${y}) rotate(-24)">
      <ellipse cx="0" cy="0" rx="46" ry="31" fill="${C.haldi}" stroke-width="7"/>
      <g stroke-width="5"><line x1="-30" y1="-10" x2="-4" y2="-10"/><line x1="-30" y1="2" x2="-2" y2="2"/><line x1="-28" y1="14" x2="-6" y2="14"/></g>
    </g>`;

  const EXTRAS = {
    sweat: (id) => `<g id="${id}-sweat" class="sweat"><path d="M108 96 Q94 122 108 132 Q122 122 108 96 Z" fill="${C.card}" stroke="${C.ink}" stroke-width="5" stroke-linejoin="round"/></g>`,
    tears: (id) => `<g id="${id}-tears" class="tears">
        ${[EYE.l, EYE.r].map(([ex, ey], i) => {
          const x = ex + (i ? 14 : -14);
          return `<path d="M${x - 7} ${ey + 22} L${x - 9} ${ey + 76} Q${x} ${ey + 90} ${x + 9} ${ey + 76} L${x + 7} ${ey + 22} Z" fill="${C.card}" stroke="${C.ink}" stroke-width="5" stroke-linejoin="round"/>`;
        }).join("")}
      </g>`,
    impact: (id) => `<g id="${id}-impact" class="impact" stroke="${C.ink}" stroke-width="8" stroke-linecap="round">
        <line x1="200" y1="36" x2="200" y2="12"/><line x1="146" y1="46" x2="132" y2="26"/><line x1="254" y1="46" x2="268" y2="26"/></g>`,
    thought: (id) => `<g id="${id}-thought" class="thought" fill="${C.card}" stroke="${C.ink}" stroke-width="5">
        <circle cx="330" cy="70" r="7"/><circle cx="352" cy="46" r="10"/><circle cx="378" cy="20" r="13"/></g>`,
    notes: (id) => `<g id="${id}-notes" class="notes" stroke="${C.ink}" stroke-width="5" stroke-linejoin="round">
        ${[[-8, -6], [4, 2], [-2, 10]].map(([rot, dy], i) => `
        <g transform="translate(200 ${300 + dy}) rotate(${rot})">
          <rect x="-62" y="-26" width="124" height="52" rx="4" fill="${C.green}"/>
          <rect x="-50" y="-15" width="100" height="30" rx="2" fill="none" stroke="${C.ink}" stroke-width="3"/>
          <circle cx="0" cy="0" r="9" fill="${C.card}" stroke-width="3"/>
        </g>`).join("")}
      </g>`,
  };

  function svg(opts = {}) {
    const expr = opts.expr || "neutral-tired";
    const id = opts.id || "chillar";
    const size = opts.size || 400;
    const p = merge(DEFAULT, EXPR[expr] || {});
    const D = DENTS[opts.dent || "none"], BODY = D.body, RIM = D.rim;
    const arms = p.arms;
    const ticks = [];
    for (let a = 0; a < 360; a += 12) {
      if (a > D.skip[0] && a < D.skip[1]) continue; // skip around the dent
      const t = (a * Math.PI) / 180;
      ticks.push(`<line x1="${(CX + 117 * Math.cos(t)).toFixed(1)}" y1="${(CY + 117 * Math.sin(t)).toFixed(1)}" x2="${(CX + 124 * Math.cos(t)).toFixed(1)}" y2="${(CY + 124 * Math.sin(t)).toFixed(1)}"/>`);
    }
    const handFront = expr === "facepalm" || expr === "thinking" || expr === "counting-money";
    const armsSvg = `
    <g id="${id}-arms" class="arms" stroke="${C.ink}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round" fill="none">
      <g id="${id}-arm-l" class="arm arm-l"><path d="${arms.l}"/><circle cx="${arms.hl[0]}" cy="${arms.hl[1]}" r="13" fill="${C.haldi}" stroke-width="5"/></g>
      <g id="${id}-arm-r" class="arm arm-r"><path d="${arms.r}"/>${arms.palm ? palm(arms.hr) : `<circle cx="${arms.hr[0]}" cy="${arms.hr[1]}" r="13" fill="${C.haldi}" stroke-width="5"/>`}</g>
    </g>`;
    const extras = p.extras.filter((x) => x !== "notes").map((x) => EXTRAS[x](id)).join("");
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 440" width="${size}" height="${(size * 1.1).toFixed(0)}" class="chillar chillar--${expr}" data-expr="${expr}" role="img" aria-label="Chillar ${expr}">
  <g id="${id}-figure" class="figure">
    <g id="${id}-legs" class="legs" stroke="${C.ink}" stroke-width="9" stroke-linecap="round" fill="${C.ink}">
      <g id="${id}-leg-l" class="leg leg-l"><line x1="172" y1="306" x2="162" y2="390" fill="none"/><ellipse cx="150" cy="397" rx="21" ry="10" stroke-width="0"/></g>
      <g id="${id}-leg-r" class="leg leg-r"><line x1="228" y1="306" x2="238" y2="390" fill="none"/><ellipse cx="250" cy="397" rx="21" ry="10" stroke-width="0"/></g>
    </g>
    ${handFront ? "" : armsSvg}
    <g id="${id}-body" class="body">
      <path class="shadow" d="${BODY}" transform="translate(9 9)" fill="${C.ink}"/><!-- taste-skill-ignore: drawn illustration -->
      <path class="coin" d="${BODY}" fill="${C.haldi}" stroke="${C.ink}" stroke-width="10" stroke-linejoin="round"/>
      <g class="ticks" stroke="${C.ink}" stroke-width="3" stroke-linecap="round">${ticks.join("")}</g>
      <path class="rim" d="${RIM}" fill="none" stroke="${C.ink}" stroke-width="4" stroke-linejoin="round"/>
      <path class="shine" d="M110.7 157.5 A95 95 0 0 1 152.5 107.7" fill="none" stroke="${C.card}" stroke-width="9" stroke-linecap="round"/>
      <g class="dent" stroke="${C.ink}" stroke-width="4" stroke-linecap="round">${D.marks}</g>
    </g>
    <g id="${id}-face" class="face">
      <g id="${id}-eyes" class="eyes">${eye("l", p, id)}${eye("r", p, id)}</g>
      ${p.bags ? `<g id="${id}-bags" class="bags" stroke="${C.pencil}" stroke-width="4" stroke-linecap="round" fill="none">
        <path d="M${EYE.l[0] - 18} ${EYE.l[1] + 34} Q${EYE.l[0]} ${EYE.l[1] + 41} ${EYE.l[0] + 18} ${EYE.l[1] + 34}"/>
        <path d="M${EYE.r[0] - 18} ${EYE.r[1] + 34} Q${EYE.r[0]} ${EYE.r[1] + 41} ${EYE.r[0] + 18} ${EYE.r[1] + 34}"/></g>` : ""}
      <g id="${id}-brows" class="brows">${brow("l", p)}${brow("r", p)}</g>
      <g id="${id}-mouth" class="mouth"><path d="${p.mouth}" ${p.mouthFill ? `fill="${C.ink}"` : `fill="none" stroke="${C.ink}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"`}/></g>
    </g>
    ${p.extras.includes("notes") ? EXTRAS.notes(id) : ""}
    ${handFront ? armsSvg : ""}
    <g id="${id}-extras" class="extras">${extras}</g>
  </g>
</svg>`;
  }

  const api = { svg, EXPRESSIONS: Object.keys(EXPR), DENTS: Object.keys(DENTS), COLORS: C };
  g.Chillar = api;
  if (typeof module !== "undefined") module.exports = api;
})(typeof window !== "undefined" ? window : globalThis);
