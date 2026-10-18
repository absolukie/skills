---
name: "verify-streaming-responses"
description: "Re-run verification for the primer 'Why the Answer Trickles' at lukezhang.si/blog/streaming-responses/: feature map, Playwright harness, and last report live in the draft's verify folder."
---

# Verify: Why the Answer Trickles

Live URL: https://lukezhang.si/blog/streaming-responses/
Draft (canonical source): `~/workspace/blog-drafts/streaming-responses/index.html`
Illustration: `images/river.webp` in the draft folder (Codex ink illustration: dammed reservoir with rust-red gate wheel; released stream turning a waterwheel and filling a row of cups).

## Run it

```bash
cd ~/workspace/blog-drafts/streaming-responses/verify
python3 verify.py            # local draft on a throwaway server
python3 verify.py <url>      # any served URL
```

The harness drives the real UI at 390x844: Fig 1 delivery stepper (5 steps), Fig 2 serving stepper (4 steps), Fig 3 protocol explorer (4 chips: default OpenAI chunk panel, Anthropic input_json_delta panel, when-not-to-stream with the 50 percent Batch tier), 6 mechanism cards, the synthesis-flagged callout, the 6-step timeline with arrows measured at the stage's vertical midway, voices/camps/takeaways counts (7/2 agree + 2 versus/6), section order, 8 sources, computed-style and content-inset assertions, zero pageerrors, zero horizontal overflow. It writes `REPORT.md` and screenshots to `shots/` on every run.

Feature map: `~/workspace/blog-drafts/streaming-responses/verify/FEATURE_MAP.md`
Last report: `~/workspace/blog-drafts/streaming-responses/verify/REPORT.md`

## Content invariants (do not let an edit break these)

- The thesis is exact: same request, same tokens, same last-token time, same per-token price; streaming changes delivery only. The worked example (500 tokens at 50 tok/s = 10.0 s total, TTFT about 0.3 s, ITL about 20 ms, reading at 5 to 8 tok/s) is arithmetic and is labeled as such.
- The same-price claim rests on rate-card structure (one price per model, streaming as a listed feature; GPT-4.1 $2/$8 per million) and the page footer states that no explicit official "costs the same" sentence was found.
- Credit assignment stays correct: iteration-level scheduling/continuous batching is Orca (Yu et al., OSDI 2022); PagedAttention is vLLM (Kwon et al., SOSP 2023), whose 24x figure is the launch blog's own benchmark claim; Sarathi-Serve chunked prefill reports 2.6 to 5.6x capacity vs vLLM (OSDI 2024); speculative decoding is Leviathan et al. (arXiv:2211.17192, 2-3x T5-XXL) and Chen et al. (arXiv:2302.01318, 2-2.5x Chinchilla 70B), distribution-preserving.
- Ably's WebSocket position is always presented with its interest attached (it sells the alternative). The callout's "architectural commitment" framing is labeled a synthesis, not a quote.
- Batch APIs at both major labs are the 50-percent-off, explicitly non-streamed tier; cancellation stops billing because ungenerated tokens are never billed.

## Quirks

- Playwright against the live URL fails through this VM's proxy (ERR_TUNNEL_CONNECTION_FAILED). Live proof is curl: page, image, and /primers/ return 200, and served page bytes equal the draft plus exactly 248 bytes (Luke's analytics beacon).
- Arrows use the template's car-arrow system: buttons live inside a .tl-stage wrapper and their top is set by JS to the stage's vertical midway on every render. Stepper totals must equal the data-row counts exactly.
- The Fig 3 explorer reuses the .dv-panel/.dv-h/.dv-p classes; their CSS is not in the shared shell head and is added per page. If the panel ever renders unstyled, check for that block first.
- Retrofitted 2026-10-13 at Luke's screenshots: (1) all three steppers (#wireStage, #serveStage, #tlBody) now carry the visualizers rule-16 gesture contract (swipe steps like an arrow tap at 48px and 1.5x dominance, plain tap advances, touch-action pan-y, 400ms post-gesture click swallow), implemented via a small attachGestures helper driving wireStepper's goNext/goPrev; the harness covers all three with dispatched-PointerEvent suites. (2) The .sb-lab label row now wraps (claim flex 1 1 230px, chip margin-left auto): long verdict chips like "BLANK FOR THE FULL 10.0 S" drop to their own line instead of crushing the claim into a one-word-per-line sliver; the harness asserts the first claim renders at least 160px wide. Harness total after both: 77/77.
- Formatting repairs 2026-10-13 evening (Luke's screenshots, same sitting as the gestures retrofit): (1) the mechanism-card headers were built by JS with classes .fhead/.ftag/.ftitle/.chev that had NO CSS anywhere in the file (the stylesheet carried the other shell variant's .fnum/h3/.ftease rules), so the tag rendered at body size in a side column, the title squeezed beside it, and the open body inherited a 60px left indent meant for a numbered-badge layout. Overrides after the .fbody rules: the button wraps, .ftag is a small mono uppercase label on its own line, .ftitle is a full-width serif title, .chev rotates 90 degrees when open, and .fbody runs full width. (2) The callout heading used class .clabel while the stylesheet only defined .callout .lab, so it rendered as body text; .callout .clabel now carries the family eyebrow style plus explicit paragraph margins. Harness asserts tag font size, title width, body inset, and the callout label style; total 81/81. Root cause worth remembering: this page mixed two shell variants' markup and CSS; when a class has no matching rule the layout fails silently, so harnesses assert computed styles for header pieces, not just counts. Kimi's primer has the same unstyled .clabel (found by grep 2026-10-13, not yet fixed, awaiting Luke's word).
