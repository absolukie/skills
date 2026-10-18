---
name: "audio-redact"
description: "Bleep PII (names, phone numbers, company names) out of audio recordings. Uses faster-whisper word-level timestamps to find spoken phrases, then bleeps them with a tone via ffmpeg, and verifies the redaction by re-transcribing. For video deliverables, redact PII with the mew instead of silence (see the video section)."
---

# Audio Redact Skill

Bleep personally identifying phrases out of an audio file: names, phone numbers, company or restaurant names, in Chinese or English.

## Quick start

```bash
VENV=~/workspace/skills/audio-redact/.venv/bin/python
BIN=~/workspace/skills/audio-redact/bin/redact-audio.py

# 1. Dry run first: see what will be bleeped, with transcript context
$VENV $BIN call.mp3 --pii "张路坤,福1088,555-010-1000" -o out.mp3 --dry-run

# 2. Run for real (verifies by re-transcribing the redacted audio)
$VENV $BIN call.mp3 --pii "张路坤,福1088,555-010-1000" -o out.mp3
```

## How it works

1. `ffmpeg` decodes the input to 16 kHz mono WAV.
2. `faster-whisper` (small model, CPU, int8) transcribes with word-level timestamps.
3. Each `--pii` phrase is matched character-by-character against the transcript.
   Chinese numerals in speech (四八零…) are normalized to digits, so an
   Arabic-digit pattern matches either spoken form.
4. Matched ranges (plus `--pad` seconds, default 0.15) are cut to silence with
   smooth 40 ms fades at each edge, so it sounds like a clean dropout rather
   than a harsh censor beep (`--style tone` brings back the classic 880 Hz beep).
5. The redacted audio is re-transcribed; any surviving pattern is reported as
   a WARNING. Output is MP3 96k.

## The dry-run habit (important)

Whisper mishears, especially names (e.g. 张路坤 heard as 张禄坤). The dry run
prints every matched segment with ~30 characters of surrounding transcript.
Read it and look for:

- **Misheard variants**: add the misheard spelling to `--pii` too.
- **Spell-outs**: "my name is X, X as in x-ray…" — the spelled-out characters
  do NOT contain the original phrase, so add the spelled portion explicitly.
- **Partial names/titles**: "Mr. Zhang" does not match "Zhang Lukun"; add it.

Then re-run the dry run until the segment list covers everything, and only
then run without `--dry-run`.

## Options

| Flag | Default | Meaning |
|---|---|---|
| `--pii` | required | comma-separated phrases to bleep |
| `-o` | required | output file |
| `--lang` | `zh` | whisper language code (`en`, `zh`, …) |
| `--model` | `small` | whisper model size (`tiny`, `base`, `small`, `medium`) |
| `--pad` | `0.15` | extra seconds around each match |
| `--freq` | `880` | bleep tone frequency in Hz (`--style tone` only) |
| `--style` | `mute` | `mute` = cut to silence with fades (natural); `tone` = censor beep |
| `--fade` | `0.04` | fade seconds at each cut edge (`mute` style) |
| `--dry-run` | off | list matches only, do not modify audio |
| `--words-json` | off | save word timestamps for debugging |

## Environment notes

- The venv lives at `~/workspace/skills/audio-redact/.venv` (faster-whisper,
  ctranslate2; ~460 MB). The whisper model cache is in `~/.cache/huggingface`
  (downloaded once, ~460 MB for `small`).
- The script scrubs bracketed IPv6 entries (`[::1]`, …) out of `no_proxy` /
  `NO_PROXY` before importing, because they crash httpx during model download.
- `ffmpeg` 8.x is expected on PATH. The script feeds WAV data directly to the
  model to avoid the `av`/`PyAV` version clash (`metadata_errors` kwarg).

## Video redaction: use the mew (Luke's rule, 2026-10-11)

When the deliverable is a **video** (for example a call transcript video), do
NOT redact PII with silence or the 880 Hz beep. Use the mew: a short cat meow
laid over each PII span. In a video the mew reads as an intentional, funny
censor; silence reads like a glitch and the beep is harsh. Audio-only
deliverables keep the default silence style above.

The proven recipe (v3, from the 2026-10-09 call video):

1. Find the spans exactly as for audio: faster-whisper word-level
   timestamps, dry-run review first (mishears, spell-outs, partial names).
2. Mew sample: `assets/mew.wav` in this skill (one mew, ~0.45 s), peak
   normalized.
3. Level: set the mew's loudness to **1/7 of the RMS of the speech just
   before the span**. Level the mew sample itself BEFORE tiling; never
   measure across the filled span, or silent gaps inflate its loudness.
4. Fill: a span shorter than the mew gets a trimmed mew; a longer span gets
   the mew tiled with 0.30 s gaps between mews.
5. Edges: 60 ms crossfades in and out of every span, so it never clicks.
6. Mux the redacted audio back onto the video, then verify the same way as
   audio: re-transcribe the finished file and confirm zero PII tokens
   remain.

## Provenance

Built 2026-10-09 to redact two restaurant-call recordings for the blog post
"My AI Calls Restaurants in China" (lukezhang.si/blog/ai-calls-to-china/):
guest name, phone digits, and restaurant name bleeped; verified zero PII
tokens in the re-transcribed redacted audio. The mew variant was built the
same day for that post's hero call-transcript video; Luke made it the
standing rule for all video PII redaction on 2026-10-11.
