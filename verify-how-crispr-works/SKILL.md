---
name: "verify-how-crispr-works"
description: "Re-run verification for the primer 'How CRISPR Works' at lukezhang.si/blog/how-crispr-works/: feature map, Playwright harness, and last report live in the draft's verify folder."
---

# Verify: How CRISPR Works

Live URL: https://lukezhang.si/blog/how-crispr-works/
Draft (canonical source): `~/workspace/blog-drafts/how-crispr-works/index.html`
Illustration: `images/cut.webp` in the draft folder (Codex ink illustration: ornate scissors guided by a notched ribbon to one rust-red rung of a DNA ladder).

## Run it

```bash
cd ~/workspace/blog-drafts/how-crispr-works/verify
python3 verify.py            # local draft on a throwaway server
python3 verify.py <url>      # any served URL
```

The harness drives the real UI at 390x844: Fig 1 cut-anatomy stepper (6 steps), Fig 2 editor-family stepper (6 steps), Fig 3 specificity-arithmetic stepper (4 steps), Fig 4 delivery explorer (3 chips switching panels: Casgevy/$2.2M, NTLA-2001/87 percent, EDIT-101/4.7 kb), 6 mechanism cards, the on-target callout, the 13-step timeline with arrows measured at the stage's vertical midway, voices/camps/takeaways counts (8/2 agree + 2 versus/6), section order, 12 sources, computed-style and content-inset assertions, zero pageerrors, zero horizontal overflow. It writes `REPORT.md` and screenshots to `shots/` on every run.

Feature map: `~/workspace/blog-drafts/how-crispr-works/verify/FEATURE_MAP.md`
Last report: `~/workspace/blog-drafts/how-crispr-works/verify/REPORT.md`

## Content invariants (do not let an edit break these)

- Mechanism numbers trace to the primary papers: PAM 5'-NGG-3' for SpCas9, cut about 3 bp upstream, HNH cuts the guide-paired strand and RuvC the other (Jinek 2012); Cas12a T-rich PAM and staggered cut (Zetsche 2015); base editors cover transitions only, 4 of 12 point changes (Komor 2016, Gaudelli 2017); prime editing's 89 percent is the paper's in-principle claim and is labeled that way (Anzalone 2019).
- Efficiency figures are ranges, never points: NHEJ up to about 60 percent of alleles (best mouse work, per the PMC review), HDR typically 0.5 to 20 percent.
- Fig 3 arithmetic is exact: 4^20 = about 1.1 trillion; variants within 3 mismatches = 1 + 60 + 1,710 + 30,780 = 32,551; expected candidate sites about 89 (3e9 x 32,551 / 1.1e12).
- NTLA-2001 figures are day-28, n of 6: TTR down 52 percent at 0.1 mg/kg, 87 percent at 0.3 mg/kg (Gillmore, NEJM 2021). The KJ case: bespoke adenine base editor, about six months design to dose, first dose February 2025 (NEJM 2025, DOI 10.1056/NEJMoa2504747).

## Quirks

- Playwright against the live URL fails through this VM's proxy (ERR_TUNNEL_CONNECTION_FAILED). Live proof is curl: page, image, and /primers/ return 200, and served page bytes equal the draft plus exactly 248 bytes (Luke's analytics beacon).
- Science, NEJM, and Cell pages refuse scripted curl (403 bot wall); their content was confirmed by reading them in a browser during research. Nature links 303-redirect then 200.
- Arrows use the template's car-arrow system: buttons live inside a .tl-stage wrapper and their top is set by JS to the stage's vertical midway on every render.
