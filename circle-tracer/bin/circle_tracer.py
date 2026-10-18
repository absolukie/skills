#!/usr/bin/env python3
"""Circle Tracer: Fourier epicycle trace videos from an uploaded image.

Extracts the subject's outer silhouette from a plain light background,
resamples it uniformly by arc length, computes the DFT, and renders a
720x1280 30fps video in which each stage is drawn by the top-K Fourier
circles for the requested K. The chain pen tip is asserted equal to the
masked inverse-FFT reconstruction, so the circle counts are real.

Layout (Luke, 2026-10-13): the title sits LOWER than the first Amogus cut
(first line top y=268, below the top fifth) and the circle counter sits
HIGHER (top y=394, directly under the title), because the YouTube Shorts
player chrome ate both in their old positions.
"""
import argparse
import json
import math
import os
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

FPS = 30
W, H = 720, 1280
BG = (246, 240, 222)
INK = (43, 38, 30)
RED = (179, 53, 43)
FAINT_RED = (226, 172, 158)
CIRCLE = (178, 172, 154)
ARM = (130, 124, 108)
WHITE = (255, 255, 255)

TITLE_Y1 = 268
TITLE_Y2 = 324
COUNT_Y = 394
STAGE_TOP = 472
STAGE_BOTTOM = 1138
MIN_CIRCLE_PX = 0.6

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
FONT_PATH = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
# Modern font options (Luke, 2026-10-13: "just add options"). The files
# are vendored WOFF builds of the Google Fonts bold cuts; PIL/FreeType
# loads them directly. DejaVu stays available as the legacy look.
FONTS = {
    "space-grotesk": os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  "fonts", "space-grotesk.woff"),
    "sora": os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "fonts", "sora.woff"),
    "inter": os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "fonts", "inter.woff"),
    "bricolage": os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              "fonts", "bricolage.woff"),
    "dejavu": FONT_PATH,
}
DEFAULT_SOUND = os.path.expanduser(
    "~/workspace/sound-library/audio/fart-with-reverb.mp3")


# ------------------------------------------------------------ contour
def moore_trace(mask):
    """Ordered outer boundary of a binary mask (Moore-Neighbor)."""
    m = np.pad(mask, 1)
    ys, xs = np.nonzero(m)
    s = (int(ys[0]), int(xs[0]))
    dirs = [(-1, 0), (-1, 1), (0, 1), (1, 1),
            (1, 0), (1, -1), (0, -1), (-1, -1)]
    b0 = (s[0], s[1] - 1)
    contour = [s]
    p, b = s, b0
    for _ in range(8_000_000):
        bd = (b[0] - p[0], b[1] - p[1])
        i = dirs.index(bd)
        found = None
        for k in range(1, 9):
            idx = (i + k) % 8
            d = dirs[idx]
            q = (p[0] + d[0], p[1] + d[1])
            if m[q]:
                pd = dirs[(idx - 1) % 8]
                nb = (p[0] + pd[0], p[1] + pd[1])
                found = (q, nb)
                break
        if found is None:
            break
        q, nb = found
        if q == s and nb == b0:
            break
        contour.append(q)
        p, b = q, nb
    return [(x - 1, y - 1) for (y, x) in contour]


def smooth_closed(pts, win):
    if win <= 1:
        return pts
    k = np.ones(win) / win
    ext = np.vstack([pts[-win:], pts, pts[:win]])
    out = np.empty_like(pts)
    for axis in range(2):
        sm = np.convolve(ext[:, axis], k, mode="same")
        out[:, axis] = sm[win:win + len(pts)]
    return out


def resample_closed(dense, n):
    seg = np.diff(dense, axis=0)
    seglen = np.hypot(seg[:, 0], seg[:, 1])
    total = seglen.sum() + np.hypot(*(dense[0] - dense[-1]))
    targets = np.linspace(0, total, n, endpoint=False)
    cum = np.concatenate([[0], np.cumsum(seglen), [total]])
    ext = np.vstack([dense, dense[0]])
    out = np.empty((n, 2))
    for axis in range(2):
        out[:, axis] = np.interp(targets, cum, ext[:, axis])
    return out


def extract_silhouette(image_path):
    """Outer silhouette of a colored/dark subject on a light background.

    Seed pixels are colorful or dark (a neutral gray cast shadow is
    neither). Non-seed space reachable from the border is background;
    everything else is silhouette, which fills enclosed pale details
    such as eyes. Returns (dense smoothed boundary points, image size).
    """
    img = Image.open(image_path).convert("RGB")
    hsv = np.asarray(img.convert("HSV")).astype(int)
    s = hsv[:, :, 1]
    v = hsv[:, :, 2]
    seed = ((s >= 52) & (v >= 42)) | ((v <= 175) & (s >= 16))
    seed = ndimage.binary_closing(seed, structure=np.ones((3, 3)),
                                  iterations=4)
    lab, _ = ndimage.label(~seed)
    border = set(np.unique(np.concatenate(
        [lab[0, :], lab[-1, :], lab[:, 0], lab[:, -1]]))) - {0}
    silhouette = ~np.isin(lab, list(border))
    lab2, n2 = ndimage.label(silhouette)
    if n2 == 0:
        raise RuntimeError("no silhouette found; check the background")
    sizes = ndimage.sum_labels(silhouette, lab2, range(1, n2 + 1))
    mask = lab2 == (1 + int(np.argmax(sizes)))
    mask = ndimage.binary_fill_holes(mask)
    frac = float(mask.mean())
    if not (0.02 < frac < 0.85):
        raise RuntimeError(f"silhouette covers {frac:.1%} of the frame; "
                           "extraction looks wrong")
    trace = moore_trace(mask)
    dense = smooth_closed(np.array(trace, dtype=float), 17)
    return dense, img.size, frac


# ---------------------------------------------------------------- DFT
def dft_setup(z):
    a = np.fft.fft(z - z.mean())
    order = np.argsort(-np.abs(a))
    order = order[order != 0]
    return a, order


def terms_of(a, order, k, n):
    idx = order[:k]
    freqs = np.fft.fftfreq(n, d=1.0 / n).astype(int)
    return [(int(freqs[i]), a[i] / n) for i in idx]


def loop_of(a, order, k, mean):
    masked = np.zeros_like(a)
    masked[order[:k]] = a[order[:k]]
    return mean + np.fft.ifft(masked)


def joints_at(mean, terms_k, tau):
    ks = np.array([f for f, _ in terms_k], dtype=float)
    cs = np.array([c for _, c in terms_k], dtype=complex)
    vec = cs * np.exp(2j * np.pi * ks * tau)
    return mean + np.concatenate([[0j], np.cumsum(vec)])


# -------------------------------------------------------------- layout
def fit_font(text, max_width, start_size):
    size = start_size
    while size > 24:
        fnt = ImageFont.truetype(FONT_PATH, size)
        box = ImageDraw.Draw(Image.new("RGB", (8, 8))).textbbox(
            (0, 0), text, font=fnt)
        if box[2] - box[0] <= max_width:
            return fnt
        size -= 2
    return ImageFont.truetype(FONT_PATH, size)


def draw_centered(d, cx, y, text, fnt, fill):
    box = d.textbbox((0, 0), text, font=fnt)
    d.text((cx - (box[2] - box[0]) / 2, y), text, font=fnt, fill=fill)


class Stage:
    """Maps contour-bbox coords into the drawing stage."""

    def __init__(self, dense):
        pad_x = (dense[:, 0].max() - dense[:, 0].min()) * 0.04 + 8
        pad_y = (dense[:, 1].max() - dense[:, 1].min()) * 0.04 + 8
        self.x0 = dense[:, 0].min() - pad_x
        self.y0 = dense[:, 1].min() - pad_y
        bw = (dense[:, 0].max() - dense[:, 0].min()) + 2 * pad_x
        bh = (dense[:, 1].max() - dense[:, 1].min()) + 2 * pad_y
        avail_w = W - 60
        avail_h = STAGE_BOTTOM - STAGE_TOP
        self.bw = bw
        self.bh = bh
        self.scale = min(avail_w / bw, avail_h / bh)
        self.ox = (W - bw * self.scale) / 2
        self.oy = STAGE_TOP + (avail_h - bh * self.scale) / 2

    def reveal_crop(self, iw, ih):
        """The ending reveal: crop the original image to the stage's
        padded silhouette box and place that crop exactly where the
        stage draws. The silhouette inside the crop lands on the traced
        outline (same transform), and the crop edges coincide with the
        stage box, so the revealed character reads at the same size as
        the traced one. Pasting the full photo instead leaves the
        character floating in the photo's own white margins, which
        reads as smaller than the dude (Luke, 2026-10-13).

        Returns (crop_box, nw, nh, px, py)."""
        cx0 = max(0.0, self.x0)
        cy0 = max(0.0, self.y0)
        cx1 = min(float(iw), self.x0 + self.bw)
        cy1 = min(float(ih), self.y0 + self.bh)
        nw = int(round((cx1 - cx0) * self.scale))
        nh = int(round((cy1 - cy0) * self.scale))
        px = int(round(self.ox + (cx0 - self.x0) * self.scale))
        py = int(round(self.oy + (cy0 - self.y0) * self.scale))
        return (int(cx0), int(cy0), int(cx1), int(cy1)), nw, nh, px, py

    def pts(self, z):
        return list(zip(self.ox + (z.real - self.x0) * self.scale,
                        self.oy + (z.imag - self.y0) * self.scale))

    def pt(self, z):
        return (self.ox + (z.real - self.x0) * self.scale,
                self.oy + (z.imag - self.y0) * self.scale)


def stride_pts(pts, cap):
    if len(pts) <= cap:
        return pts
    step = int(np.ceil(len(pts) / cap))
    out = pts[::step]
    if out[-1] != pts[-1]:
        out.append(pts[-1])
    return out


def allocate_frames(duration_s, ramp, ending="picture"):
    """Exact frame budget: draws + inter-stage holds + done hold +
    ending picture hold == duration * FPS. With ending="none" there is
    no done hold and no ending hold: the final stage is still drawing
    on the very last frame."""
    total = int(round(duration_s * FPS))
    if ending == "none":
        end_s = 0.0
        done_s = 0.0
    else:
        end_s = 3.9 if duration_s <= 20 else 4.0
        done_s = 0.4 if duration_s <= 20 else 1.0
    hold_s = 0.4 if duration_s <= 20 else 0.6
    end_f = int(round(end_s * FPS))
    hold_f = int(round(hold_s * FPS))
    done_f = int(round(done_s * FPS))
    draw_total = total - end_f - done_f - hold_f * (len(ramp) - 1)
    if draw_total < 30 * len(ramp):
        raise ValueError("duration too short for that many stages")
    if max(ramp) >= 50:
        weights = [0.72 + 0.11 * i for i in range(len(ramp))]
        weights[-1] *= 1.55
    else:
        weights = [0.85 + 0.10 * i for i in range(len(ramp))]
    raw = [w / sum(weights) * draw_total for w in weights]
    frames = [int(math.floor(x)) for x in raw]
    order = np.argsort([-(x - math.floor(x)) for x in raw])
    for i in range(draw_total - sum(frames)):
        frames[int(order[i % len(order)])] += 1
    assert sum(frames) == draw_total
    return frames, hold_f, done_f, end_f


# -------------------------------------------------------------- render
def main():
    ap = argparse.ArgumentParser(description="Circle Tracer video maker")
    ap.add_argument("--image", required=True)
    ap.add_argument("--subject", required=True)
    ap.add_argument("--duration", type=float, required=True)
    ap.add_argument("--ramp", required=True,
                    help="comma separated circle counts, ascending")
    ap.add_argument("--output", required=True)
    ap.add_argument("--preview", default=None,
                    help="write a contour preview PNG here")
    ap.add_argument("--preview-only", action="store_true")
    ap.add_argument("--samples", type=int, default=8192)
    ap.add_argument("--font", choices=sorted(FONTS), default="space-grotesk",
                    help="title and counter typeface (default space-grotesk)")
    ap.add_argument("--sound", choices=["fart", "none"], default="fart")
    ap.add_argument("--sound-file", default=DEFAULT_SOUND)
    ap.add_argument("--ending", choices=["picture", "freeze", "none"],
                    default="picture",
                    help="picture: cut to the original image, placed with "
                         "the stage transform so it lands on the outline. "
                         "freeze: hold the final trace frame, no overlay. "
                         "none: no ending hold at all, the final stage "
                         "draws right up to the last frame.")
    ap.add_argument("--final-fraction", type=float, default=1.0,
                    help="draw only this fraction of the final stage "
                         "(0.5 cuts the last stage off halfway)")
    args = ap.parse_args()
    global FONT_PATH
    FONT_PATH = FONTS[args.font]
    if not os.path.exists(FONT_PATH):
        raise RuntimeError(f"font file missing for {args.font}: {FONT_PATH}")
    if not (0 < args.final_fraction <= 1.0):
        raise ValueError("final-fraction must be in (0, 1]")

    ramp = [int(x) for x in args.ramp.split(",") if x.strip()]
    if ramp != sorted(ramp) or ramp[0] < 1:
        raise ValueError("ramp must be ascending positive counts")
    if max(ramp) >= args.samples // 2:
        raise ValueError("largest ramp count must be under samples/2 "
                         "for the DFT terms to be real headroom")

    dense, (iw, ih), frac = extract_silhouette(args.image)
    body = resample_closed(dense, args.samples)
    st = Stage(dense)
    print(f"image {iw}x{ih}; silhouette {frac:.1%} of frame; "
          f"dense boundary {len(dense)} pts; resampled {args.samples}")

    if args.preview:
        prev = Image.new("RGB", (W, H), BG)
        d = ImageDraw.Draw(prev)
        loop = st.pts(body[:, 0] + 1j * body[:, 1])
        loop = stride_pts(loop, 4096)
        d.line(loop + [loop[0]], fill=RED, width=3, joint="curve")
        draw_centered(d, W // 2, 60, "contour preview", 
                      ImageFont.truetype(FONT_PATH, 34), INK)
        os.makedirs(os.path.dirname(os.path.abspath(args.preview)),
                    exist_ok=True)
        prev.save(args.preview)
        print("preview:", args.preview)
        if args.preview_only:
            return 0

    z = body[:, 0] + 1j * body[:, 1]
    mean = z.mean()
    a, order = dft_setup(z)
    n = args.samples

    title1 = "How many circles"
    title2 = f"to draw {args.subject}?"
    f_title1 = fit_font(title1, W - 60, 44)
    f_title2 = fit_font(title2, W - 60, 42)
    f_count = ImageFont.truetype(FONT_PATH, 52)

    def count_text(k):
        return "1 circle" if k == 1 else f"{k} circles"

    def draw_text(d, k):
        draw_centered(d, W // 2, TITLE_Y1, title1, f_title1, INK)
        draw_centered(d, W // 2, TITLE_Y2, title2, f_title2, INK)
        draw_centered(d, W // 2, COUNT_Y, count_text(k), f_count, INK)

    faint = stride_pts(st.pts(z), 3000)
    stage_loops, stage_terms, stage_radii = {}, {}, {}
    for k in ramp:
        stage_loops[k] = loop_of(a, order, k, mean)
        stage_terms[k] = terms_of(a, order, k, n)
        stage_radii[k] = [abs(c) for _, c in stage_terms[k]]

    for k in ramp:
        for m in (n // 7, n // 3):
            j = joints_at(mean, stage_terms[k], m / n)
            err = abs(j[-1] - stage_loops[k][m])
            assert err < 1e-6, (k, err)
    print("pen-tip checks passed for every stage")

    draw_frames, hold_f, done_f, end_f = allocate_frames(
        args.duration, ramp, args.ending)
    total_frames = sum(draw_frames) + hold_f * (len(ramp) - 1) \
        + done_f + end_f
    cut_frame = total_frames - end_f
    print(f"draw frames {draw_frames}; holds {hold_f}; done {done_f}; "
          f"ending {end_f}; total {total_frames} "
          f"({total_frames / FPS:.2f}s)")

    out_dir = os.path.dirname(os.path.abspath(args.output))
    os.makedirs(out_dir, exist_ok=True)
    tmp = tempfile.NamedTemporaryFile(suffix=".mp4", dir=out_dir,
                                      delete=False)
    tmp.close()
    silent_mp4 = tmp.name
    cmd = ["ffmpeg", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-c:v", "libx264", "-pix_fmt", "yuv420p",
           "-color_range", "tv", "-colorspace", "bt709",
           "-color_primaries", "bt709", "-color_trc", "bt709",
           "-crf", "19", "-movflags", "+faststart", silent_mp4]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL)
    idx = 0
    stats = {}

    def push(img):
        nonlocal idx
        proc.stdin.write(img.tobytes())
        idx += 1

    def base(k):
        img = Image.new("RGB", (W, H), BG)
        d = ImageDraw.Draw(img)
        d.line(faint + [faint[0]], fill=FAINT_RED, width=2, joint="curve")
        return img, d

    last_img = None
    for si, k in enumerate(ramp):
        loop_pts = st.pts(stage_loops[k])
        nf = draw_frames[si]
        stage_fraction = args.final_fraction if si == len(ramp) - 1 else 1.0
        for fr in range(nf):
            frac_t = (fr + 1) / nf * stage_fraction
            m = int(round(frac_t * (n - 1)))
            img, d = base(k)
            joints = joints_at(mean, stage_terms[k], m / n)
            centers = [st.pt(j) for j in joints]
            drawn = skipped = 0
            for c, r in zip(centers[:-1], stage_radii[k]):
                rp = r * st.scale
                if rp >= MIN_CIRCLE_PX:
                    d.ellipse([c[0] - rp, c[1] - rp,
                               c[0] + rp, c[1] + rp],
                              outline=CIRCLE, width=1)
                    drawn += 1
                else:
                    skipped += 1
            d.line(centers, fill=ARM, width=1)
            trace = loop_pts[:m + 1]
            if m >= n - 1:
                trace = trace + [loop_pts[0]]
            trace = stride_pts(trace, 3000)
            d.line(trace, fill=RED, width=4, joint="curve")
            pen = centers[-1]
            d.ellipse([pen[0] - 5, pen[1] - 5, pen[0] + 5, pen[1] + 5],
                      fill=RED)
            draw_text(d, k)
            push(img)
            last_img = img
            if fr == nf - 1:
                stats[k] = (drawn, skipped)
        hold = done_f if si == len(ramp) - 1 else hold_f
        for _ in range(hold):
            push(last_img)

    if args.ending == "none":
        end_img = None
    elif args.ending == "freeze":
        end_img = last_img
    else:
        # Aligned reveal: crop the original picture to the stage's
        # padded silhouette box and place the crop on the stage
        # transform, so the character lands on the traced outline at
        # the same size, with no photo margins shrinking the read.
        src_img = Image.open(args.image).convert("RGB")
        end_img = Image.new("RGB", (W, H), BG)
        crop_box, nw, nh, px, py = st.reveal_crop(iw, ih)
        pic = src_img.crop(crop_box).resize((nw, nh), Image.LANCZOS)
        end_img.paste(pic, (px, py))
        d_end = ImageDraw.Draw(end_img)
        draw_text(d_end, ramp[-1])
    for _ in range(end_f):
        push(end_img)

    proc.stdin.close()
    proc.wait()
    assert idx == total_frames, (idx, total_frames)
    print("frames written:", idx)
    print("final stage circles drawn/skipped (sub-pixel):", stats[ramp[-1]])

    if args.sound == "none":
        os.replace(silent_mp4, args.output)
    else:
        if not os.path.exists(args.sound_file):
            raise RuntimeError(f"sound file not found: {args.sound_file}")
        cut_ms = int(cut_frame / FPS * 1000)
        if args.ending == "none":
            # No ending hold: the sound must finish as the video ends,
            # so start it one sound-length before the final frame.
            probe = subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries",
                 "format=duration", "-of", "csv=p=0", args.sound_file],
                capture_output=True, text=True, check=True)
            fart_ms = int(float(probe.stdout.strip()) * 1000)
            cut_ms = max(0, int(args.duration * 1000) - fart_ms)
        subprocess.run(
            ["ffmpeg", "-y", "-i", silent_mp4, "-i", args.sound_file,
             "-filter_complex",
             f"[1:a]aresample=48000,adelay={cut_ms}:all=1,"
             f"apad=whole_dur={args.duration}[a]",
             "-map", "0:v", "-map", "[a]", "-c:v", "copy",
             "-c:a", "aac", "-b:a", "160k", "-t", str(args.duration),
             args.output],
            check=True, stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL)
        os.unlink(silent_mp4)
    print("wrote", args.output)
    summary = {
        "subject": args.subject, "duration_s": args.duration,
        "ramp": ramp, "frames": total_frames, "cut_frame": cut_frame,
        "sound": args.sound, "samples": args.samples,
        "ending": args.ending, "final_fraction": args.final_fraction,
        "font": args.font,
        "final_stage_circles_drawn": stats[ramp[-1]][0],
        "final_stage_circles_skipped_subpixel": stats[ramp[-1]][1],
    }
    print(json.dumps(summary))
    return 0


if __name__ == "__main__":
    sys.exit(main())
