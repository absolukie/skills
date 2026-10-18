---
name: verify-pi-api
description: Verify the Pi API primer (lukezhang.si/blog/pi-api/) against its feature map by running the Playwright harness, which drives the real UI (partner stepper, latency lab slider, access explorer chips, timeline) and asserts rendered geometry and computed styles.
---

# Verify Pi API primer

Feature map: `~/workspace/blog-drafts/pi-api/verify/FEATURE_MAP.md`
Harness: `~/workspace/blog-drafts/pi-api/verify/verify.py` (local port 8947)

Run it:

```
python3 ~/workspace/blog-drafts/pi-api/verify/verify.py            # local draft
python3 ~/workspace/blog-drafts/pi-api/verify/verify.py https://lukezhang.si/blog/pi-api/
```

Wait: Playwright against live URLs fails with ERR_TUNNEL_CONNECTION_FAILED in this VM; the live URL argument logs in REPORT.md but load checks fail there. Live verification is curl 200s plus served bytes = draft + 248.

Invariants the harness guards:
- Partner stepper: 6 panels, gesture suite (swipe left/right, tap advance, vertical ignored), terminal next hidden, Ultra 96.4 and Weave 42 percent present.
- Latency lab: buffer = 50 - L/20 exactly (43 actions at 139 ms default; 7 burned/frozen ticks; 50 at 0 ms; 20 at 600 ms with the beyond-tests verdict).
- Access explorer: rent 4 rows, download 3, build 4, chip selection moves .on.
- Mechanism card visuals (2026-10-15 rule: every card carries one): all 6 cards contain a styled .cviz; card 1 chips switch the readout and the diagram shows the 3B / 0.3B split; card 2 seg toggle swaps the token readout (30 to 60 tokens) and the flow readout (50 hertz); card 3 chunk strip has 100 ticks and taps advance Beat 1 to 3 with chunk 2 fully done at beat 3; card 4 shows 10,000 h and 400 h; card 5 scale SVG plus coach chip readout (espresso); card 6 has 4 latency bars, the first at 36% width (108 of 300 ms), with 108 ms and 139 ms present.
- KaTeX: katex.min.css must be loaded and .katex-mathml computed position absolute (a missing stylesheet link double-renders every formula; this bit rotation-matrices live before its fix).
- css_audit: `python3 ~/workspace/tools/css_audit.py index.html` with the draft's css-audit-allow.txt (cards, fhead, voices, xicon).
