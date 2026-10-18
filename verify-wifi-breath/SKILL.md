---
name: verify-wifi-breath
description: Verify the Wi-Fi breathing primer (lukezhang.si/blog/wifi-breath/, "Your Wi-Fi Can Hear You Breathe") against its feature map by running the Playwright harness, which drives the real UI (mechanism cards, breathing lab with real band-pass filtering and zero-crossing rate count, phasor stepper with gestures, Fresnel explorer drag, timeline) and asserts computed styles, geometry, and the lab's measured readouts.
---

# Verify Your Wi-Fi Can Hear You Breathe

Feature map: `~/workspace/blog-drafts/wifi-breath/verify/FEATURE_MAP.md`
Harness: `~/workspace/blog-drafts/wifi-breath/verify/verify.py` (local port 8931)

Run it:

```
python3 ~/workspace/blog-drafts/wifi-breath/verify/verify.py            # local draft
```

Live URL runs fail in this VM (ERR_TUNNEL_CONNECTION_FAILED); verify live by curl 200s plus served bytes = draft + 248.

The page's numbers are arithmetic, and the harness guards them: a 5 mm chest rise is a 10 mm path change, which is 60.0 degrees of phase at 5 GHz (wavelength 59.96 mm) and 28.8 degrees at 2.4 GHz; the first Fresnel zone radius at the midpoint of a 4 m link at 5 GHz is 24.5 cm. The lab is a labeled simulation, but its processing is real: a two-pole biquad band pass (high-pass corner 0.08 Hz, low-pass corner 0.6 Hz) and a hysteresis zero-crossing counter over a 20 s window; the harness waits for the measured readout to land within 9 to 15 brpm at the 12 brpm default, checks the filter-off state labels itself noise, and checks that Hold breath drives the readout to "no breath detected" (recent 3 s amplitude under threshold).

Invariants the harness guards:
- KaTeX stylesheet loaded and .katex-mathml computed position absolute (the rotation-matrices lesson); at least 3 rendered equations, each with an adjacent .legend.
- Mechanism cards: 6, third card opens and closes through its real header, chevron bounding box at most 28px, card body computed display block at 15.5px.
- Phase stepper: 5 steps, arrows exactly 46px, arrow vertical center within 3px of the canvas center, terminal arrows display:none, tap advances, dispatched-pointer swipes move exactly one step each way.
- Worked example stepper (rebuilt 2026-10-15 from five prose paragraphs at Luke's screenshot call): 5 steps, one inline SVG visual and one large headline number per step (24.5 cm, 5 mm to 10 mm, 60.0 degrees with the arithmetic line visible, 0.2 Hz, 6 breaths in 30 s), arrows exactly 46px centered on the card within 3px, terminal arrows display:none, tap and swipe move one step, guarded arrow keys move one step, widget computed user-select is none.
- Fresnel explorer: a real mouse drag on the person changes the distance readout; sensitivity bar starts non-zero at the default seat.
- Timeline: 7 entries, dots tappable, terminal arrow hidden, arrows centered on the card within 3px.
- Takeaways conclusion paragraph is 60 to 80 words with 5 bullets; 15 source cards; zero pageerrors; scrollWidth at most 391.
- css_audit: `python3 ~/workspace/tools/css_audit.py index.html` with the draft's css-audit-allow.txt (cards, fhead, voices, xicon, meta, nokatex, fn, tl): 0 unexplained orphans.
