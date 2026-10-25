---
name: "circle-tracer"
description: "Generate Luke's Fourier epicycle 'How many circles' trace videos from an uploaded image: extract the outer contour, run a real DFT, and render a vertical 720x1280 video through a requested circle ramp and duration. Trigger on: 'circle tracer', 'how many circles video', 'fourier trace this image', 'make a trace video', or a new subject for the Your Soup Is Typing trace format."
---

# Circle Tracer

## Purpose

Turn one uploaded image into a verified Fourier trace video. The math is real:
the script extracts the subject's outer contour, resamples it, computes the
DFT, and draws each stage with the requested number of highest amplitude
circles. It never fakes the count.

Working code: `bin/circle_tracer.py` in this skill. The earlier Amogus build
lives in `~/workspace/moonblinked-studio/fourier-traces/` and is the reference
implementation this skill generalizes.

## Workflow

1. Read the `youtube-shorts` skill for channel and publishing context.
2. Inspect the source image. It works best on a plain light background with
   one connected subject. The tracer follows the outer silhouette only, so
   internal details such as eyes are not separate traces.
3. Run a contour preview first and view it:
   `python3 ~/workspace/skills/circle-tracer/bin/circle_tracer.py --image <img> --subject "<name>" --duration <s> --ramp <k,k,...> --output <out.mp4> --preview <preview.png> --preview-only`
   The preview must hug the subject and exclude cast shadows and background.
   If it does not, stop and fix the extraction before rendering.
4. Render without `--preview-only`. Keep the user's exact ramp and duration.
5. QA every render before delivery (see Output contract).

## Command

```
python3 ~/workspace/skills/circle-tracer/bin/circle_tracer.py \
  --image /path/to/image.jpg \
  --subject "Tung Tung Sahur" \
  --duration 40 \
  --ramp 4,5,6,7,10,500 \
  --output /path/to/output.mp4 \
  --preview /path/to/contour-preview.png
```

Options: `--font space-grotesk` (default) or `sora`, `inter`, `bricolage`,
`dejavu` for the title and counter typeface (vendored bold cuts in
`bin/fonts/`; Luke asked for font options on 2026-10-13 rather than one
locked pick), `--sound fart` (default; the cleaned sound library fart fires at the
ending cut) or `--sound none` (silent master for adding sound in the YouTube
app), `--samples 8192`, `--sound-file <mp3>`, `--ending picture` (default) or
`--ending freeze` (no picture overlay; hold the final trace) or
`--ending none` (no done hold and no ending hold at all: the final stage
draws right up to the last frame, and the sound is placed to finish as
the video ends), and
`--final-fraction 0.5` to cut the final stage off partway through its draw.

## Format rules

- 720x1280, 30fps, H.264 yuv420p limited range BT.709.
- Parchment background. The full target outline sits underneath in faint red;
  the trace is bold red `#b3352b`; epicycle circles and arms are muted gray
  and visible. No error readout, no branding, no math words on screen.
- Title: "How many circles / to draw <subject>?" The counter reads
  "1 circle" or "N circles" for the current stage.
- ALL on-screen text on Your Soup Is Typing is lowercase, always (Luke,
  2026-10-19, "make all text lowercase and save that to skill"): the title
  renders "how many circles to draw <subject>?" in lowercase, and so does
  the counter and every other text element, on still and moving traces.
- Ending: after a brief hold on the completed trace, hard cut to the
  original picture, with the title and final counter still visible.
- Circle counts are MEASURED, never inherited (Luke, 2026-10-19: "make
  sure the circles is the minimum set to get minimal error"). A preset
  ramp stage is not a measurement: the hamster Short's 48 came from the
  still format's ramp and was never the measured minimum for that subject.
  For any trace, still or moving, sweep the reconstruction error across
  counts on the subject itself and use the smallest count that reaches
  the error floor; report the count and its error with the render.
- NO freeze tail (Luke, 2026-10-19, on the posted hamster video: "weird
  extra freeze dead time at the end of the clip. I had to crop that"). A
  trace video ends when the action ends: at most a 0.4s beat on the final
  frame, never a long frozen hold. He crops nothing; the render ships at
  the length the action takes. Intentional end beats (a sound hit, a still
  overlay) stay only as long as the beat itself needs. The
  reveal MUST be the picture cropped to the stage's padded silhouette box
  (`Stage.reveal_crop`), placed on the stage transform, so the character
  lands on the traced outline at the same size and the crop edges meet
  the stage box. Two failure modes Luke flagged on the Tung Tung cuts
  (2026-10-13): a contain-fit box floats the picture at a different size
  and position, and pasting the full photo leaves the character floating
  in the photo's white margins so he reads smaller than the traced dude
  even when the transform is exact. The sound fires at the cut when
  sound is on.

## Text placement (Luke, 2026-10-13)

The Amogus Short's title was clipped by the top player chrome and its counter
was hidden behind the bottom share bar. Circle Tracer moves both inward:

- Title lower: first line top at y=268, second line at y=324, below the top
  fifth of the 1280px frame.
- Circle counter higher: top at y=394, directly under the title, nowhere near
  the bottom fifth.
- Drawing stage: y=472 to y=1138. Text is drawn last, on top of the chain.

Do not move the title back to the top edge or the counter back to the bottom
without Luke asking.

## Output contract

Every delivery states and verifies:

- Exact duration from ffprobe (450 frames for 15s, 1200 for 40s at 30fps).
- The exact ramp rendered, and that the largest count is a real DFT term
  count (the script asserts the chain pen tip equals the masked inverse FFT
  reconstruction).
- Frame grabs viewed at an early stage, a middle stage, the final stage,
  and the ending picture.
- Audio state: silent, or the fart's placement and level from volumedetect.
- The contour preview was viewed and follows the subject, not its shadow.
