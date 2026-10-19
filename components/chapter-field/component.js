CH.define("chapter-field", {
  build({ el, p, tl }) {
    el.classList.add("field-light");
    if (p.grain) el.classList.add("grain");
    const root = document.getElementById("root");
    const vars = (f) => ({ "--field": `var(--${f})`, "--on-field": `var(--${f}-ink)` });
    const chs = (p.chapters || []).slice().sort((a, b) => a.start - b.start);
    const first = vars((chs[0] || {}).field || "bone");
    for (const k in first) root.style.setProperty(k, first[k]);   // frame 1 is right before any seek
    // hard cut to the next field exactly on the chapter's first scene (seek-safe: sets revert on rewind)
    chs.slice(1).forEach((c) => tl.set(root, vars(c.field), c.start));
  },
});
