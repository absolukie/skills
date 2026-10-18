---
name: "verify-sound-library"
description: "Verify Luke's private Sound Library soundboard (projects.lukezhang.si/sound-library): feature map, Playwright harness, and the Cloudflare Access privacy check. Trigger on: 'verify the sound library', 'check the soundboard', 're-verify sound-library'."
---

# Verify Sound Library

Project: ~/workspace/sound-library/ (canonical clips in audio/, catalog in manifest.json, deployable page in site/).
Live URL: https://projects.lukezhang.si/sound-library/ (Cloudflare Access, Luke only; the harness cannot sign in as him).

## Run
- Local UI checks: `python3 ~/workspace/sound-library/verify/verify.py`
  Serves site/ locally, drives Chromium at 390x844 with real taps: card render, play/pause with real playback state, playback end reset, search filter and empty state, tag chips, real download capture, pageerror listener. Writes verify/REPORT.md and verify/shots/.
- Live privacy check: `python3 ~/workspace/sound-library/verify/verify.py --live`
  Unauthenticated GETs of the page and the first manifest audio URL must come back blocked (302 to cloudflareaccess.com or 401/403), never 200. Writes verify/REPORT-LIVE.md.

## Map and reports
- Feature map: ~/workspace/sound-library/verify/FEATURE_MAP.md (the contract; live-only privacy entry is marked there).
- Last reports: verify/REPORT.md (local), verify/REPORT-LIVE.md (live).

## Quirks
- After editing manifest.json, run `python3 ~/workspace/sound-library/sync_sounds.py` before verifying or deploying; it regenerates the SOUNDS block in site/index.html and copies audio into site/audio/.
- Deploy is a surgical CAS push to absolukie/lukezhang-si (sites/sound-library/ plus the worker.js SITES entry) via ~/workspace/tools/gh_surgical.py. Fetch worker.js fresh first, never edit a stale copy.
- The Access app "Sound library" (domain projects.lukezhang.si/sound-library, policy "Luke only" for absolukie@gmail.com) must exist before any deploy of this site; it mirrors the "Build status dashboard" app for /status/.
