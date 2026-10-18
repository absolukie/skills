---
name: "verify-meme-vault"
description: "Verify Luke's private Meme Vault (projects.lukezhang.si/meme-vault): feature map, Playwright harness, and the Cloudflare Access privacy check. Trigger on: 'verify the meme vault', 'check the meme vault', 're-verify meme-vault'."
---

# Verify Meme Vault

Project: ~/workspace/meme-vault/ (canonical media in media/, catalog in manifest.json, deployable page in site/).
Live URL: https://projects.lukezhang.si/meme-vault/ (Cloudflare Access, Luke only; the harness cannot sign in as him).

## Run
- Local UI checks: `python3 ~/workspace/meme-vault/verify/verify.py`
  Serves site/ locally, drives Chromium at 390x844 with real taps: one card per manifest meme (image cards on thumbnails, text cards for file:null entries, GIF badge), tag chips (kitten narrows to 3, All restores), search by title/text/tags with empty state and 16px input guard, tap-to-open viewer loading the ORIGINAL file (never the thumb) plus a text-meme viewer pass, no horizontal overflow, pageerror listener. Writes verify/REPORT.md and verify/shots/.
- Live privacy check: `python3 ~/workspace/meme-vault/verify/verify.py --live`
  Unauthenticated GETs of the page and the first manifest media URL must come back blocked (302 to cloudflareaccess.com or 401/403), never 200. Writes verify/REPORT-LIVE.md.

## Map and reports
- Feature map: ~/workspace/meme-vault/verify/FEATURE_MAP.md (the contract; the privacy entry is live-only and marked there).
- Last reports: verify/REPORT.md (local, 6/6 at launch), verify/REPORT-LIVE.md (live, 2/2 at launch).

## Quirks
- After editing manifest.json, run `python3 ~/workspace/meme-vault/sync_memes.py` before verifying or deploying; it regenerates the MEMES block in site/index.html, copies media into site/media/, and rebuilds thumbnails into site/media/thumbs/ with ffmpeg. The grid uses thumbs; the viewer always loads originals.
- Deploy is a surgical CAS push to absolukie/lukezhang-si (sites/meme-vault/ files; worker.js SITES already contains "meme-vault") via ~/workspace/tools/gh_surgical.py. Fetch worker.js fresh first, never edit a stale copy.
- The Access app "Meme vault" (domain projects.lukezhang.si/meme-vault, policy "Luke only" for absolukie@gmail.com, 24h sessions) mirrors the "Sound library" app exactly and must exist before any deploy of this site. Re-running ~/workspace/meme-vault/setup_access.py is idempotent.
- The vault URL is private: never link it from any public page.
