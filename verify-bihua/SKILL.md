---
name: "verify-bihua"
description: "Verify Bihua, the stroke-order game: run its Playwright harness against the feature map and read the report. Use before and after changing Bihua, or when Luke asks whether Bihua still works. Live URL https://projects.lukezhang.si/bihua/"
---

# Verify Bihua

Bihua （笔画） is the Chinese stroke-order game: a fixed 16-key stroke keyboard under a character outline, easy/hard difficulty pills, persistent done/streak stats, and a hidden 56-stroke boss round behind 5 quick hard-pill taps.

## Artifacts (in ~/workspace/bihua/verify/)
- `FEATURE_MAP.md` — the contract: every feature from the player's point of view, with steps, expectations, and proof screenshots. One entry (the just-in-time loader) is marked UNVERIFIED: it is timing-dependent and has no harness check yet.
- `verify.py` — the harness. Python Playwright, 390x844, real UI taps only, fails on any pageerror.
- `REPORT.md` — the latest run's per-check results, plus a live cross-check section.
- `shots/` — proof screenshots named after the map entries.

## Run it
```
cd ~/workspace/bihua && python3 verify/verify.py            # local copy (default)
python3 verify/verify.py https://projects.lukezhang.si/bihua/   # live, when the sandbox browser can reach it
```
The sandbox's headless browser has failed to tunnel to the live origin before (ERR_TUNNEL_CONNECTION_FAILED). When that happens, cross-check live by served bytes instead: fetch the live index.html, remove the production analytics beacon script (248 bytes, inserted before </body>), and compare byte-for-byte with the local source; spot-check asset URLs for HTTP 200. Record which method the run used in REPORT.md.

## Known state (2026-10-12)
- 19 of 20 checks pass locally. The one failure is asset-integrity against the LOCAL copy only: ~/workspace/bihua is missing biang_ghost.png, which production serves (HTTP 200). The app is fine; the local mirror is incomplete until someone copies the file in.
- Boss round: any key advances it, 56 taps complete it, rotation then resumes at 木.
- Difficulty: tapping the last remaining ON pill swaps to the other difficulty instead of selecting none.
