---
name: "visualizers"
description: "Luke's six visualizer patterns: zoom bars (comparison bars with a magnified inset strip for tiny deltas), dot-grid simulator (N dots re-run with staggered animation for probability/risk), live formula slider (slider driving instant recomputed readouts + a dynamic insight line), estimator + caveat card (computed estimate beside a prominent callout that overrides the naive reading), source link-out cards (stacked source cards with type badges), and live mic visualizer (tap-to-start microphone driving a real-time waveform plus a scrolling waterfall spectrogram, analyzed on-device). Dependency-free vanilla JS/CSS, mobile-first."
---

# Visualizers Skill

## Purpose
Four interactive patterns for making numbers *felt*, extracted from the SPF 30/50/60 blog post (https://lukezhang.si/blog/spf-30-50-60/) — the visualizers Luke called out as worth reusing. Each pattern is copy-paste-ready vanilla HTML/CSS/JS: no dependencies, no build step, parameterized through a small CONFIG block at the top of each script. They ship with the explainer-tools family's 7 shared rules baked in (16px inputs, `touch-action:manipulation` on taps, `pan-y` on sliders, pointer-first, bespoke chrome, mobile-first, zero console errors).

## When to use which pattern
- **Zoom bars** — a comparison where the interesting difference is small and would be invisible on a normal bar chart (blocked % vs the transmitted sliver; fee differences; error rates).
- **Dot-grid simulator** — probability, risk, or funnel stories: N dots = a population, a toggle re-runs which dots "get through" (infection rates, conversion funnels, defect rates).
- **Live formula slider** — any what-if calculator: one input drives several instantly recomputed readouts plus a dynamic insight line that states the takeaway in words.
- **Estimator + caveat card** — an estimate whose model's limits matter more than its output: computed rows beside a prominent, always-visible caveat callout.
- **Source link-out cards** — the Sources section at the end of a post: stacked cards with a source-type badge, full-width title, and one-line citation meta. No JS.
- **Live mic visualizer** — letting the reader speak into the page and see their own voice: a tap-to-start mic button driving a live waveform strip plus a scrolling waterfall spectrogram, analyzed on-device. Use when seeing your own input teaches the concept (spectrograms, pitch, vowels vs fricatives).

All six can live on the same page. Each script is an IIFE scoped to its own element IDs — no shared globals, no collisions.

## Shared theme block
Put this once per page; every pattern below reads these variables. Retheme by changing six values.

```css
:root{
  --viz-bg:#141311; --viz-panel:#1d1b17; --viz-panel2:#26231d;
  --viz-line:#3a362c; --viz-ink:#f2ede0; --viz-muted:#a39c88; --viz-faint:#6f695b;
  --viz-accent:#e8a33d;   /* the "good/majority" color */
  --viz-danger:#e05252;   /* the "gets through / warning" color */
  --viz-mono:ui-monospace,'SF Mono',Menlo,Consolas,monospace;
}
```

---

## Pattern 1 — Comparison bars

Horizontal comparison bars where each bar is 100% of something, with the fill growing from the left and the remainder (sliver) settling in from the right edge. That simultaneous opposing motion is the feel.

### Structure
```html
<div class="vzb-row" data-value="96.7" data-tail="3.3" data-cap="of every 100 get through">
  <div class="vzb-lab"><b>SPF 30</b><span><b>96.7%</b> blocked</span></div>
  <div class="vzb-bar"><div class="vzb-fill"></div><div class="vzb-sliver"></div></div>
  <div class="vzb-cap"></div>
</div>
```
- `data-value`: the big number (0–100). `data-tail`: the small remainder shown as the sliver. `data-cap`: the per-row caption after the bold tail number (see rule 3).

### CSS
```css
.vzb-row{margin:0 0 22px;}
.vzb-lab{display:flex; justify-content:space-between; align-items:baseline; margin-bottom:8px;}
.vzb-lab b{font-size:16px; color:var(--viz-ink);}
.vzb-lab span{font-family:var(--viz-mono); font-size:13px; color:var(--viz-muted); font-variant-numeric:tabular-nums;}
.vzb-lab span b{color:var(--viz-accent); font-size:13px;}
.vzb-bar{position:relative; height:26px; background:var(--viz-panel2); border:1px solid var(--viz-line); border-radius:8px; overflow:hidden;}
.vzb-bar .vzb-fill{position:absolute; inset:0 auto 0 0; width:0; background:linear-gradient(90deg,#c98a2e,var(--viz-accent)); transition:width 1.1s cubic-bezier(.2,.7,.2,1);}
.vzb-bar .vzb-sliver{position:absolute; top:0; bottom:0; right:0; width:0; background:var(--viz-danger); transition:width 1.1s cubic-bezier(.2,.7,.2,1);}
.vzb-row.go .vzb-bar .vzb-fill{width:var(--w);}
.vzb-row.go .vzb-bar .vzb-sliver{width:var(--t);}
.vzb-cap{font-size:13.5px; color:var(--viz-muted); margin-top:6px; font-variant-numeric:tabular-nums;}
.vzb-cap b{color:var(--viz-danger);}
@media (prefers-reduced-motion:reduce){
  .vzb-bar .vzb-fill,.vzb-bar .vzb-sliver{transition:none;}
}
```

### JS (copy-paste; pure math up top is unit-testable)
```html
<script>
(function(){
  /* pure, testable */
  function vzbClamp(v){ return Math.min(100, Math.max(0, v)); }
  function vzbMainWidths(value){
    var v = vzbClamp(value);
    return { fill: v, sliver: 100 - v };
  }
  /* DOM wiring */
  var rows = document.querySelectorAll('.vzb-row');
  rows.forEach(function(row){
    var value = parseFloat(row.getAttribute('data-value'));
    var tail  = parseFloat(row.getAttribute('data-tail'));
    if(!(value >= 0)) value = 0;
    if(!(tail >= 0)) tail = 0;
    var m = vzbMainWidths(value);
    row.style.setProperty('--w', m.fill + '%');
    row.style.setProperty('--t', m.sliver + '%');
    var cap = row.getAttribute('data-cap') || '';
    var zc = row.querySelector('.vzb-cap');
    if(zc) zc.innerHTML = '<b>' + tail.toFixed(1) + '</b> ' + cap.replace(/</g, '&lt;');
  });
  function arm(){ rows.forEach(function(r){ r.classList.add('go'); }); }
  if('IntersectionObserver' in window){
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if(e.isIntersecting){ e.target.classList.add('go'); io.unobserve(e.target); }
      });
    }, { threshold: 0.35 });
    rows.forEach(function(r){ io.observe(r); });
  } else { arm(); }
  /* expose pure fns for tests */
  window.__vzb = { main: vzbMainWidths };
})();
</script>
```

### Operating rules
1. **Bars animate once on scroll into view** (IntersectionObserver, 0.35 threshold, unobserve after). Both widths (main fill, sliver) transition together on the same `go` class: `width 1.1s cubic-bezier(.2,.7,.2,1)`. The fill grows left-to-right while the sliver settles in from the right edge — that simultaneous opposing motion is the feel he called out loving (2026-10-09, HERMES). No-JS/no-IO fallback: bars render at full width immediately.
2. **No layout shift**: bar heights are fixed.
3. `prefers-reduced-motion: reduce` kills the width transition.
4. **Per-row captions via `data-cap`** (added 2026-10-09, HERMES). The caption after the bold tail number differs per row ("of every 100 get through" vs "nothing saved. this is the baseline."), so it lives in a `data-cap` attribute, never hardcoded in the JS. The number itself is always `tail.toFixed(1)` in the danger color.

---

## Pattern 2 — Dot-grid simulator

N dots = a population. Scenario buttons re-run which dots "get through," staggered so the eye can follow the change. Generalizes to probability, risk, and funnel visualizations.

### Structure
```html
<div class="vdg" id="dg1">
  <div class="vdg-btns" role="group" aria-label="Scenarios"></div>
  <div class="vdg-grid" aria-hidden="true"></div>
  <div class="vdg-legend"><span><i class="lb"></i>absorbed</span><span><i class="lt"></i>reaches skin</span></div>
  <p class="vdg-cap"></p>
</div>
```

### CSS
```css
.vdg-btns{display:flex; flex-wrap:wrap; gap:8px; margin:0 0 16px;}
.vdg-btns button{font-family:inherit; font-size:14px; font-weight:600; background:var(--viz-panel2); color:var(--viz-ink); border:1px solid var(--viz-line); border-radius:10px; padding:9px 14px; cursor:pointer; touch-action:manipulation;}
.vdg-btns button:active{transform:scale(.97);}
.vdg-btns button[aria-pressed="true"]{border-color:var(--viz-accent); color:var(--viz-accent);}
.vdg-grid{display:grid; grid-template-columns:repeat(10,1fr); gap:7px; max-width:420px; margin:4px auto 6px;}
.vdg-dot{aspect-ratio:1; border-radius:50%; background:#333832; transition:background 160ms, box-shadow 160ms, opacity 160ms;}
.vdg-dot.blocked{background:var(--viz-accent); opacity:.75;}
.vdg-dot.through{background:var(--viz-danger); box-shadow:0 0 10px rgba(224,82,82,.9);}
.vdg-legend{display:flex; justify-content:center; gap:18px; font-size:13px; color:var(--viz-muted); margin:10px 0 2px;}
.vdg-legend i{display:inline-block; width:11px; height:11px; border-radius:50%; margin-right:6px; vertical-align:-1px;}
.vdg-legend .lb{background:var(--viz-accent); opacity:.75;}
.vdg-legend .lt{background:var(--viz-danger); box-shadow:0 0 8px rgba(224,82,82,.9);}
.vdg-cap{font-family:var(--viz-mono); font-size:13px; color:var(--viz-muted); margin:14px 0 0; font-variant-numeric:tabular-nums; min-height:2.4em;}
.vdg-cap b{color:var(--viz-ink);}
@media (max-width:640px){ .vdg-grid{gap:5px;} }
@media (prefers-reduced-motion:reduce){ .vdg-dot{transition:none;} }
```

### JS (copy-paste; pure math up top is unit-testable)
```html
<script>
(function(){
  /* ---------- CONFIG: edit me ---------- */
  var CFG = {
    rootId: 'dg1',
    count: 100,
    staggerBase: 60,   /* ms before first dot flips */
    staggerStep: 7,    /* ms between dots */
    blockedLabel: 'absorbed',
    throughLabel: 'reaches skin',
    scenarios: [
      { id: 'none', label: 'No protection', through: 100 },
      { id: 'a',    label: 'Option A',      through: 3 },
      { id: 'b',    label: 'Option B',      through: 2 }
    ],
    caption: function(sc, through, total){
      return '<b>' + through + ' of ' + total + '</b> get through under ' + sc.label + '.';
    }
  };
  /* ---------- pure, testable ---------- */
  function vdgAssign(through, count){
    var t = Math.min(Math.max(Math.round(through), 0), count);
    var out = [];
    for(var i = 0; i < count; i++) out.push(i < t ? 'through' : 'blocked');
    return out;
  }
  /* ---------- DOM wiring ---------- */
  var root = document.getElementById(CFG.rootId);
  if(!root) return;
  var btnWrap = root.querySelector('.vdg-btns');
  var grid = root.querySelector('.vdg-grid');
  var cap = root.querySelector('.vdg-cap');
  var dots = [];
  for(var i = 0; i < CFG.count; i++){
    var d = document.createElement('span');
    d.className = 'vdg-dot';
    grid.appendChild(d);
    dots.push(d);
  }
  var timers = [];
  function run(id){
    var sc = null;
    CFG.scenarios.forEach(function(s){ if(s.id === id) sc = s; });
    if(!sc) sc = CFG.scenarios[0];
    timers.forEach(clearTimeout); timers = [];
    var classes = vdgAssign(sc.through, CFG.count);
    dots.forEach(function(d){ d.className = 'vdg-dot'; });
    for(var i = 0; i < dots.length; i++){
      (function(i){
        timers.push(setTimeout(function(){
          dots[i].classList.add(classes[i]);
        }, CFG.staggerBase + i * CFG.staggerStep));
      })(i);
    }
    var through = classes.filter(function(c){ return c === 'through'; }).length;
    cap.innerHTML = CFG.caption(sc, through, CFG.count);
    btnWrap.querySelectorAll('button').forEach(function(b){
      b.setAttribute('aria-pressed', b.getAttribute('data-id') === sc.id ? 'true' : 'false');
    });
  }
  CFG.scenarios.forEach(function(s){
    var b = document.createElement('button');
    b.type = 'button';
    b.textContent = s.label;
    b.setAttribute('data-id', s.id);
    b.setAttribute('aria-pressed', 'false');
    btnWrap.appendChild(b);
  });
  btnWrap.addEventListener('click', function(e){
    var b = e.target.closest('button');
    if(b) run(b.getAttribute('data-id'));
  });
  btnWrap.addEventListener('pointerdown', function(e){
    var b = e.target.closest('button');
    if(b) b.style.transform = 'scale(.97)';
  });
  run(CFG.scenarios[0].id);
  window.__vdg = { assign: vdgAssign };
})();
</script>
```

### Operating rules
1. **Timers are always cleared before a re-run** — rapid scenario taps never leave orphaned timeouts painting stale states.
2. **Buttons use `aria-pressed`, not a bare class** — screen readers announce the active scenario.
3. **Press visuals start on `pointerdown`** (the scale transform), selection commits on `click`. Keyboard users get native button behavior for free.
4. **Caption reserves space** (`min-height`) so the staggered run never shifts layout below it.
5. Legend labels come from CONFIG — rename them to the domain (e.g. "converted" / "dropped off").

---

## Pattern 3 — Live formula slider

One slider drives several instantly recomputed readouts plus a dynamic insight line that states the takeaway in words. Generalizes to any what-if calculator.

### Structure
```html
<div class="vfs" id="fs1">
  <input type="range" class="vfs-slider" min="25" max="100" step="1" value="50" aria-label="Percent of recommended amount applied">
  <div class="vfs-read"><b class="vfs-pct">50%</b> of the recommended amount</div>
  <div class="vfs-grid"></div>
  <div class="vfs-insight" aria-live="polite"></div>
  <p class="vfs-foot">*Rough illustrative model. Real-world messiness not included — the point is the shape.</p>
</div>
```

### CSS
```css
.vfs-slider{width:100%; height:34px; background:transparent; cursor:pointer; touch-action:pan-y; margin:4px 0 2px; -webkit-appearance:none; appearance:none;}
.vfs-slider::-webkit-slider-runnable-track{height:4px; border-radius:3px; background:linear-gradient(90deg,var(--viz-danger),var(--viz-accent)); border:1px solid var(--viz-line);}
.vfs-slider::-webkit-slider-thumb{-webkit-appearance:none; appearance:none; width:50px; height:50px; border-radius:50%; border:none; background:radial-gradient(circle,var(--viz-accent) 0 6px,#141311 6px 8px,rgba(0,0,0,0) 9px); margin-top:-23px; filter:drop-shadow(0 1px 3px rgba(0,0,0,.45));}
/* ^ 50px invisible hit box, 16px visible knob with a dark contrast ring baked into the gradient. margin-top = (track 4px - thumb 50px) / 2. drop-shadow (not box-shadow) so the shadow hugs the visible knob. Do NOT use the transparent-border + background-clip trick here: Chromium clips the visible background to a dot. */
.vfs-slider::-moz-range-track{height:4px; border-radius:3px; background:linear-gradient(90deg,var(--viz-danger),var(--viz-accent)); border:1px solid var(--viz-line);}
.vfs-slider::-moz-range-thumb{width:50px; height:50px; border-radius:50%; border:none; background:radial-gradient(circle,var(--viz-accent) 0 6px,#141311 6px 8px,rgba(0,0,0,0) 9px); filter:drop-shadow(0 1px 3px rgba(0,0,0,.45));}
/* ^ Firefox self-centers the thumb; same hit-box trick. */
.vfs-read{text-align:center; font-size:15px; color:var(--viz-muted); margin-bottom:16px;}
.vfs-read .vfs-pct{font-family:var(--viz-mono); font-size:22px; color:var(--viz-ink); font-variant-numeric:tabular-nums;}
.vfs-grid{display:grid; grid-template-columns:repeat(3,1fr); gap:10px;}
.vfs-cell{background:var(--viz-panel2); border:1px solid var(--viz-line); border-radius:12px; padding:14px 8px; text-align:center;}
.vfs-cell b{display:block; font-size:14px; color:var(--viz-ink); margin-bottom:4px;}
.vfs-cell .vfs-num{display:block; font-family:var(--viz-mono); font-size:30px; color:var(--viz-accent); font-variant-numeric:tabular-nums; line-height:1.2;}
.vfs-cell em{display:block; font-style:normal; font-size:11.5px; color:var(--viz-faint); margin-top:2px;}
.vfs-insight{background:rgba(232,163,61,.08); border:1px solid rgba(232,163,61,.35); border-radius:12px; padding:14px 16px; margin:16px 0 4px; font-size:15px; color:var(--viz-ink); min-height:3.2em;}
.vfs-insight b{color:var(--viz-accent);}
.vfs-foot{font-size:13px; color:var(--viz-faint); margin:12px 0 0;}
@media (max-width:640px){ .vfs-cell .vfs-num{font-size:24px;} }
```

### JS (copy-paste; pure math up top is unit-testable)
```html
<script>
(function(){
  /* ---------- CONFIG: edit me ---------- */
  var CFG = {
    rootId: 'fs1',
    decimals: 1,
    unitNote: 'effective SPF*',
    readouts: [
      { id: 'r30', label: 'SPF 30', compute: function(f){ return Math.pow(30, f); } },
      { id: 'r50', label: 'SPF 50', compute: function(f){ return Math.pow(50, f); } },
      { id: 'r60', label: 'SPF 60', compute: function(f){ return Math.pow(60, f); } }
    ],
    /* insight(frac, values[]) -> HTML string; values[i] aligns with readouts[i] */
    insight: function(frac, values){
      if(frac >= 0.999)
        return 'At the full lab amount, the numbers work as advertised. Almost nobody applies this much.';
      var v = values[values.length - 1];
      return 'At ' + Math.round(frac * 100) + '% application, the top option behaves like <b>' +
        v.toFixed(1) + '</b> — input quality beats the label number.';
    }
  };
  /* ---------- pure, testable ---------- */
  function vfsCompute(frac, readouts, decimals){
    return readouts.map(function(r){
      var v = r.compute(frac);
      return { id: r.id, label: r.label, text: v.toFixed(decimals) };
    });
  }
  /* ---------- DOM wiring ---------- */
  var root = document.getElementById(CFG.rootId);
  if(!root) return;
  var slider = root.querySelector('.vfs-slider');
  var pct = root.querySelector('.vfs-pct');
  var grid = root.querySelector('.vfs-grid');
  var insight = root.querySelector('.vfs-insight');
  var cells = CFG.readouts.map(function(r){
    var cell = document.createElement('div');
    cell.className = 'vfs-cell';
    cell.innerHTML = '<b></b><span class="vfs-num"></span><em></em>';
    cell.querySelector('b').textContent = r.label;
    cell.querySelector('em').textContent = CFG.unitNote;
    grid.appendChild(cell);
    return cell.querySelector('.vfs-num');
  });
  function render(){
    var frac = parseInt(slider.value, 10) / 100;
    pct.textContent = slider.value + '%';
    var out = vfsCompute(frac, CFG.readouts, CFG.decimals);
    out.forEach(function(o, i){ cells[i].textContent = o.text; });
    insight.innerHTML = CFG.insight(frac, CFG.readouts.map(function(r){ return r.compute(frac); }));
  }
  slider.addEventListener('input', render);
  render();
  window.__vfs = { compute: vfsCompute };
})();
</script>
```

### Operating rules
1. **`touch-action:pan-y` on the slider** — horizontal drags drive the slider, vertical drags scroll the page. Never `touch-action:none` on a range input.
2. **Recompute on `input`, not `change`** — readouts track the thumb live.
3. **The insight line is the point of the pattern.** It must state the takeaway in one sentence, with the key number in `<b>`. Reserve `min-height` so it never shifts layout.
4. **Label the model honestly** — the footnote names the approximation. Real data or labeled simulation, per family rule 2.
5. **Small knob, big grab** (his Oct 7 calls: the slider should look small and slim, but the grab area stays big). The thumb is a 50px box whose visible knob is only 16px: `background:radial-gradient(circle,var(--viz-accent) 0 6px,#141311 6px 8px,transparent 9px)` — accent core, dark contrast ring, transparent surround, and the whole 50px box grabs. Track is 4px slim; input is 34px tall. Center the knob on the track with `margin-top: (trackHeight − thumbTotal) / 2` (WebKit; Firefox self-centers). Use `filter:drop-shadow(...)` for depth, never `box-shadow` — box-shadow would ring the invisible hit box instead of the knob. Do NOT use the transparent-border + `background-clip` trick for this: Chromium clips the visible background down to a dot. The input keeps `touch-action:pan-y` so track taps land too. Any draggable SVG dot gets an invisible transparent hit halo (2–2.5× the visible radius) drawn under it, positioned with the dot. Chromium does not hit-test fully transparent SVG fills (alpha-0 counts as unpainted under `visiblePainted`), so the halo MUST carry `pointer-events="all"`, and the visible dot must share the same drag listener (it paints over the halo's center). Grab-anywhere: the drag surface itself (svg or track) also responds to pointerdown, so near-misses still move the knob.

---

## Pattern 4 — Estimator + caveat card

A numeric input producing computed estimate rows beside a prominent, always-visible caveat card that overrides the naive reading. Generalizes to any estimate where the model's limits matter more than its output.

### Structure
```html
<div class="ves" id="es1">
  <div class="ves-row">
    <label for="vesIn1">Minutes to redden, no sunscreen:</label>
    <input type="number" id="vesIn1" value="10" min="1" max="180" inputmode="numeric">
  </div>
  <div class="ves-out"></div>
  <div class="ves-card warn">
    <b>Don't trust these numbers past 2 hours.</b>
    <p>"SPF 60 × 10 minutes = 10 hours" is lab arithmetic on a perfect, undisturbed film. In real life the film is never perfect. Reapply every 2 hours no matter what the bottle promises.</p>
  </div>
</div>
```

### CSS
```css
.ves-row{display:flex; align-items:center; gap:12px; flex-wrap:wrap; margin:4px 0 16px;}
.ves-row label{font-size:15px; color:var(--viz-muted);}
.ves-row input[type=number]{font-family:var(--viz-mono); font-size:16px; width:88px; background:var(--viz-bg); color:var(--viz-ink); border:1px solid var(--viz-line); border-radius:10px; padding:10px 12px;}
.ves-row input[type=number]:focus{outline:none; border-color:var(--viz-accent);}
.ves-out{display:grid; gap:10px;}
.ves-brow{display:flex; justify-content:space-between; align-items:baseline; background:var(--viz-panel2); border:1px solid var(--viz-line); border-radius:12px; padding:13px 16px;}
.ves-brow b{font-size:15px; color:var(--viz-ink);}
.ves-brow .ves-t{font-family:var(--viz-mono); font-size:15px; color:var(--viz-accent); font-variant-numeric:tabular-nums;}
.ves-brow .ves-t small{color:var(--viz-faint); font-size:12px;}
.ves-card{background:var(--viz-panel); border:1px solid var(--viz-line); border-radius:14px; padding:22px; margin:20px 0 4px;}
.ves-card.warn{border-color:rgba(224,82,82,.45); background:rgba(224,82,82,.06);}
.ves-card.warn > b{color:var(--viz-danger); font-size:16px;}
.ves-card p{margin:8px 0 0; font-size:15px; color:var(--viz-muted);}
```

### JS (copy-paste; pure math up top is unit-testable)
```html
<script>
(function(){
  /* ---------- CONFIG: edit me ---------- */
  var CFG = {
    rootId: 'es1',
    min: 1, max: 180, fallback: 10,
    rows: [
      { label: 'SPF 30', compute: function(base){ return Math.round(base * 30); } },
      { label: 'SPF 50', compute: function(base){ return Math.round(base * 50); } },
      { label: 'SPF 60', compute: function(base){ return Math.round(base * 60); } }
    ]
  };
  /* ---------- pure, testable ---------- */
  function vesClampBase(raw, cfg){
    var b = parseFloat(raw);
    if(!(b > 0)) b = cfg.fallback;
    if(b > cfg.max) b = cfg.max;
    if(b < cfg.min) b = cfg.min;
    return b;
  }
  function vesFmtMins(mins){
    mins = Math.round(mins);
    if(mins < 60) return mins + ' min';
    var h = Math.floor(mins / 60), m = mins % 60;
    return m === 0 ? h + ' hr' : h + ' hr ' + m + ' min';
  }
  /* ---------- DOM wiring ---------- */
  var root = document.getElementById(CFG.rootId);
  if(!root) return;
  var inp = root.querySelector('input[type=number]');
  var out = root.querySelector('.ves-out');
  var spans = CFG.rows.map(function(r){
    var row = document.createElement('div');
    row.className = 'ves-brow';
    row.innerHTML = '<b></b><span class="ves-t"></span>';
    row.querySelector('b').textContent = r.label;
    out.appendChild(row);
    return row.querySelector('.ves-t');
  });
  function render(){
    var base = vesClampBase(inp.value, CFG);
    CFG.rows.forEach(function(r, i){
      var mins = r.compute(base);
      spans[i].innerHTML = '<b style="font-size:17px">' + vesFmtMins(mins) +
        '</b> <small>theoretical · ' + mins + ' min</small>';
    });
  }
  inp.addEventListener('input', render);
  render();
  window.__ves = { clamp: vesClampBase, fmt: vesFmtMins };
})();
</script>
```

### Operating rules
1. **The caveat card is always visible, never conditional** — the pattern's whole point is that the warning outranks the numbers. Never hide it behind a toggle.
2. **Sanitize the input**: non-numeric/empty → fallback, over max → clamp to max, under min → clamp to min. Never render `NaN`.
3. **Number input is 16px** (iOS zoom rule) with `inputmode="numeric"`.
4. **Format long durations humanely** — "10 hr", not "600 min".
5. Recompute on `input` for live feedback as the user types.

---

## Pattern 5 — Source link-out cards

Stacked cards for a Sources section. Each card names the source type up top (badge with a bespoke icon), gives the title the full width, and puts citation details in a quiet caption line. Born 2026-10-09 on the HERMES visualizer: the first version squeezed the title and metadata into two side-by-side columns and both wrapped badly at 390px. The stacked version reads clean at any width. No JS — pure HTML/CSS.

### Structure
```html
<ul class="vsc-list">
  <li><a href="https://arxiv.org/abs/2610.07832">
    <span class="vsc-head">
      <span class="vsc-kind"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4"/></svg>arXiv paper</span>
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 17L17 7"/><path d="M8 7h9v9"/></svg>
    </span>
    <span class="vsc-title">Harness Engineering for Software Engineering via Modular Executable Dev-Primitives</span>
    <span class="vsc-meta">Jin et al. &middot; UIUC / Penn State &middot; arXiv:2610.07832 &middot; submitted 6 Oct 2026</span>
  </a></li>
  <li><a href="https://x.com/omarsar0/status/2108360049848717588">
    <span class="vsc-head">
      <span class="vsc-kind"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231 5.451-6.231zm-1.161 17.52h1.833L7.084 4.126H5.117l11.966 15.644z"/></svg>X post</span>
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 17L17 7"/><path d="M8 7h9v9"/></svg>
    </span>
    <span class="vsc-title">The X post that surfaced it</span>
    <span class="vsc-meta">@omarsar0 &middot; 8 Oct 2026</span>
  </a></li>
</ul>
```

### CSS
```css
.vsc-list{list-style:none; margin:12px 0 0; padding:0; display:grid; gap:10px;}
.vsc-list a{display:block; background:var(--viz-panel2); border:1px solid var(--viz-line);
  border-radius:14px; padding:16px; color:var(--viz-ink); text-decoration:none; touch-action:manipulation;}
.vsc-list a:active{transform:scale(.99);}
.vsc-head{display:flex; align-items:center; justify-content:space-between; gap:10px; margin-bottom:10px;}
.vsc-kind{display:inline-flex; align-items:center; gap:7px; font-family:var(--viz-mono); font-size:11px;
  letter-spacing:.12em; text-transform:uppercase; color:var(--viz-accent);}
.vsc-kind svg{width:15px; height:15px;}
.vsc-head > svg{flex:none; width:15px; height:15px; color:var(--viz-muted);}
.vsc-title{display:block; font-size:16.5px; font-weight:600; line-height:1.35;}
.vsc-meta{display:block; margin-top:8px; font-size:13px; color:var(--viz-faint);}
```

### Icon set
- **Document** (paper, blog post, docs): folded-corner page, 1.9px stroke, round caps, `currentColor`.
- **X post**: X logo glyph (fill, `currentColor`).
- **Arrow**: the standard link-out arrow from cross-pattern rule 6 (15px, `currentColor`, muted).
- New kinds pair one bespoke icon with a mono uppercase label: icon at 15px, label at 11px letterspaced. Never emoji.

### Operating rules
1. **Stacked, never side-by-side.** The title always gets the full width; metadata is a caption below it. Two-column source cards wrap badly on phones.
2. **The badge names the source type, not the site.** "arXiv paper", "X post", "Docs", "Video" — the reader knows what they're opening before reading the title.
3. **Meta line is one breath**: authors · venue · id · date, separated with `&middot;`. Never a second paragraph.
4. **The whole card is the tap target** (`display:block` on the anchor), `touch-action:manipulation`, `:active` scale. No nested interactive elements inside.
5. Link the exact page, not a homepage (cross-pattern rule 7 applies: verify the destination before shipping).

---

## Pattern 6 — Live mic visualizer

A tap-to-start microphone button driving two live canvases: a thin raw-waveform strip on top and a scrolling waterfall spectrogram below (x = time scrolling left, y = frequency, color = intensity). Born 2026-10-11 on the voice-ai primer ("speak into it and see it on the website"). The FFT runs entirely on-device; the recipe contains no network code at all.

### Structure
```html
<div class="vmv" id="mv1">
  <button type="button" class="vmv-btn" aria-pressed="false">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0"/><path d="M12 18v3"/></svg>
    <span class="vmv-btnlabel">Tap to speak</span>
  </button>
  <p class="vmv-status" aria-live="polite"></p>
  <canvas class="vmv-wave" role="img" aria-label="Live microphone waveform"></canvas>
  <canvas class="vmv-spec" role="img" aria-label="Live scrolling spectrogram"></canvas>
  <p class="vmv-cap"></p>
  <p class="vmv-priv">Analyzed on your device, never uploaded.</p>
</div>
```

### CSS
```css
.vmv{margin:14px 0;}
.vmv-btn{display:inline-flex; align-items:center; gap:10px; font-family:inherit; font-size:16px; font-weight:600;
  background:var(--viz-panel2); color:var(--viz-ink); border:1px solid var(--viz-line); border-radius:999px;
  padding:12px 20px; cursor:pointer; touch-action:manipulation;}
.vmv-btn svg{width:20px; height:20px;}
.vmv-btn:active{transform:scale(.97);}
.vmv-btn[aria-pressed="true"]{border-color:var(--viz-danger); color:var(--viz-danger);}
.vmv-status{font-size:14px; color:var(--viz-muted); margin:10px 0 0; min-height:1.4em;}
.vmv canvas{display:block; width:100%; border:1px solid var(--viz-line); border-radius:12px; background:#0f0e0c;}
.vmv-wave{height:56px; margin:10px 0 8px;}
.vmv-spec{height:180px;}
.vmv-cap{font-size:14px; color:var(--viz-muted); margin:10px 0 0;}
.vmv-priv{font-size:13px; color:var(--viz-faint); margin:6px 0 0;}
```

### JS (copy-paste; CONFIG block at the top, pure heat-scale fn is unit-testable)
```html
<script>
(function(){
  /* ---------- CONFIG: edit me ---------- */
  var CFG = {
    rootId: 'mv1',
    fftSize: 2048,
    waveCssH: 56,
    specCssH: 180,
    /* heat scale stops: [t, [r,g,b]], paper -> accent */
    heat: [[0,[246,241,227]],[0.45,[232,163,61]],[1,[179,53,43]]],
    startLabel: 'Tap to speak',
    stopLabel: 'Tap to stop',
    restartLabel: 'Tap to speak again',
    deniedMsg: 'Microphone is blocked. Open this page in Safari and try again.',
    noMicMsg: 'No microphone found.'
  };
  /* ---------- pure, testable ---------- */
  function vmvHeat(t, stops){
    t = Math.min(1, Math.max(0, t));
    for(var i = 1; i < stops.length; i++){
      if(t <= stops[i][0]){
        var f = (t - stops[i-1][0]) / Math.max(1e-6, stops[i][0] - stops[i-1][0]);
        var a = stops[i-1][1], b = stops[i][1];
        return 'rgb(' + Math.round(a[0]+(b[0]-a[0])*f) + ',' + Math.round(a[1]+(b[1]-a[1])*f) + ',' + Math.round(a[2]+(b[2]-a[2])*f) + ')';
      }
    }
    var l = stops[stops.length-1][1];
    return 'rgb(' + l[0] + ',' + l[1] + ',' + l[2] + ')';
  }
  /* ---------- DOM wiring ---------- */
  var root = document.getElementById(CFG.rootId);
  if(!root) return;
  var btn = root.querySelector('.vmv-btn');
  var btnLabel = root.querySelector('.vmv-btnlabel');
  var status = root.querySelector('.vmv-status');
  var waveC = root.querySelector('.vmv-wave');
  var specC = root.querySelector('.vmv-spec');
  var waveX = waveC.getContext('2d');
  var specX = specC.getContext('2d');
  var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var ctx = null, stream = null, analyser = null, raf = 0, timer = 0;
  var running = false, everStarted = false;
  var freqData = null, timeData = null;

  function fit(){
    var dpr = window.devicePixelRatio || 1;
    [[waveC, CFG.waveCssH],[specC, CFG.specCssH]].forEach(function(p){
      var w = p[0].clientWidth;
      p[0].width = Math.max(1, Math.round(w * dpr));
      p[0].height = Math.max(1, Math.round(p[1] * dpr));
    });
  }
  function drawWave(){
    var w = waveC.width, h = waveC.height, dpr = window.devicePixelRatio || 1;
    analyser.getByteTimeDomainData(timeData);
    waveX.fillStyle = '#0f0e0c';
    waveX.fillRect(0, 0, w, h);
    waveX.strokeStyle = '#e8a33d';
    waveX.lineWidth = Math.max(1, dpr);
    waveX.beginPath();
    for(var i = 0; i < timeData.length; i++){
      var x = (i / (timeData.length - 1)) * w;
      var y = ((timeData[i] - 128) / 128) * (h * 0.42) + h / 2;
      if(i === 0) waveX.moveTo(x, y); else waveX.lineTo(x, y);
    }
    waveX.stroke();
  }
  function drawSpec(){
    var w = specC.width, h = specC.height;
    var step = Math.max(2, Math.round(window.devicePixelRatio || 1));
    analyser.getByteFrequencyData(freqData);
    specX.drawImage(specC, -step, 0); /* scroll existing image left */
    var bins = analyser.frequencyBinCount;
    for(var y = 0; y < h; y++){
      var bin = Math.floor((1 - y / h) * (bins - 1)); /* bin 0 (bass) at the bottom */
      specX.fillStyle = vmvHeat(freqData[bin] / 255, CFG.heat);
      specX.fillRect(w - step, y, step, 1);
    }
  }
  function tick(){
    if(!running) return;
    drawWave();
    drawSpec();
    if(reduced) timer = setTimeout(tick, 500); /* ~2fps under reduced motion */
    else raf = requestAnimationFrame(tick);
  }
  function setRunning(on){
    running = on;
    btn.setAttribute('aria-pressed', on ? 'true' : 'false');
    btnLabel.textContent = on ? CFG.stopLabel : (everStarted ? CFG.restartLabel : CFG.startLabel);
  }
  function stop(say){
    if(raf) cancelAnimationFrame(raf);
    if(timer) clearTimeout(timer);
    raf = 0; timer = 0;
    if(stream){ stream.getTracks().forEach(function(t){ t.stop(); }); stream = null; }
    if(ctx){ ctx.suspend(); }
    analyser = null;
    setRunning(false);
    if(say) status.textContent = say;
  }
  btn.addEventListener('click', function(){
    if(running){ stop('Tap to speak again.'); return; }
    if(!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia){
      status.textContent = CFG.noMicMsg;
      return;
    }
    status.textContent = '';
    navigator.mediaDevices.getUserMedia({audio:{echoCancellation:true, noiseSuppression:true}}).then(function(s){
      stream = s;
      var AC = window.AudioContext || window.webkitAudioContext;
      ctx = new AC();
      if(ctx.state === 'suspended') ctx.resume(); /* iOS: resume inside the gesture */
      var src = ctx.createMediaStreamSource(stream);
      analyser = ctx.createAnalyser();
      analyser.fftSize = CFG.fftSize;
      src.connect(analyser);
      freqData = new Uint8Array(analyser.frequencyBinCount);
      timeData = new Uint8Array(analyser.fftSize);
      everStarted = true;
      fit();
      setRunning(true);
      tick();
    }, function(){
      status.textContent = CFG.deniedMsg; /* never throws to console */
    });
  });
  window.addEventListener('resize', fit);
  fit();
  /* expose pure fn for tests */
  window.__vmv = { heat: vmvHeat };
})();
</script>
```

### Operating rules
1. **AudioContext is created and resumed inside the tap gesture.** iOS will not start audio outside a user gesture; creating it earlier leaves it suspended forever.
2. **Stop everything on end.** Stop all tracks, suspend the context, cancel the frame loop. A leaked stream keeps the browser's recording indicator on.
3. **On-device only, and say so.** The recipe contains no network code at all. Keep the "Analyzed on your device, never uploaded." caption next to the widget so the reader knows.
4. **Deny gracefully.** The widget renders and lays out fine with no mic. Permission denial names the fix ("Open this page in Safari and try again"): pages opened in an iOS bottom-sheet webview can have mic permission blocked, and the denied state covers it. Never throw to console; show messages in the status line.
5. **Reduced motion throttles to ~2fps** instead of the full-rate loop.
6. **Canvases are devicePixelRatio-aware** and re-fit on resize; the waterfall scrolls in device pixels so it stays crisp.

### QA notes
- Playwright cannot provide a real mic: stub `getUserMedia` to resolve with a fake stream for the running state and to reject with a DOMException for the denied state.
- Assert the button label/state flips (idle → running → "tap to speak again"), both canvases paint non-blank frames (sample pixels), the denied message appears with no pageerrors, and 390px layout holds (`scrollWidth <= 390`).
- Screenshot idle, running, and denied states at full size and review them.

---

## Cross-pattern operating rules
1. Each script is an IIFE with a CONFIG block at the top — adapt by editing CONFIG, never the wiring.
2. IDs are per-instance (`dg1`, `fs1`, `es1`, `mv1`); duplicate a pattern on one page by copying the block and changing the IDs + CONFIG `rootId`.
3. All four scripts are inert if their root element is missing (`if(!root) return`) — safe to include page-wide.
4. Colors come from the shared theme block; the danger/accent semantics (`--viz-accent` = majority/good, `--viz-danger` = the sliver/warning) stay consistent across patterns on a page.
5. **Stepper navigation: edge-straddling circle arrows, never a button row** (evolved 2026-10-08 to 2026-10-09: the Taylor sheet hid terminal buttons instead of disabling them; the ai-bank-heist stepper pinned Next with `margin-left:auto` and locked content height; the sidecar post replaced the Next/Back pill row with gutter arrows, which Luke preferred, then refined four times: no overlaying content, no height lock, bare chevrons, then back to circles straddling the card edge and nudged lower, the classic carousel look). Final spec: 46px circles with bespoke SVG chevrons (22px, `currentColor`, round caps), dark translucent fill + border + subtle shadow, straddling the card's left/right edges (half in, half out: `left:-23px` / `right:-23px`), pinned with a FIXED `top` offset from the card's top edge (not `top:50%`): the card's top never moves between steps, so the arrows can't bounce even though each step sizes to its natural height. **Arrow vertical anchor (his 2026-10-10 call):** the arrows sit at the vertical midway of an anchor card, fixed for all steps. Measure every step card's natural height at init (reset min-height first, paint each step, record offsetHeight, restore). Anchor = the first card, unless the first card is significantly taller than the smallest card (over 1.5x), in which case the anchor is the smallest card. Every card gets `min-height` = anchor height, so shorter cards grow to meet it and taller cards keep their natural height. Arrows get `top` = card.offsetTop + anchorH/2 - 23 (46px circle), set once via JS. Re-run the measurement on resize (debounced) and on `document.fonts.ready`. `touch-action:manipulation`; `:active` scale. Terminal arrows are `display:none`, never disabled. Keep: the dots + count row and arrow-key support with the standard guards. Verify: each arrow's bounding box identical across all steps where visible; arrow sits at the anchor card's vertical midway; no horizontal page overflow from the overhang at 390px; zero drift while spamming through every step.
6. **Cross-article buttons carry a link-out icon** (his 2026-10-08 call). Any button or card that navigates to a different post gets a small bespoke external-link SVG icon (inline, `currentColor`, ~14px, never emoji), so it's obvious the tap leaves the page rather than interacting with the visualizer. Applies to all Keep Exploring cards and in-post cross-links.
7. **Cite sources for factual claims** (his 2026-10-08 call). Every claim about how a real system works, every number, every named paper/benchmark/model gets a source: inline links or a Sources section at the end of the post. Verify against primary sources (official docs, system cards, the paper itself) before shipping, never from memory. Link the exact page, not a homepage.
8. **Step-through widgets get left/right arrow keys** (his 2026-10-08 call on the lean-proofs stepper). ArrowLeft/ArrowRight move back/forward through steps. Guards, in this order: bail on any modifier key (alt/ctrl/meta/shift); bail if the event target is a textarea, input, select, or contentEditable (editors keep their caret keys); bail if the target sits inside a horizontally scrolling code block (arrows must keep scrolling it); bail unless the widget is at least partly on screen (no invisible step changes while the reader is elsewhere). Clamp at both ends: arrows never go past the first or last step. `preventDefault()` only on handled keys.
```js
document.addEventListener('keydown', function (e) {
  if (e.altKey || e.ctrlKey || e.metaKey || e.shiftKey) return;
  if (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return;
  var t = e.target, tag = t && t.tagName;
  if (tag === 'TEXTAREA' || tag === 'INPUT' || tag === 'SELECT' || (t && t.isContentEditable)) return;
  if (t && t.closest && t.closest('.step-code')) return;
  var r = stepperEl.getBoundingClientRect();
  if (r.bottom < 0 || r.top > window.innerHeight) return;
  if (e.key === 'ArrowLeft' && i > 0) { i--; render(); e.preventDefault(); }
  else if (e.key === 'ArrowRight' && i < steps.length - 1) { i++; render(); e.preventDefault(); }
});
```
9. **Explainer bubbles rotate through tips** (his 2026-10-08 call on the lean-proofs stepper). Highlighted keywords in code carry 5 tips each, not one: every view (hover or tap) shows the next tip and cycles back after the fifth. Tips[0] is the plain definition; later tips go one level deeper, each teaching exactly one new thing in one breath. No "n of m" counter on the bubble; the rotation is discovered by re-visiting. Interaction model: hover shows and mouse-leave hides (desktop); a tap pins the currently shown tip instead of advancing (touch fires an emulated hover before the click, so re-showing would skip a tip); a second tap on the same keyword dismisses. Keep each tip jargon-light and em-dash-free.
```js
var TAC_HELP = {
  'have': ['Proves a helper fact right now and names it...', 'You can skip the name...',
           'have is how long proofs stay readable...', 'have h : P := ... is the most common shape...',
           'Chain them: each have can use the names from earlier haves...']
  /* ... 5 tips per keyword; definition first ... */
};
var tacSeen = {};
function showBubble(anchor, tac) {
  var tips = TAC_HELP[tac];
  if (!tips) return;
  var n = tacSeen[tac] || 0;
  bubbleName.textContent = tac;
  bubbleText.textContent = tips[n % tips.length];
  tacSeen[tac] = n + 1;
  /* ... position and show ... */
}
code.addEventListener('click', function (e) {
  var t = e.target && e.target.closest ? e.target.closest('.tk-tac') : null;
  if (!t) return;
  e.stopPropagation();
  var tac = t.getAttribute('data-tac');
  var same = !bubble.hasAttribute('hidden') && bubbleTac === tac && bubbleAnchor === t;
  if (same && bubbleMode === 'click') { hideBubble(); return; }
  if (same) { bubbleMode = 'click'; return; }  // pin; the tap's emulated hover already showed it
  showBubble(t, tac);
  bubbleMode = 'click';
});
code.addEventListener('mouseover', function (e) {
  var t = e.target && e.target.closest ? e.target.closest('.tk-tac') : null;
  if (!t || bubbleMode === 'click') return;  // a pinned bubble stays until dismissed
  showBubble(t, t.getAttribute('data-tac'));
  bubbleMode = 'hover';
});
```
10. **Step-through means click-per-step, never auto-play** (his 2026-10-09 call on the pocket-test race: "I hate the run pattern where you click and wait"). No "Run" / "Play" button that animates the whole sequence on a timer while the reader watches. Every step advances on an explicit user action: a Next button, a tap on the widget, or arrow keys (rule 8). One click = one step. The reader controls the pace; the widget never moves on its own. The final tap reveals the end state; offer a replay affordance that resets to step 0 instead of replaying automatically. This applies to every step-through, race, and timeline widget going forward.
11. **Research uses the most modern papers available** (his 2026-10-09 call). When a post needs research, find the latest peer-reviewed papers on the topic, not the most-cited classics. Check publication dates; a 2025 paper beats a 2018 paper on the same finding. Prefer primary sources (the paper itself, official data) over news summaries of the paper. If newer research updates or contradicts an older finding, the newer one wins and the post says so. Every factual claim still gets its exact source link (rule 7).
12. **Speed comparisons get bouncing balls, not static bars** (his 2026-10-10 call: "add this bouncing balls to my visualizers skill pls when it comes to showing speed", from tov.sh). When a visualizer compares speeds (benchmarks, latencies, throughput), each row gets a ball that ping-pongs along its track forever, at a pace proportional to the measured value. The motion IS the data: a faster ball means a faster system, readable at a glance without parsing numbers. This does not conflict with rule 10 (click-per-step): rule 10 covers step-throughs where the reader follows a sequence. Bouncing balls are ambient; the reader never waits on them and there is no sequence to control. If a widget has both a sequence and a speed comparison, rule 10 wins.
```css
.race-track{position:relative; height:22px; background:var(--viz-panel2);
  border:1px solid var(--viz-line); border-radius:999px; overflow:hidden;}
.race-ball{position:absolute; top:50%; left:0; width:16px; height:16px; margin-top:-8px;
  border-radius:50%; background:#dcdce0;
  animation:race-bounce var(--t,1s) linear infinite alternate;}
.race-ball.fast{background:var(--viz-accent); box-shadow:0 0 10px rgba(232,163,61,.55);}
@keyframes race-bounce{
  0%{left:0; transform:scale(.72,1.25);}            /* squash into the wall */
  8%{transform:scale(1,1);}
  92%{transform:scale(1,1);}
  100%{left:calc(100% - 16px); transform:scale(.72,1.25);}
}
@media (prefers-reduced-motion:reduce){ .race-ball{animation:none; left:calc(100% - 16px);} }
```
```js
// Per-lane duration: fastest lane is 0.9s, the rest scale by the speed ratio.
// Cap the slowest at ~9s so it reads as slow, not frozen.
lanes.forEach(function(l){
  var t = 0.9 * (vmax / l.v);
  l.ball.style.setProperty('--t', Math.min(t, 9).toFixed(2) + 's');
});
```
Operating rules: row layout is label left, track middle, right-aligned value column (bold figure + small caption). The fastest row gets the accent ball (plus glow), a bold label, and an accent caption ("fastest"); every other row gets a muted gray ball and a gray relative caption ("12% slower", "2.2× slower"). Balls in tabbed boards restart from the left wall on tab switch (hiding with `display:none` resets the animation), which is the desired behavior. Honor `prefers-reduced-motion`: balls sit still at the finished position and the numbers carry the comparison. Verify: balls visibly move at different paces matching the value ratios (spot-check two lanes with a stopwatch if the ratios are close); the squash reads at both walls; nothing shifts layout while they run.
13. **Any drag/touch interaction gets the bottom-sheet-drag-lock treatment** (his 2026-10-10 call on yuru-ink: downward drags on the artwork were also dragging the native bottom sheet). These pages are opened inside a native bottom-sheet webview; a downward drag on the page yanks the whole sheet instead of reaching the interaction. Whenever a visualizer has a touch or drag surface, apply all four parts of `~/workspace/skills/bottom-sheet-drag-lock/SKILL.md`: (1) lock the page to the viewport (`position:fixed; inset:0; overscroll-behavior:none; overflow:hidden` on html/body), (2) `touch-action:none` on the drag surface, (3) non-passive `touchmove` + `preventDefault` (document-level for full-viewport pages with nothing scrollable, scoped to the surface otherwise), (4) block `gesturestart`. Tap targets keep `touch-action:manipulation`. This was missed on yuru-ink's first touch pass and had to be repaired after he reported it; do it in the same edit that adds the interaction, not after.
14. **Ignore input during transition animations** (found 2026-10-10 on the ai-memory primer's compaction animation: rapid taps mid-animation raced the state machine and stranded it). While a widget is mid-transition, its input handlers ignore new taps/clicks until the transition completes — a second interaction must never start from a half-rendered state. Implement with an `animating` flag checked at the top of every input handler, cleared on `transitionend` with a timeout fallback. Verify with rapid-tap Playwright spam: no stranded states, no double-applied steps, zero pageerrors.

## QA checklist (run before calling it done)- Zoom bars: scroll each row into view → bars animate once to the exact configured widths; zoom tag reads the computed factor ("zoomed 20×"); with JS disabled, bars still render (graceful: add `go` class server-side or accept static full widths).
- Dot grid: tap each scenario → exactly the configured number of dots flip, staggered, caption updates, `aria-pressed` follows; rapid taps don't strand timers.
- Slider: drag thumb → all readouts update live; insight line states the takeaway; at min/max the math stays sane; vertical page scroll still works on mobile.
- Estimator: type garbage/empty/huge values → sane fallback/clamp, never NaN; caveat card visible without scrolling on mobile.
- Source cards: at 390px the badge row, title, and meta stack with no overlap or cramped columns; the whole card taps through to the exact linked page; badge icons render (no missing-glyph boxes).
- Race balls: lanes move at visibly different paces matching the value ratios; squash reads at both walls; with reduced-motion the balls sit still; tab switches restart the race from the left.
- Mic visualizer: stub getUserMedia (resolve fake stream / reject denied) → button flips idle/running/"tap to speak again", both canvases paint non-blank frames, denied message shows, no pageerrors; idle/running/denied screenshots reviewed at full size.
- 390×844: no horizontal overflow in any pattern; dots stay circular; slider thumb reachable.
- Zero console errors.
