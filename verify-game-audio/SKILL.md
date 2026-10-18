---
name: "verify-game-audio"
description: "Re-run verification for the primer 'Game Audio, Three Ways' at lukezhang.si/blog/game-audio/: feature map, Playwright harness, and last report live in the draft's verify folder."
---

# Verify: Game Audio, Three Ways

Published 2026-10-13: content commit a308d08f23aeb9181559d9ab267766a13e7b45ae, index commit ad0740404e4f1a77d9455a2fcfd53da9847b4cf8. Final local harness run: 79 of 79 checks passed. Live-verified by curl: page 200 with title (served bytes = draft + 248 beacon), primers index contains the entry, both illustrations and sampled audio files 200 with exact sizes.
Live URL: https://lukezhang.si/blog/game-audio/
Draft (canonical source): `~/workspace/blog-drafts/game-audio/index.html`
Assets: `images/three-routes.webp` and `images/wiring.webp` (Codex ink illustrations), `audio/claude/*.mp3` and `audio/codex/*.mp3` (the two tested packs, vendored verbatim).

## Run it

```bash
cd ~/workspace/blog-drafts/game-audio/verify
python3 verify.py            # local draft on a throwaway server (port 8821)
python3 verify.py <url>      # any served URL
```

The harness checks the static invariants first (zero em/en dashes, tag balance, node --check on all three inline scripts, pack byte totals on disk matching the numbers printed on the page), then drives the real UI at 390x844: hero and section order, six mechanism cards (tap to open, aria-expanded), the embedded Coin Hop game played with real keyboard input (move, jump, first coin, then a state-polled platforming route across all five coins to the win banner and Play again reset), pack switching Muse to Codex to Summer and back (Summer must show the skip note and hold no audio at all), all twelve listening files returning HTTP 200 plus two decode checks, the measured comparison table's key numbers, the sixteen-step timeline (rule-5 arrows: 46px, straddling at minus 23px, midway on the card, terminal arrows hidden, dots, count, arrow keys, no page scroll), eight voice cards, prediction camps (5 camps, 6 split sides), six takeaways, the two Keep exploring links, twenty-six source cards, zero third-party requests, zero pageerrors, no horizontal overflow, and finally every source link returning HTTP 200 with retries. It writes `REPORT.md` and screenshots to `shots/` on every run.

Feature map: `~/workspace/blog-drafts/game-audio/verify/FEATURE_MAP.md`
Last report: `~/workspace/blog-drafts/game-audio/verify/REPORT.md`

## Content invariants (do not let an edit break these)

- The Summer arm was SKIPPED at Luke's call (sign-in flow: browser OAuth, 15-minute session expiry, Google phone tap; three sessions burned). The page must always say so plainly: brief callout, game skip note, Summer listening block, footer. Summer is judged on docs and research only, never as tested. Never fabricate Summer audio or results.
- Measured numbers are from the actual files (ffmpeg ebur128 LUFS, astats peaks): Muse pack 362,973 bytes total, about 57 s, 7 steps; Codex pack 1,087,374 bytes, 101.7 s, 8 steps, 24,056 tokens. Loop seam steps: Muse 0.052 vs internal max 0.255; Codex 0.00137 vs 0.0382. Voices: Muse npc 3.888 s at 24 kHz, -25.1 LUFS; dialogue 7.944 s, -22.6 LUFS (the laughing line carries a spoken "Ha!" cue, disclosed on the page). Codex npc 4.069 s, -16.2 LUFS (Flite); dialogue 8.129 s, -22.0 LUFS.
- Sections 5 and 6 (voices, predictions) come only from `~/workspace/research_notes/ai-game-audio-primer-20261013-0010/report.md` sections 3 and 4. Nothing invented: the per-player-score item is one party's patent plus vendor direction, labeled as such on the page.
- Unverified items stay in the footer, never promoted to facts: Summer founding/funding (no primary source; do not attribute W4 Games funding to Summer), ElevenLabs and Suno official pricing (their pages blocked the research browser; secondary summaries agree), Udio live terms (login-gated), Stable Audio hosted price (sources conflict), Sonilo claims (vendor press release).
- The TechCrunch ElevenLabs SFX link died after research (404/403 from this network); the source card now points at ElevenLabs' own sound-effects page, with the May 31, 2024 date cross-checked on the Wikipedia card.
- Five more research-era links (Shacknews, TheWrap, Rock Paper Shotgun, Eurogamer, PSU) started returning 404 from this network after research despite returning 200 during it; they were replaced before publish with reachable coverage of the same facts: GamesBeat (IMA ratification and the Drescher quote), Polygon (the Söderlund interview), and GamesRadar (Burch in her own words). If they 404 again in a future run, swap coverage, never drop the claim's sourcing.
- Nine source URLs arrived from the research handoff with paraphrased slugs that 404 (two Production Expert, two Music Business Worldwide, and one each for Music Ally, the GDC survey report, Operation Sports, the Sonilo release, and VG247); the real slugs were recovered by search and curl-verified before publish (the Shulman card now points at Chaoszine's coverage of the same 20VC interview). Also corrected from the handoff: the $250M in the Warner-Suno story was Suno's Series C raise at a $2.45B valuation, not a settlement payment; the page now says so.
- The game win route is timing-sensitive under VM load: it drives with continuous key holds and closed-loop steering (hold Right only while heroX is left of the release point), retries each hop up to four times, and repositions between leg attempts. A failed game check on a loaded machine deserves one rerun before anyone touches game code.

## Quirks

- The game's platforms are solid from below: jumping from directly under a platform bonks the hero's head (original test-game physics, kept). The harness routes around it: jumps start beside their target platform, and the top platform is reached by jumping straight up at x=296 then drifting right near the apex. If the win route flakes, check takeoff positions before touching game code.
- Playwright against the live URL fails through this VM's proxy (ERR_TUNNEL_CONNECTION_FAILED); local harness plus curl is the accepted proof pattern. Served bytes exceed draft bytes by exactly 248 (analytics beacon injection).
- Game keyboard input is visibility-guarded (the game must be in the viewport) so Space and arrows never hijack page scroll; the harness scrolls the game into view before sending keys.
