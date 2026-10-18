---
name: "verify-the-10k-app-recipe"
description: "Re-run verification for the primer 'The $10K App Recipe, Checked' at lukezhang.si/blog/the-10k-app-recipe/: feature map, Playwright harness, and last report live in the draft's verify folder."
---

# Verify: The $10K App Recipe, Checked

Live URL: https://lukezhang.si/blog/the-10k-app-recipe/
Draft (canonical source): `~/workspace/blog-drafts/the-10k-app-recipe/index.html`
Illustration: `images/funnel.webp` in the draft folder (Codex ink illustration).

## Run it

```bash
cd ~/workspace/blog-drafts/the-10k-app-recipe/verify
python3 verify.py            # local draft on a throwaway server
python3 verify.py <url>      # any served URL
```

The harness drives the real UI at 390x844: claim-check stepper (7 steps, 6 claims), funnel stepper (5 steps), 6 mechanism cards, the platform-risk callout, the 13-step timeline with rule-5 anchored arrows, voices/camps/takeaways counts, keep-exploring links, 20 sources, a zero em/en dash scan, and keyboard stepping scoped to the visible stepper. It writes `REPORT.md` and screenshots to `shots/` on every run.

Feature map: `~/workspace/blog-drafts/the-10k-app-recipe/verify/FEATURE_MAP.md`
Last report: `~/workspace/blog-drafts/the-10k-app-recipe/verify/REPORT.md`

## Quirks

- Playwright against the live URL fails through this VM's proxy (ERR_TUNNEL_CONNECTION_FAILED). Live proof is curl: page, image, and /primers/ return 200, and served page bytes equal the draft plus exactly 248 bytes (Luke's analytics beacon injected before the closing body tag).
- Two sources (GlobeNewswire, Reuters) block scripted curl checks with 403/401 but load for real readers; both were confirmed readable via a page fetch before publish.
