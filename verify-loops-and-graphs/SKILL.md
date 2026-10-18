---
name: verify-loops-and-graphs
description: Verify the loops-and-graphs primer (lukezhang.si/blog/loops-and-graphs/, "Loops and Graphs: Approve Only the Last Step") against its feature map by running the Playwright harness, which drives the real UI (mechanism cards, the loop panel stepper with gestures, the edge-audit graph lab, the return simulator, the timeline) and asserts computed styles, rendered geometry, and the primer's verified arithmetic.
---

# Verify Loops and Graphs

Feature map: `~/workspace/blog-drafts/loops-and-graphs/verify/FEATURE_MAP.md`
Harness: `~/workspace/blog-drafts/loops-and-graphs/verify/verify.py` (local port 8938)

Run it:

```
python3 ~/workspace/blog-drafts/loops-and-graphs/verify/verify.py            # local draft
```

Live URL runs fail in this VM (ERR_TUNNEL_CONNECTION_FAILED); verify live by curl 200s plus served bytes = draft + 248.

Invariants the harness guards:
- Arithmetic: the edge-audit lab starts at a 45 minute wall clock and recomputes the critical path to 35, 25, then 15 minutes (3.0x) as the three habit arrows are cut, with total work fixed at 45. The return simulator's seeded Monte Carlo averages sit near the exact formulas (at p = 0.75: unit 5.33, batch 12.64; caption prints those expectations and the 31.6 percent all-pass round). At p = 0.90 the caption expectations read 4.44 and 6.10.
- Steppers: the loop stepper has exactly 6 panels and 6 notes' worth of steps, dots and count agree, terminal arrows are display:none (never disabled), the next arrow's bounding box is identical across steps, and dispatched-pointer swipes move exactly one step each way. The timeline has 7 entries with the same arrow discipline.
- Cards and components: 6 mechanism cards (third toggles through its real header), chevron SVG at 20px, 7 voices, 3 agree camps, 3 split camps, 5 takeaway bullets, 3 keep-exploring links with 14px link-out icons, 8 sources.
- KaTeX stylesheet loaded and .katex-mathml computed position absolute (the rotation-matrices lesson); both display formulas render.
- css_audit: `python3 ~/workspace/tools/css_audit.py index.html` with the draft's css-audit-allow.txt (copied from feel-physics: cards, fhead, voices, xicon, meta, nokatex, fn, tl) must stay at 0 unexplained orphans.
