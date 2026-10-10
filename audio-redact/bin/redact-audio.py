#!/usr/bin/env python3
"""Bleep PII phrases out of an audio file using word-level timestamps.

Pipeline: ffmpeg decode -> faster-whisper word timestamps -> character-level
PII matching -> redaction (default: clean cut to silence with smooth fades;
--style tone for the classic censor beep) -> verify by re-transcribing the
redacted audio.

Usage:
    redact-audio.py INPUT.mp3 --pii "John Smith,5550101000,Acme Corp" -o out.mp3
    redact-audio.py INPUT.mp3 --pii "name,number" --dry-run   # list segments only

Notes:
- Whisper sometimes mishears (especially names). Always review --dry-run output;
  if a name was misheard, add the misheard spelling to --pii as well.
- Chinese numerals in speech (四八零…) are normalized to digits before matching,
  so an Arabic-digit pattern matches either spoken form.
"""
import os
# Work around broken bracketed-IPv6 entries in no_proxy that crash httpx
# (used by huggingface_hub when downloading the model).
def _clean_proxy(val):
    parts = [p for p in val.split(",") if not (p.startswith("[") and p.endswith("]"))]
    return ",".join(parts)
os.environ["no_proxy"] = _clean_proxy(os.environ.get("no_proxy", ""))
os.environ["NO_PROXY"] = _clean_proxy(os.environ.get("NO_PROXY", ""))

import argparse
import json
import re
import subprocess
import sys
import tempfile
import wave

import numpy as np

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CN_NUM = {"一": "1", "二": "2", "三": "3", "四": "4", "五": "5", "六": "6",
          "七": "7", "八": "8", "九": "9", "零": "0", "两": "2", "幺": "1",
          "○": "0", "〇": "0"}


def normalize(s):
    """Strip whitespace/punctuation; map Chinese numerals to digits."""
    s = "".join(CN_NUM.get(c, c) for c in s)
    return re.sub(r"[\s,.?!，。？！、；：:;\"'「」『』（）()\[\]…—–-]", "", s)


def decode_wav(src, tmpdir):
    out = os.path.join(tmpdir, "in.wav")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src,
                    "-ar", "16000", "-ac", "1", out], check=True)
    return out


def load_mono16(path):
    w = wave.open(path)
    return (np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
            .astype(np.float32) / 32768.0)


def transcribe(model, audio, lang):
    segments, _ = model.transcribe(audio, language=lang, word_timestamps=True)
    words = []
    for seg in segments:
        for wd in (seg.words or []):
            words.append({"w": wd.word, "s": wd.start, "e": wd.end})
    return words


def find_ranges(words, patterns, pad):
    """Character-level match of each pattern against the word stream."""
    chars, times = [], []
    for wd in words:
        for i, ch in enumerate(wd["w"]):
            frac0, frac1 = i / len(wd["w"]), (i + 1) / len(wd["w"])
            chars.append(ch)
            times.append((wd["s"] + frac0 * (wd["e"] - wd["s"]),
                          wd["s"] + frac1 * (wd["e"] - wd["s"])))
    norm_chars = [normalize(c) for c in chars]
    # drop chars that normalize to empty (punctuation/whitespace)
    kept = [(c, t) for c, t in zip(norm_chars, times) if c]
    stream = "".join(c for c, _ in kept)

    ranges = []
    for pat in patterns:
        npat = normalize(pat)
        if not npat:
            continue
        start = 0
        while True:
            idx = stream.find(npat, start)
            if idx < 0:
                break
            s = kept[idx][1][0] - pad
            e = kept[idx + len(npat) - 1][1][1] + pad
            ranges.append((max(0.0, s), e, pat))
            start = idx + 1

    # merge overlapping/adjacent ranges
    ranges.sort()
    merged = []
    for s, e, pat in ranges:
        if merged and s <= merged[-1][1] + 0.25:
            merged[-1] = (merged[-1][0], max(merged[-1][1], e),
                          merged[-1][2] + "+" + pat)
        else:
            merged.append((s, e, pat))
    return merged


def bleep(src_wav, ranges, out_wav, freq=880.0, level=0.12, style="mute",
          fade=0.04, sr=16000):
    """Redact ranges from audio.

    style="mute": replace with digital silence, with raised-cosine fades at
        both edges so it sounds like a clean dropout, no clicks.
    style="tone": classic censor beep (sine at `freq` Hz) over muted audio.
    """
    w = wave.open(src_wav)
    audio = (np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
             .astype(np.float32) / 32768.0)
    n = len(audio)

    if style == "mute":
        out = audio.copy()
        fl = max(1, int(fade * sr))
        ramp = 0.5 * (1 - np.cos(np.linspace(0, np.pi, fl)))  # 0 -> 1
        for s, e, _ in ranges:
            i0, i1 = int(s * sr), min(n, int(e * sr))
            if i1 <= i0:
                continue
            out[i0:i1] = 0.0
            # fade out: full volume -> 0 across [i0-fl, i0]
            a0, a1 = max(0, i0 - fl), i0
            if a1 > a0:
                r = ramp[fl - (a1 - a0):][::-1]
                out[a0:a1] = audio[a0:a1] * r
            # fade in: 0 -> full volume across [i1, i1+fl]
            b0, b1 = i1, min(n, i1 + fl)
            if b1 > b0:
                out[b0:b1] = audio[b0:b1] * ramp[:(b1 - b0)]
        with wave.open(out_wav, "wb") as wo:
            wo.setnchannels(1)
            wo.setsampwidth(2)
            wo.setframerate(sr)
            wo.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())
        return

    # style="tone": original ffmpeg approach
    dur = float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", src_wav]).decode().strip())
    expr = "+".join(f"between(t,{s:.2f},{e:.2f})" for s, e, _ in ranges)
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", src_wav,
         "-f", "lavfi", "-i", f"sine=frequency={freq}:duration={dur}",
         "-filter_complex",
         f"[0:a]volume=0:enable='{expr}'[muted];"
         f"[1:a]volume={level}:enable='{expr}'[beep];"
         f"[muted][beep]amix=inputs=2:duration=first[aout]",
         "-map", "[aout]", "-ar", "16000", "-ac", "1", out_wav],
        check=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("input", help="input audio file (mp3/wav/m4a/...)")
    ap.add_argument("--pii", required=True,
                    help="comma-separated PII phrases to bleep")
    ap.add_argument("-o", "--output", required=True, help="output audio file")
    ap.add_argument("--lang", default="zh", help="whisper language code")
    ap.add_argument("--model", default="small", help="whisper model size")
    ap.add_argument("--pad", type=float, default=0.15,
                    help="seconds of padding around each match")
    ap.add_argument("--freq", type=float, default=880.0, help="bleep tone Hz")
    ap.add_argument("--style", choices=["mute", "tone"], default="mute",
                    help="mute=cut to silence with smooth fades (default); "
                         "tone=classic censor beep")
    ap.add_argument("--fade", type=float, default=0.04,
                    help="fade seconds at each cut edge (mute style)")
    ap.add_argument("--dry-run", action="store_true",
                    help="only list matched segments, do not modify audio")
    ap.add_argument("--words-json",
                    help="save word-level timestamps here (debug)")
    args = ap.parse_args()

    from faster_whisper import WhisperModel
    patterns = [p.strip() for p in args.pii.split(",") if p.strip()]

    with tempfile.TemporaryDirectory() as tmp:
        wav = decode_wav(args.input, tmp)
        model = WhisperModel(args.model, device="cpu", compute_type="int8")
        words = transcribe(model, load_mono16(wav), args.lang)
        if args.words_json:
            json.dump(words, open(args.words_json, "w"), ensure_ascii=False)

        ranges = find_ranges(words, patterns, args.pad)
        total = sum(e - s for s, e, _ in ranges)
        print(f"matched {len(ranges)} segment(s), {total:.1f}s total:")
        full = "".join(wd["w"] for wd in words)
        # char offset of each word start, for context display
        offs, acc = [], 0
        for wd in words:
            offs.append(acc)
            acc += len(wd["w"])
        for s, e, pat in ranges:
            mid = (s + e) / 2
            wi = next((i for i, wd in enumerate(words)
                       if wd["s"] <= mid <= wd["e"]), 0)
            lo = max(0, offs[wi] - 30)
            print(f"  [{s:6.2f}-{e:6.2f}] {pat}")
            print(f"           ...{full[lo:offs[wi] + 30]}...")
        if args.dry_run:
            return

        if not ranges:
            print("nothing matched; copying input unchanged")
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i",
                            args.input, "-c", "copy", args.output], check=True)
            return

        red_wav = os.path.join(tmp, "redacted.wav")
        bleep(wav, ranges, red_wav, freq=args.freq, style=args.style,
              fade=args.fade)

        # verify: re-transcribe and look for surviving patterns
        words2 = transcribe(model, load_mono16(red_wav), args.lang)
        ranges2 = find_ranges(words2, patterns, 0.0)
        if ranges2:
            print("WARNING: PII may survive in redacted audio:")
            for s, e, pat in ranges2:
                print(f"  [{s:6.2f}-{e:6.2f}] {pat}")
        else:
            print("verify: no PII patterns detected in redacted audio")

        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", red_wav,
                        "-codec:a", "libmp3lame", "-b:a", "96k",
                        args.output], check=True)
        print("wrote", args.output)


if __name__ == "__main__":
    main()
