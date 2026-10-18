---
name: verify-one-line-machine
description: Verify the one-line-machine primer (lukezhang.si/blog/one-line-machine/, "One Line In, a Machine Out") against its feature map by running the Playwright harness, which drives the real UI (the live isometric plate recreation with its seven stop tour, brew, explode slider, drag and swipe; mechanism cards; the audit stepper; the timeline) and asserts computed styles, rendered geometry, and the engine's math against hand computed values.
---

# Verify One Line In, a Machine Out

Feature map: `~/workspace/blog-drafts/one-line-machine/verify/FEATURE_MAP.md`
Harness: `~/workspace/blog-drafts/one-line-machine/verify/verify.py` (local port 8941)

Run it:

```
python3 ~/workspace/blog-drafts/one-line-machine/verify/verify.py            # local draft
```

Live URL runs fail in this VM (ERR_TUNNEL_CONNECTION_FAILED); verify live by curl 200s plus served bytes = draft + 248.

The page's centerpiece is an independent isometric recreation of Ann Nguyen's Anatomy reveal video. Its numbers must be genuinely computed by the running code: the engine's projection of the machine's top front corner (190, 207.5, 470) at 45 degrees yaw must match the hand worked Figure 2 values (sx about -12.37, sy about -221.5); the needle formula must give exactly 16.875 degrees at 9 bar, -135 at 0, 135 at 16; the parts list must count 33 parts in 8 assemblies and the exploded caption must print those counts, not the video's claimed 82 and 44.

Invariants the harness guards:
- Plate: renders more than 120 faces; spin changes the rendered SVG between two samples; drag rotates without stepping the tour; a fast swipe steps it; terminal tour arrows hide.
- Gauge stop auto brews to above 7.5 bar; the slider drives explode above 0.95; readout chips show pressure, needle, and the live counts.
- Mechanism cards: 6, a middle card toggles through its real header, chevron SVG renders at 20px.
- Audit stepper: 6 rows reveal cumulatively, tap and swipe step it, terminal next hides, score line ends at 2 standard facts and 2 model-authored.
- Timeline: 8 events, tap and swipe step it, terminal next hides.
- KaTeX stylesheet loaded and .katex-mathml hidden (the rotation-matrices lesson).
- css_audit: `python3 ~/workspace/tools/css_audit.py index.html` with the draft's css-audit-allow.txt (cards, fhead, voices, xicon, meta, nokatex, fn, tl), currently 0 unexplained orphans.
