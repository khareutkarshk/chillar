/* Chillar component runtime — shared helpers + registry. Classic script (no modules).
 *
 * A component is   CH.define("name", { build(ctx) { ... } })
 *   ctx = { el, p, t, d, tl, rng, id, stage, spec }
 *     el    the scene's clip container (absolutely filled 1080x1920)
 *     p     params (already merged with component.json defaults)
 *     t, d  absolute start time + duration (seconds) on the master timeline
 *     tl    the ONE paused master GSAP timeline
 *     rng   seeded random() for this scene (determinism)
 * Layout zones (px): content x 60–940, y 240–1120; captions y 1150–1450.
 * Every tween goes on ctx.tl at absolute time (ctx.t + offset). Use fromTo (seek-safe).
 *
 * Look ("Note Fields"): flat rupee-note colour fields (var(--field) / var(--on-field)), paper
 * objects lying on them at a slight seeded tilt, blue-ballpoint scribbles, stamp-pad red stamps.
 * No borders-as-decoration, no resting shadows, no tracked-caps labels, no bounce on entrances.
 */
(function (g) {
  const F = 1 / 30;                       // one frame
  const registry = {};
  const CH = { F, registry };

  CH.define = (name, def) => { registry[name] = def; };

  // ---------------------------------------------------------------- formatting
  CH.inr = (n, opts = {}) => {
    const d = opts.decimals ?? (Math.abs(n) % 1 ? 2 : 0);
    return Number(n).toLocaleString("en-IN", { minimumFractionDigits: d, maximumFractionDigits: d });
  };
  CH.money = (n, opts = {}) => (opts.prefix ?? "₹") + CH.inr(n, opts) + (opts.suffix ?? "");
  // headline fit: never break inside a word — shrink the font (to `min` × size at most) until the
  // longest word fits the line. Line breaks between words are untouched. Returns the final px size.
  CH.fitHead = (node, size, min = 0.55) => {
    if (!node) return size;
    node.style.overflowWrap = "normal";
    node.style.wordBreak = "keep-all";
    node.style.hyphens = "none";
    let s = +size;
    const floor = +size * min;
    node.style.fontSize = `${Math.round(s)}px`;
    while (node.scrollWidth > node.clientWidth + 1 && s > floor) {
      s = Math.max(floor, s * 0.95);
      node.style.fontSize = `${Math.round(s)}px`;
    }
    return Math.round(s);
  };
  CH.esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  // "*word*" -> marker span ; numbers/₹ amounts -> tabular num span. Works on text, never on HTML.
  const NUM = /(₹\s?[\d,]+(?:\.\d+)?|\b\d[\d,]*(?:\.\d+)?%?)/g;
  const nums = (txt) => CH.esc(txt).replace(NUM, '<span class="num">$1</span>');
  CH.rich = (s) => String(s ?? "").split(/(\*[^*]+\*)/g).map((part) =>
    /^\*[^*]+\*$/.test(part) ? `<span class="marker" style="--marker:0">${nums(part.slice(1, -1))}</span>` : nums(part)).join("");

  // ---------------------------------------------------------------- seeded rng
  CH.rng = (seed) => {
    let a = 0;
    for (const ch of String(seed)) a = (a * 31 + ch.charCodeAt(0)) | 0;
    return () => {
      a |= 0; a = (a + 0x6d2b79f5) | 0;
      let t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  };
  // resting tilt of a paper object: never perfectly straight, never more than ~2°
  CH.tilt = (rng, max = 2.2) => { const v = (rng() * 2 - 1) * max; return Math.abs(v) < 0.5 ? (v < 0 ? -0.7 : 0.7) : v; };

  // ---------------------------------------------------------------- DOM helpers
  CH.h = (html) => { const tpl = document.createElement("template"); tpl.innerHTML = html.trim(); return tpl.content.firstElementChild; };
  CH.mascot = (expr, id, size = 400, extraClass = "") =>
    g.Chillar.svg({ expr, id, size }).replace('class="chillar ', `class="chillar ${extraClass} `);

  // ---------------------------------------------------------------- motion vocabulary
  // entrance: opacity is already full on the entrance frame (a cut never lands on an empty frame),
  // the motion runs 6 frames,
  // decisive ease-out, no overshoot (bounce is reserved for the mascot + stamp)
  CH.pop = (tl, el, t, o = {}) => {
    tl.fromTo(el, { opacity: 0 }, { opacity: 1, duration: F, ease: "none" }, t - F);   // fully visible ON the cut frame
    return tl.fromTo(el, { scale: o.from ?? 0.94, y: o.y ?? 40, rotation: o.rot ?? 0 },
      { scale: 1, y: 0, rotation: o.rotTo ?? 0, duration: (o.frames ?? 6) * F, ease: o.ease ?? "power3.out" }, t);
  };
  // a paper object put down on the desk by a hand. A real editor's shots don't all arrive the same way, so each
  // scene gets one seeded way in (all its papers share it: one hand, one move), never the previous scene's:
  // toss (lands from below with a twist) · slide (pushed in from a side) · drop (set down from above, a touch
  // closer to the lens) · place (already in hand, settles) · deal (flicked in like a card). A scene's
  // `entrance` param picks one. No overshoot (reserved for the mascot + stamp). Travel stays short (≤ 150 px) and
  // ≥ 9 frames for the sideways moves: the eye must land on the paper, not chase it (creator, 2026-10-22: "moves too fast").
  const ENTRANCES = ["toss", "slide", "drop", "place", "deal"];
  CH.entranceFor = (sceneId, want) => {
    if (ENTRANCES.includes(want)) return want;
    const r = CH.rng("entr:" + sceneId);
    let k = ENTRANCES[Math.floor(r() * ENTRANCES.length)];
    if (k === CH._prevEntrance) k = ENTRANCES[(ENTRANCES.indexOf(k) + 1 + Math.floor(r() * 4)) % ENTRANCES.length];
    return k;
  };
  CH.toss = (tl, el, t, rest = 0, o = {}) => {
    const dir = rest >= 0 ? 1 : -1;
    const sc = CH._scene || {};
    const kind = o.kind || sc.entrance || "toss";
    const side = (sc.side ?? (rest >= 0 ? 1 : -1));
    tl.fromTo(el, { opacity: 0 }, { opacity: 1, duration: F, ease: "none" }, t - F);   // fully visible ON the cut frame
    const to = { x: 0, y: 0, rotation: rest, scale: 1, ease: "power3.out" };
    if (kind === "slide")
      return tl.fromTo(el, { x: -120 * side, y: 10, rotation: rest - side * 2, scale: 1 }, { ...to, duration: (o.frames ?? 9) * F }, t);
    if (kind === "drop")
      return tl.fromTo(el, { x: 0, y: -46, rotation: rest + dir * 2, scale: 1.045 }, { ...to, duration: (o.frames ?? 6) * F }, t);
    if (kind === "place")
      return tl.fromTo(el, { x: 6 * side, y: 10, rotation: rest + dir * 1.2, scale: 1.022 }, { ...to, duration: (o.frames ?? 5) * F }, t);
    if (kind === "deal")
      return tl.fromTo(el, { x: 150 * side, y: 24, rotation: rest + side * 6, scale: 1 }, { ...to, duration: (o.frames ?? 9) * F }, t);
    return tl.fromTo(el,
      { x: 0, y: o.y ?? 90, rotation: rest + dir * (o.twist ?? 5), scale: 1.02 },
      { ...to, duration: (o.frames ?? 7) * F }, t);
  };
  CH.slideIn = (tl, el, t, dir = 1, o = {}) => {
    tl.fromTo(el, { opacity: 0 }, { opacity: 1, duration: F, ease: "none" }, t - F);   // fully visible ON the cut frame
    return tl.fromTo(el, { x: 140 * dir }, { x: 0, duration: (o.frames ?? 6) * F, ease: "power3.out" }, t);
  };
  // the thappa: 140% -> 100% in 4 frames, then a 2-frame shake
  CH.slam = (tl, el, t, rot = -8) => {
    tl.fromTo(el, { opacity: 0, scale: 1.4, rotation: rot - 4 }, { opacity: 1, scale: 1, rotation: rot, duration: 4 * F, ease: "power4.in" }, t);
    tl.fromTo(el, { x: 0 }, { x: -7, duration: F, ease: "none" }, t + 4 * F);
    tl.to(el, { x: 6, duration: F, ease: "none" }, t + 5 * F);
    tl.to(el, { x: 0, duration: F, ease: "none" }, t + 6 * F);
    return t + 4 * F; // impact time (for the thunk)
  };
  // yellow marker swipe on every .marker inside el
  CH.markers = (tl, el, t, gap = 4 * F) => {
    [...el.querySelectorAll(".marker")].forEach((m, i) =>
      tl.fromTo(m, { "--marker": 0 }, { "--marker": 1, duration: 6 * F, ease: "power2.out" }, t + i * gap));
  };
  // small zoom punch on a punchline
  CH.punch = (tl, el, t, amt = 1.06) => {
    tl.fromTo(el, { scale: 1 }, { scale: amt, duration: 3 * F, ease: "power2.out" }, t);
    tl.to(el, { scale: 1, duration: 6 * F, ease: "power2.inOut" }, t + 3 * F);
  };
  // receipt-style stepped reveal: each element appears on its own frame step
  CH.print = (tl, els, t, step = 0.18) => {
    els.forEach((e, i) => tl.fromTo(e, { opacity: 0, y: -10 }, { opacity: 1, y: 0, duration: 2 * F, ease: "steps(2)" }, t + i * step));
    return t + els.length * step;
  };

  // ---------------------------------------------------------------- blue-ballpoint scribbles
  // Hand-drawn marks generated from a seeded rng, so every scene's circle is a little different
  // but every render is identical. kind: circle | underline | strike | arrow | tick
  const smooth = (pts) => {           // Catmull-Rom -> cubic Bézier
    let d = `M${pts[0][0].toFixed(1)} ${pts[0][1].toFixed(1)}`;
    for (let i = 0; i < pts.length - 1; i++) {
      const p0 = pts[i - 1] || pts[i], p1 = pts[i], p2 = pts[i + 1], p3 = pts[i + 2] || p2;
      const c1 = [p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6];
      const c2 = [p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6];
      d += ` C${c1[0].toFixed(1)} ${c1[1].toFixed(1)} ${c2[0].toFixed(1)} ${c2[1].toFixed(1)} ${p2[0].toFixed(1)} ${p2[1].toFixed(1)}`;
    }
    return d;
  };
  const SCRIB = {
    circle(w, h, r) {
      const cx = w / 2, cy = h / 2, a0 = (-160 + r() * 30) * Math.PI / 180, sweep = (1.12 + r() * 0.08) * 2 * Math.PI;
      const ph = r() * 6, pts = [];
      for (let i = 0; i <= 44; i++) {
        const f = i / 44, a = a0 + f * sweep, wob = 1 + 0.035 * Math.sin(3 * a + ph) + 0.05 * f;
        pts.push([cx + (w / 2) * wob * Math.cos(a) + f * w * 0.03, cy + (h / 2) * wob * Math.sin(a) - f * h * 0.06]);
      }
      return [smooth(pts)];
    },
    underline(w, h, r) {
      const y = h * 0.5, a = [], b = [];
      for (let i = 0; i <= 8; i++) a.push([w * i / 8, y + Math.sin(i * 1.3 + r() * 2) * 3 - i * 0.8]);
      for (let i = 0; i <= 6; i++) b.push([w * (0.92 - i * 0.12), y + 16 + Math.sin(i * 1.7) * 3 + i * 0.6]);
      return [smooth(a), smooth(b)];
    },
    strike(w, h, r) {
      const pts = [], n = 3;
      for (let i = 0; i <= n; i++) {
        const x = i % 2 ? w * (0.94 + r() * 0.06) : w * (r() * 0.06);
        pts.push([x, h * 0.38 + (h * 0.3) * (i / n) + (r() - 0.5) * 8]);
      }
      return [pts.map((p, i) => `${i ? "L" : "M"}${p[0].toFixed(1)} ${p[1].toFixed(1)}`).join(" ")];
    },
    arrow(w, h, r) {       // from bottom-left to top-right, curving
      const s = [6, h - 6], e = [w - 10, 12], c = [w * (0.18 + r() * 0.1), h * 0.1];
      const pts = [];
      for (let i = 0; i <= 16; i++) {
        const f = i / 16;
        pts.push([(1 - f) ** 2 * s[0] + 2 * (1 - f) * f * c[0] + f * f * e[0], (1 - f) ** 2 * s[1] + 2 * (1 - f) * f * c[1] + f * f * e[1]]);
      }
      const [px, py] = pts[14], ang = Math.atan2(e[1] - py, e[0] - px), L = 34;
      const head = `M${(e[0] - L * Math.cos(ang - 0.5)).toFixed(1)} ${(e[1] - L * Math.sin(ang - 0.5)).toFixed(1)} L${e[0]} ${e[1]} L${(e[0] - L * Math.cos(ang + 0.5)).toFixed(1)} ${(e[1] - L * Math.sin(ang + 0.5)).toFixed(1)}`;
      return [smooth(pts), head];
    },
    tick(w, h) { return [`M${w * 0.06} ${h * 0.55} L${w * 0.38} ${h * 0.88} L${w * 0.96} ${h * 0.08}`]; },
  };
  // returns an absolutely positioned <svg> (x, y = top-left inside the positioned parent)
  CH.scribble = (kind, { x = 0, y = 0, w = 200, h = 100, rng = Math.random, stroke = 7, cls = "" } = {}) => {
    const pad = 24, paths = (SCRIB[kind] || SCRIB.underline)(w, h, rng);
    return `<svg class="scrib ${cls}" viewBox="${-pad} ${-pad} ${w + 2 * pad} ${h + 2 * pad}" width="${w + 2 * pad}" height="${h + 2 * pad}"
      style="left:${x - pad}px; top:${y - pad}px">${paths.map((d) =>
        `<path d="${d}" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1" style="stroke-width:${stroke}px"/>`).join("")}</svg>`;
  };
  // draws every scribble path inside root, one after another, at hand speed
  CH.draw = (tl, root, t, dur = 0.35) => {
    const paths = root ? [...root.querySelectorAll(".scrib path")] : [];
    const each = dur / Math.max(1, paths.length);
    paths.forEach((p, i) => tl.fromTo(p, { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: each, ease: "power1.inOut" }, t + i * each));
    return t + dur;
  };

  // odometer: every digit starts BLANK (never a wrong number on screen), rolls a full cycle, lands
  const STRIP = ["&nbsp;", 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9];
  CH.odometer = (value, o = {}) => {
    const s = (o.prefix ?? "") + CH.inr(value, o) + (o.suffix ?? "");
    const cells = [...s].map((ch) => /\d/.test(ch)
      ? `<span class="odo-d"><span class="odo-strip">${STRIP.map((n, k) => `<span${k ? ' style="visibility:hidden"' : ""}>${n}</span>`).join("")}</span></span>`
      : `<span class="odo-s${ch === "." ? " odo-dot" : ""}">${CH.esc(ch)}</span>`).join("");
    return `<span class="odo" data-target="${CH.esc(s)}">${cells}</span>`;
  };
  CH.roll = (tl, odoEl, t, dur = 0.9) => {
    const target = odoEl.dataset.target;
    const digits = [...target].filter((c) => /\d/.test(c));
    const end = t + dur + digits.length * 0.04;
    [...odoEl.querySelectorAll(".odo-strip")].forEach((strip, i) => {
      const final = +digits[i];
      const land = 11 + final;                          // blank → one full cycle → the final digit
      const lag = (digits.length - 1 - i) * 0.04;      // lower digits keep spinning longer
      // land on the cell's exact layout offset (px), not a rounded % of the 21-cell strip: a %-based
      // offset leaves sub-pixel slivers of the neighbouring digits inside the 1em window
      const cell = strip.children[land];
      const y = cell && cell.offsetHeight ? -cell.offsetTop : null;
      tl.set([...strip.children].slice(1), { visibility: "inherit" }, t);   // only the blank shows before the roll
      tl.fromTo(strip, y === null ? { yPercent: 0 } : { y: 0 }, y === null
        ? { yPercent: -(land / STRIP.length) * 100, duration: dur + lag, ease: "power3.out" }
        : { y, duration: dur + lag, ease: "power3.out" }, t);
      // once landed only the final digit stays painted, so every landed frame reads exactly the value
      tl.set([...strip.children].filter((_, k) => k !== land), { visibility: "hidden" }, end);
    });
    return end;
  };

  // ---------------------------------------------------------------- mascot motion (GSAP mirrors of mascot.css)
  CH.mascotAnim = (tl, svg, kind, t, d) => {
    if (!svg || !kind || kind === "none") return;
    const q = (s) => [...svg.querySelectorAll(s)];
    const fig = svg.querySelector(".figure");
    if (kind === "blink") {
      for (let b = t + 0.5; b < t + d - 0.2; b += 2.2) {
        tl.fromTo(q(".eye"), { scaleY: 1 }, { scaleY: 0.12, duration: F, transformOrigin: "50% 50%", ease: "none" }, b);
        tl.to(q(".eye"), { scaleY: 1, duration: F, ease: "none" }, b + 3 * F);
      }
    } else if (kind === "bounce") {
      const n = Math.max(1, Math.min(3, Math.floor(d / 0.6)));
      for (let i = 0; i < n; i++) {
        const b = t + i * 0.6;
        tl.fromTo(fig, { y: 0, scaleY: 1 }, { y: -26, scaleY: 1.03, duration: 0.24, ease: "power2.out", transformOrigin: "50% 100%" }, b);
        tl.to(fig, { y: 0, scaleY: 0.95, duration: 0.22, ease: "power2.in" }, b + 0.24);
        tl.to(fig, { scaleY: 1, duration: 0.1, ease: "power1.out" }, b + 0.46);
      }
    } else if (kind === "shake") {
      tl.fromTo(fig, { x: 0, rotation: 0 }, { x: -8, rotation: -2, duration: F, ease: "none", transformOrigin: "50% 100%" }, t);
      [7, -5, 4, -2, 0].forEach((x, i) => tl.to(fig, { x, rotation: x / 4, duration: F, ease: "none" }, t + (i + 1) * F));
    } else if (kind === "sweat") {
      tl.fromTo(q(".sweat"), { y: -6, opacity: 0 }, { y: 34, opacity: 1, duration: 1.0, ease: "power1.in" }, t + 0.2);
    } else if (kind === "walk") {
      const steps = Math.max(2, Math.floor(Math.min(d, 2.4) / 0.4));
      for (let i = 0; i < steps; i++) {
        const b = t + i * 0.4, s = i % 2 ? -16 : 16;
        tl.fromTo(svg.querySelector(".leg-l"), { rotation: -s }, { rotation: s, duration: 0.4, ease: "sine.inOut", transformOrigin: "50% 0%" }, b);
        tl.fromTo(svg.querySelector(".leg-r"), { rotation: s }, { rotation: -s, duration: 0.4, ease: "sine.inOut", transformOrigin: "50% 0%" }, b);
        tl.fromTo(fig, { y: 0 }, { y: -8, duration: 0.2, ease: "sine.out", yoyo: true, repeat: 1 }, b);
      }
    }
  };

  // ---------------------------------------------------------------- mount
  // Builds every scene onto one paused timeline. Does NOT register it: the caller registers
  // window.__timelines[id] only after everything (captions too) has been added.
  CH.mount = (spec, opts = {}) => {
    const tl = opts.tl;  // created + registered by the composition bootstrap
    const stage = document.getElementById("stage");
    for (const s of spec.scenes) {
      const def = registry[s.component];
      const el = document.getElementById(s.id);
      if (!def || !el) { console.error("missing component/clip", s.component, s.id); continue; }
      el.classList.add("c-" + s.component);
      const shot = s.track === 1 && s.component !== "outro";
      const entrance = CH.entranceFor(s.id, (s.params || {}).entrance);
      CH._scene = { id: s.id, entrance, side: CH.rng("side:" + s.id)() < 0.5 ? -1 : 1 };
      def.build({ el, p: s.params || {}, t: s.start, d: s.duration, tl, rng: CH.rng(s.id), id: s.id, stage, spec });
      if (shot) CH._prevEntrance = entrance;
      el.dataset.entrance = entrance;
      CH._scene = null;
      // dy (px, optional, any scene component with a .zone): nudge the whole composition down (+) or up (−)
      // inside the content zone. CSS `translate` so it never fights GSAP transforms.
      const dy = +((s.params || {}).dy || 0), zone = dy ? el.querySelector(".zone") : null;
      if (zone) zone.style.translate = `0 ${dy}px`;
    }
    for (const fx of spec.effects || []) {
      if (fx.type === "punch") CH.punch(tl, stage, fx.at, fx.amount || 1.06);
    }
    // spec.human: true (default) | false | {camera, boil, ink, tex} to switch single layers (tuning, A/B)
    const H = spec.human === false ? {} : { camera: true, boil: true, ink: false, tex: true,   // ink: read as compression
                                            ...(typeof spec.human === "object" ? spec.human : {}) };
    if (H.tex || H.ink) CH.paperTexture(spec, H);
    if (H.boil) CH.boil(tl, spec); else document.getElementById("root")?.classList.add("ch-noboil");
    if (H.camera && !g.CH_PROBE) CH.camera(tl, spec);
    return tl;
  };

  // ---------------------------------------------------------------- the hand-made layer (every reel)
  // A phone held over a table: slow drift + breathing, the operator re-settling after some cuts, an occasional
  // focus pull, light that moves a little. Seeded from the episode, so every render is identical. Captions and
  // the wordmark sit outside #camera (they're added in post, like a real edit). qa's probe turns it off
  // (CH_PROBE) so layout boxes are measured still.
  CH.camera = (tl, spec) => {
    const cam = document.getElementById("camera"), rig = document.getElementById("rig");
    const light = document.getElementById("light");
    if (!cam || !rig) return;
    const dur = +spec.duration || 0, r = CH.rng("camera:" + (spec.episode || "reel"));
    // whole pixels only, no rotation, no zoom: any sub-pixel transform makes Chrome resample the whole frame and
    // every edge goes soft (pilot 2026-10-22: text sharpness 940 → 31). Drift reads as a hand; pixels stay crisp.
    tl.set(cam, { x: 0, y: 0 }, 0);
    for (let t = 0; t < dur; ) {
      const step = 0.7 + r() * 0.9;
      tl.to(cam, { x: Math.round((r() * 2 - 1) * 4), y: Math.round((r() * 2 - 1) * 3), duration: step,
                   ease: "sine.inOut", snap: { x: 1, y: 1 } }, t);
      t += step;
    }
    const cuts = spec.scenes.filter((s) => s.track === 1 && s.component !== "outro" && s.start > 0.3).map((s) => s.start);
    cuts.forEach((c, i) => {
      const k = CH.rng("cut:" + i + ":" + c)();
      if (k < 0.28) {            // re-framed a beat late: a small push that settles, exactly back to 1:1 pixels
        // immediateRender:false — a fromTo otherwise stamps its start (zoom/blur) on the frame from t=0 until its cut
        tl.fromTo(rig, { scale: 1.016, y: 7 }, { scale: 1, y: 0, duration: 9 * F, ease: "power2.out", immediateRender: false }, c);
        tl.set(rig, { clearProps: "transform" }, c + 9 * F);
      } else if (k < 0.42) {     // focus finds the paper; then no filter at all (blur(0px) still re-rasterises)
        tl.fromTo(rig, { filter: "blur(1.4px)" }, { filter: "blur(0px)", duration: 4 * F, ease: "power1.out", immediateRender: false }, c);
        tl.set(rig, { filter: "none" }, c + 4 * F);
      }
    });
    if (light) {
      tl.set(light, { opacity: 0.5, "--lx": "46%", "--ly": "28%" }, 0);
      for (let t = 0; t < dur; ) {
        const step = 2.2 + r() * 2.5;
        tl.to(light, { opacity: 0.35 + r() * 0.4, "--lx": `${38 + r() * 24}%`, "--ly": `${20 + r() * 18}%`,
                       duration: step, ease: "sine.inOut" }, t);
        t += step;
      }
    }
  };

  // Paper that has lived: fibre, a seeded crease on some sheets, slightly aged edges. Found by colour (every
  // surface painted the theme's --paper), so every component gets it without its own CSS. An overlay child
  // (.ch-tex, multiply, under 6 % density) sits in the sheet's own clip; qa ignores it like pen marks.
  CH.paperTexture = (spec, H = { tex: true, ink: true }) => {
    const probe = document.createElement("i");
    probe.style.cssText = "position:absolute;width:1px;height:1px;background:var(--paper)";
    document.getElementById("root").appendChild(probe);
    const paper = getComputedStyle(probe).backgroundColor;
    probe.remove();
    for (const s of spec.scenes) {
      const root = document.getElementById(s.id);
      if (!root || s.component === "chapter-field") continue;
      let n = 0;
      for (const el of root.querySelectorAll("*")) {
        if (el.classList.contains("ch-tex") || el instanceof SVGElement) continue;
        const cs = getComputedStyle(el);
        // thermal / dot-matrix print is never crisp vector type: printout text gets slightly rough edges
        if (H.ink && /JetBrains/i.test(cs.fontFamily) && el.childElementCount === 0 && el.textContent.trim()) el.classList.add("ch-ink");
        if (n >= 6 || !H.tex) continue;
        const isPaper = el.matches(".paper-obj, .paper-torn") || cs.backgroundColor === paper;
        if (!isPaper || cs.position === "static" || el.offsetWidth < 140 || el.offsetHeight < 90) continue;
        if (el.parentElement && el.parentElement.closest(".ch-papered")) continue;   // one texture per sheet
        const r = CH.rng("tex:" + s.id + ":" + n);
        const tex = document.createElement("i");
        tex.className = "ch-tex";
        tex.style.setProperty("--sx", `${Math.round(r() * 240)}px`);
        tex.style.setProperty("--sy", `${Math.round(r() * 240)}px`);
        tex.style.setProperty("--crease", `${Math.round(70 + r() * 40)}deg`);
        tex.style.setProperty("--cp", `${Math.round(28 + r() * 44)}%`);
        tex.style.setProperty("--ca", r() < 0.45 ? "1" : "0");           // not every sheet was folded
        tex.style.setProperty("--age", (0.4 + r() * 0.6).toFixed(2));
        el.classList.add("ch-papered");
        el.appendChild(tex);
        n++;
      }
    }
  };

  // Line boil: hand-drawn lines are never perfectly still. The mascot, people and pen marks wobble a hair,
  // re-drawn on twos (every 3rd frame at 30 fps, like hand animation), from one seeded turbulence.
  CH.boil = (tl, spec) => {
    const turb = document.querySelector("#ch-boil feTurbulence");
    if (!turb) return;
    const dur = +spec.duration || 0;
    for (let t = 0, k = 1; t < dur; t += 3 * F, k++) tl.set(turb, { attr: { seed: (k % 7) + 1 } }, t);
  };

  g.CH = CH;
})(window);
