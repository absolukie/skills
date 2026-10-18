---
name: "verify-disdain-reads-as-confidence"
description: "Re-run verification for the primer 'Disdain Reads as Confidence, Checked' at lukezhang.si/blog/disdain-reads-as-confidence/: feature map, Playwright harness, and last report live in the draft's verify folder."
---

# Verify: Disdain Reads as Confidence, Checked

Live URL: https://lukezhang.si/blog/disdain-reads-as-confidence/
Draft (canonical source): `~/workspace/blog-drafts/disdain-reads-as-confidence/index.html`
Illustration: `images/spotlight.webp` in the draft folder (Codex ink illustration: speaker, dashed imagined spotlight, tiny real one, audience on phones).

## Run it

```bash
cd ~/workspace/blog-drafts/disdain-reads-as-confidence/verify
python3 verify.py            # local draft on a throwaway server
python3 verify.py <url>      # any served URL
```

The harness drives the real UI at 390x844: claim-check stepper (6 steps, 5 claims with verdict chips), Brooks worked-example stepper (4 steps, karaoke bars ordered, anxiety-twist bars near equal), 6 mechanism cards, the dominance/prestige callout, the 16-step timeline with rule-5 anchored arrows, voices/camps/takeaways counts (8/6/6), keep-exploring links, 18 sources, a zero em/en dash scan, and keyboard stepping scoped to the visible stepper. It writes `REPORT.md` and screenshots to `shots/` on every run.

Feature map: `~/workspace/blog-drafts/disdain-reads-as-confidence/verify/FEATURE_MAP.md`
Last report: `~/workspace/blog-drafts/disdain-reads-as-confidence/verify/REPORT.md`

## Quirks

- Playwright against the live URL fails through this VM's proxy (ERR_TUNNEL_CONNECTION_FAILED). Live proof is curl: page, image, and /primers/ return 200, and served page bytes equal the draft plus exactly 248 bytes (Luke's analytics beacon injected before the closing body tag).
- Three sources block scripted curl checks but load for real readers, all confirmed via a page fetch before publish: Fast Company (403; the Sam Horn "ridicules your audience" passage is the article's first item), ListenNotes (403; BBC More or Less episode page), PubMed (203; the Brooks 2014 abstract page).
- Quote discipline: the post is quoted once on the page, 16 words, well under any fair-use concern; everything else about it is paraphrase.
