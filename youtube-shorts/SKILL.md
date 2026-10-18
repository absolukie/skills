---
name: "youtube-shorts"
description: "Luke's YouTube Shorts production playbook: 9:16 renders for his faceless channels, text safe zones, sound workflow, and per-format specs. Trigger on: 'youtube shorts', 'make a short', 'shorts skill', or any Shorts render/upload task."
---

# YouTube Shorts

How Luke's Shorts get made. Two faceless channels: The Moon Blinked (dreamy, slow,
pure mathematics, never AI-generated imagery) and Your Soup Is Typing (the
"How Many Circles" Fourier trace format and other playful builds). Public pages
and repos never name or link either channel; that rule lives in memory, this
skill is private working notes.

Channel plan (set 2026-10-13):
- The Moon Blinked visual directions: fractals (Mandelbrot and Julia zooms,
  recursive structures) and space (orbital mechanics, particle starfields,
  eclipse and phase cycles), all math-built, on top of the existing ink and
  wave pieces. Interesting visuals first; the math stays invisible.
- Your Soup Is Typing: Luke committed to 10 Fourier trace videos. Its
  ingredient board is the private Soup Pantry
  (https://projects.lukezhang.si/soup-pantry/, Cloudflare Access, Luke only):
  latest memes and trends, songs, funny sounds, and funny images, with a
  star-to-pick trace queue (10 picks). Kit refreshes the pantry from sweeps
  and from memes Luke sends in chat; the pantry manifest lives in
  ~/workspace/soup-pantry/.

## Text safe zone (Luke, 2026-10-13, from his Amogus Short screenshot)

Keep all on-screen text toward the CENTER of the frame. The Shorts player
chrome eats the edges:

- Top: the status bar, the Shorts header, and the Subscriptions/Live/Trends
  pills overlap roughly the top fifth. His title text sat there and got
  clipped and collided with the pills.
- Bottom: the channel row, video title, share bar, and nav overlap roughly
  the bottom fifth. His "1 circle" counter sat there, half hidden behind the
  share bar.
- Right edge: the like/comment/save/share action rail.

Rule: titles, counters, and captions live in the central band of the 9:16
frame, vertically centered-ish, clear of the top fifth, the bottom fifth, and
the right rail. If a design wants a top title or a bottom counter, pull it
inward until it sits in the clear middle region, and verify with a screenshot
of the actual Short playing in the app before calling it done.

## Format rules

- 9 by 16, seamless loop where the concept loops, music forward.
- No math words on screen for the Moon Blinked video primers (no "Fourier",
  no formulas as text); the math is the motion, not the caption.
- Fourier trace format (Your Soup Is Typing) is owned by the dedicated
  `circle-tracer` skill (~/workspace/skills/circle-tracer/): real DFT
  epicycles, visible chain, red outline, no error readout, no branding,
  title lower and circle counter higher per the safe-zone rule above, fart
  with reverb at the ending cut.

## Sound workflow

- Kit renders and preps everything SILENT. Luke attaches the sound in the
  YouTube mobile app and does the final post from his phone.
- Commercial Shorts sounds exist only in the mobile app picker (label
  licensing). The desktop Studio editor has only the royalty-free Audio
  Library. No API exists for attaching sounds. Baking a commercial track into
  the render instead means a Content ID claim and no sound-page link.
- Sounds come from his sound library (~/workspace/sound-library/), cleaned:
  trim dead air, loudnorm about -14 LUFS, true peak under -1 dB, MP3 192k.

## Publishing split

- Kit: render, QA (including the in-app safe-zone screenshot check above),
  upload prep.
- Luke: final sound pick and publish from his phone, plus any title edits he
  wants to make himself.
