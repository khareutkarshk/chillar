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
  // a paper object tossed onto the desk: lands from below with a little extra twist, settles at its tilt
  CH.toss = (tl, el, t, rest = 0, o = {}) => {
    const dir = rest >= 0 ? 1 : -1;
    tl.fromTo(el, { opacity: 0 }, { opacity: 1, duration: F, ease: "none" }, t - F);   // fully visible ON the cut frame
    return tl.fromTo(el,
      { y: o.y ?? 90, rotation: rest + dir * (o.twist ?? 5), scale: 1.02 },
      { y: 0, rotation: rest, scale: 1, duration: (o.frames ?? 7) * F, ease: "power3.out" }, t);
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
      ? `<span class="odo-d"><span class="odo-strip">${STRIP.map((n) => `<span>${n}</span>`).join("")}</span></span>`
      : `<span class="odo-s">${CH.esc(ch)}</span>`).join("");
    return `<span class="odo" data-target="${CH.esc(s)}">${cells}</span>`;
  };
  CH.roll = (tl, odoEl, t, dur = 0.9) => {
    const target = odoEl.dataset.target;
    const digits = [...target].filter((c) => /\d/.test(c));
    [...odoEl.querySelectorAll(".odo-strip")].forEach((strip, i) => {
      const final = +digits[i];
      const land = 11 + final;                          // blank → one full cycle → the final digit
      const lag = (digits.length - 1 - i) * 0.04;      // lower digits keep spinning longer
      tl.fromTo(strip, { yPercent: 0 }, { yPercent: -(land / STRIP.length) * 100, duration: dur + lag, ease: "power3.out" }, t);
    });
    return t + dur + digits.length * 0.04;
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
      def.build({ el, p: s.params || {}, t: s.start, d: s.duration, tl, rng: CH.rng(s.id), id: s.id, stage, spec });
    }
    for (const fx of spec.effects || []) {
      if (fx.type === "punch") CH.punch(tl, stage, fx.at, fx.amount || 1.06);
    }
    return tl;
  };

  g.CH = CH;
})(window);
