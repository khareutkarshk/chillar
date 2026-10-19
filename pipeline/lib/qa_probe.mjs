// Headless layout probe for pipeline/qa.py.
//
//   node pipeline/lib/qa_probe.mjs <request.json>   -> JSON on stdout
//   request = {html, chrome, times: [s, ...], compId}
//
// Loads the built composition, seeks the one master GSAP timeline to each time, shows only the
// clips live at that time (what the HyperFrames renderer does), and reports, per visible clip:
//   texts   — every visible text run: text, box (clipped by overflow ancestors), opacity, font px
//   painted — visible painted elements (text, svg, img, filled boxes): box + opacity
//   odo     — what each odometer actually displays (digits that sit inside their column window)
import { createRequire } from "node:module";
import { readFileSync } from "node:fs";
import { pathToFileURL } from "node:url";
import path from "node:path";

const require = createRequire(path.resolve("package.json"));
const puppeteer = require("puppeteer-core");
const req = JSON.parse(readFileSync(process.argv[2], "utf8"));

const browser = await puppeteer.launch({
  executablePath: req.chrome,
  headless: "shell",
  args: ["--no-sandbox", "--allow-file-access-from-files", "--font-render-hinting=none"],
});
try {
  const page = await browser.newPage();
  await page.setViewport({ width: 1080, height: 1920, deviceScaleFactor: 1 });
  const errors = [];
  page.on("pageerror", (e) => errors.push(String(e)));
  page.on("console", (m) => { if (m.type() === "error") errors.push(m.text()); });
  // the renderer injects its runtime; standalone we only need the registry it reads from
  await page.evaluateOnNewDocument(() => { window.__timelines = {}; });
  await page.goto(pathToFileURL(req.html).href, { waitUntil: "load" });
  // the renderer sizes the page to the composition; standalone html/body would collapse to 0 height
  await page.addStyleTag({ content: "html, body { width: 1080px; height: 1920px; }" });
  await page.waitForFunction((id) => !!(window.__timelines && window.__timelines[id]), { timeout: 20000, polling: 100 }, req.compId)
    .catch((e) => { throw new Error(`composition never registered its timeline: ${errors.join(" | ") || e.message}`); });

  const samples = await page.evaluate((times, compId) => {
    const tl = window.__timelines[compId];
    const clips = [...document.querySelectorAll(".clip")];
    const VW = 1080, VH = 1920;
    const inter = (a, b) => {
      const r = { x0: Math.max(a.x0, b.x0), y0: Math.max(a.y0, b.y0), x1: Math.min(a.x1, b.x1), y1: Math.min(a.y1, b.y1) };
      return r.x1 > r.x0 && r.y1 > r.y0 ? r : null;
    };
    const box = (r) => ({ x0: r.left, y0: r.top, x1: r.right, y1: r.bottom });
    const round = (b) => b && [b.x0, b.y0, b.x1, b.y1].map((v) => Math.round(v));

    // effective opacity + clip rect from ancestors (overflow != visible clips its children)
    function env(el) {
      let op = 1, clip = { x0: 0, y0: 0, x1: VW, y1: VH };
      for (let n = el; n && n !== document.documentElement; n = n.parentElement) {
        const cs = getComputedStyle(n);
        if (cs.display === "none" || cs.visibility === "hidden") return null;
        op *= parseFloat(cs.opacity);
        if (n !== el && (cs.overflow !== "visible" || cs.overflowX !== "visible" || cs.overflowY !== "visible")) {
          clip = inter(clip, box(n.getBoundingClientRect()));
          if (!clip) return null;
        }
      }
      return op < 0.02 ? null : { op, clip };
    }

    // colour behind a text element from its own ancestors (up to and incl. the clip): a filled box,
    // or a .marker swipe once it is at least half drawn. null = nothing of its own -> paper/field decides.
    function ownBg(el, clip) {
      for (let n = el; n; n = n.parentElement) {
        const cs = getComputedStyle(n);
        if (n.classList && n.classList.contains("marker")) {
          const m = parseFloat(cs.getPropertyValue("--marker") || "1");
          const c = (cs.backgroundImage.match(/rgba?\([^)]*\)/) || [])[0];
          if (m >= 0.5 && c) return c;
        } else if (cs.backgroundColor && !/rgba\(.*,\s*0\)$|transparent/.test(cs.backgroundColor)) {
          return cs.backgroundColor;
        }
        if (n === clip) break;
      }
      return null;
    }

    function probeClip(clip) {
      const texts = [], painted = [];
      const walker = document.createTreeWalker(clip, NodeFilter.SHOW_TEXT);
      const byEl = new Map();
      for (let n = walker.nextNode(); n; n = walker.nextNode()) {
        if (!n.nodeValue.trim()) continue;
        const el = n.parentElement;
        const e = env(el);
        if (!e) continue;
        const rg = document.createRange();
        rg.selectNodeContents(n);
        let u = null;
        const lines = [];
        for (const r of rg.getClientRects()) {
          const b = inter(box(r), e.clip);
          if (!b) continue;
          lines.push(b);
          u = u ? { x0: Math.min(u.x0, b.x0), y0: Math.min(u.y0, b.y0), x1: Math.max(u.x1, b.x1), y1: Math.max(u.y1, b.y1) } : b;
        }
        if (!u) continue;
        const prev = byEl.get(el);
        if (prev) {
          prev.text += " " + n.nodeValue.trim();
          prev.lines.push(...lines);
          prev.b = { x0: Math.min(prev.b.x0, u.x0), y0: Math.min(prev.b.y0, u.y0), x1: Math.max(prev.b.x1, u.x1), y1: Math.max(prev.b.y1, u.y1) };
        } else {
          const cs = getComputedStyle(el);
          const br = el.getBoundingClientRect();
          const sy = el.offsetHeight ? br.height / el.offsetHeight : 1;
          byEl.set(el, { el, text: n.nodeValue.trim(), b: u, lines, op: e.op, font: parseFloat(cs.fontSize) * sy, color: cs.color, bg: ownBg(el, clip) });
        }
      }
      const els = [...byEl.values()];
      els.forEach((t, i) => {
        // ancestry index so qa.py can skip overlaps between an element and its own children
        t.el.dataset.qaIdx = i;
      });
      for (const t of els) {
        let anc = [];
        for (let n = t.el.parentElement; n && n !== clip; n = n.parentElement) if (n.dataset.qaIdx) anc.push(+n.dataset.qaIdx);
        const odo = t.el.closest(".odo, .od-num");
        texts.push({ i: +t.el.dataset.qaIdx, text: t.text.slice(0, 80), box: round(t.b), lines: t.lines.slice(0, 12).map(round), op: +t.op.toFixed(2),
                     font: Math.round(t.font), cls: String(t.el.className || "").slice(0, 40), anc, color: t.color, bg: t.bg,
                     odo: odo ? (odo.closest(".clip")?.id || "") : "" });
      }
      els.forEach((t) => delete t.el.dataset.qaIdx);

      for (const el of clip.querySelectorAll("*")) {
        const r = el.getBoundingClientRect();
        if (r.width * r.height < 900) continue;
        const cs = getComputedStyle(el);
        const fill = (cs.backgroundColor && !/rgba\(.*,\s*0\)$|transparent/.test(cs.backgroundColor)) || cs.backgroundImage !== "none";
        const kind = el instanceof SVGSVGElement ? "svg" : el.tagName === "IMG" || el.tagName === "CANVAS" ? "img" : fill ? "fill" : null;
        if (!kind) continue;
        if (r.width >= VW - 2 && r.height >= VH - 2) continue;      // full-frame wash, not an object
        const e = env(el);
        if (!e) continue;
        const b = inter(box(r), e.clip);
        if (!b) continue;
        painted.push({ kind, box: round(b), op: +e.op.toFixed(2), cls: String(el.className?.baseVal ?? el.className ?? "").slice(0, 40) });
      }
      return { texts, painted };
    }

    const out = [];
    for (const t of times) {
      tl.seek(t, false);   // like the renderer: callbacks (count-mode onUpdate) must fire
      for (const c of clips) {
        const s = parseFloat(c.dataset.start), d = parseFloat(c.dataset.duration);
        c.style.display = t >= s - 1e-6 && t < s + d - 1e-6 ? "" : "none";
      }
      const live = clips.filter((c) => c.style.display !== "none");
      const stage = document.getElementById("stage");
      const st = getComputedStyle(stage).transform;
      const fl = document.querySelector(".field-light");
      const field = fl ? getComputedStyle(fl).backgroundColor : null;
      out.push({ t, stage: st, field, clips: live.map((c) => ({ id: c.id, comp: ([...c.classList].find((k) => k.startsWith("c-")) || "").slice(2),
                                                        track: +c.dataset.trackIndex, ...probeClip(c) })) });
    }
    return out;
  }, req.times, req.compId);

  process.stdout.write(JSON.stringify({ errors, samples }));
} finally {
  await browser.close();
}
