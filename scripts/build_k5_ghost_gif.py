"""5 keyframes (0-45-100-45-0) + smoothstep ghost blends with adaptive step counts."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageChops

ASSETS = Path(r"C:\Users\Dogan\.cursor\projects\C-Users-Dogan-Projects\assets")
OUT_GIF = Path(r"C:\Users\Dogan\Projects\kalori-exercise-assets\squat-k5-ghost.gif")
SIZE = 512
FRAME_MS = 88
BOTTOM_HOLD_COPIES = 2  # extra display time at deepest squat
STAND_HOLD_COPIES = 3  # end on exact standing key (avoids loop snap)
BG = (233, 233, 233)
BG_TOL = 28


def smoothstep(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return t * t * (3.0 - 2.0 * t)


def load_rgb(path: Path) -> Image.Image:
    return Image.open(path).convert("RGB").resize((SIZE, SIZE), Image.Resampling.LANCZOS)


def _content_bbox(im: Image.Image) -> tuple[int, int, int, int]:
    bg = Image.new("RGB", im.size, BG)
    diff = ImageChops.difference(im, bg).convert("L")
    # ignore tiny compression noise
    mask = diff.point(lambda p: 255 if p > BG_TOL else 0)
    box = mask.getbbox()
    if not box:
        return (0, 0, im.width, im.height)
    return box


def _box_h(box: tuple[int, int, int, int]) -> int:
    return max(1, box[3] - box[1])


def _band_content_width(im: Image.Image, y0: int, y1: int) -> int:
    y0 = max(0, y0)
    y1 = min(im.height, max(y0 + 1, y1))
    band = im.crop((0, y0, im.width, y1))
    bg = Image.new("RGB", band.size, BG)
    diff = ImageChops.difference(band, bg).convert("L")
    mask = diff.point(lambda p: 255 if p > BG_TOL else 0)
    box = mask.getbbox()
    if not box:
        return 0
    return box[2] - box[0]


def _min_upper_band_width(im: Image.Image, box: tuple[int, int, int, int]) -> int:
    """Narrowest band under arms — proxy for head/face width in side view."""
    h = _box_h(box)
    band_h = max(10, int(h * 0.09))
    y_start = box[1] + int(h * 0.04)
    y_end = box[1] + int(h * 0.16)
    best = 10**9
    for y in range(y_start, min(y_end, box[3] - band_h)):
        w = _band_content_width(im, y, y + band_h)
        if 0 < w < best:
            best = w
    return max(1, best)


def _uniform_body_scale(
    ref: Image.Image,
    ref_box: tuple[int, int, int, int],
    im: Image.Image,
    im_box: tuple[int, int, int, int],
) -> float:
    """Same figure zoom (never squash shorter); visible height comes from pose only."""
    ref_h = _box_h(ref_box)
    im_h = _box_h(im_box)
    if im_h >= ref_h * 0.98:
        return 1.0
    rw = _min_upper_band_width(ref, ref_box)
    iw = _min_upper_band_width(im, im_box)
    # Only upscale if AI drew head/body thinner — never shrink (avoids "zoomed out" squat)
    return max(1.0, rw / iw)


def normalize_scale_and_feet(ref: Image.Image, im: Image.Image) -> Image.Image:
    """Lock figure scale to standing, anchor feet; pose may shorten visible height (bend, not shrink)."""
    return normalize_scale_and_feet_with_scale(ref, im, None)


def normalize_scale_and_feet_with_scale(
    ref: Image.Image, im: Image.Image, scale: float | None = None
) -> Image.Image:
    ref_box = _content_bbox(ref)
    im_box = _content_bbox(im)
    if ref_box == im_box and im is ref:
        return im.copy()
    if scale is None:
        scale = _uniform_body_scale(ref, ref_box, im, im_box)

    crop = im.crop(im_box)
    new_w = max(1, int(round(crop.width * scale)))
    new_h = max(1, int(round(crop.height * scale)))
    scaled = crop.resize((new_w, new_h), Image.Resampling.LANCZOS)

    canvas = Image.new("RGB", ref.size, BG)
    ref_cx = (ref_box[0] + ref_box[2]) // 2
    ref_foot_y = ref_box[3]
    paste_x = ref_cx - new_w // 2
    paste_y = ref_foot_y - new_h
    canvas.paste(scaled, (paste_x, paste_y))
    return canvas


def normalize_keyframes(keyframes: list[Image.Image]) -> list[Image.Image]:
    ref_raw = keyframes[0]
    # Canonical standing canvas — all frames match this
    ref = normalize_scale_and_feet_with_scale(ref_raw, ref_raw)
    ref_box = _content_bbox(ref)
    out: list[Image.Image] = []
    for i, im in enumerate(keyframes):
        im_box = _content_bbox(im)
        scale = _uniform_body_scale(ref, ref_box, im, im_box)
        # Key 4 (ascent): AI often shrinks vs keys 2–3 — keep at least mid-ascent height
        if i == 3 and len(out) >= 2:
            h2 = _box_h(_content_bbox(out[1]))
            h3 = _box_h(_content_bbox(out[2]))
            min_ascent_h = int(h3 + 0.55 * (h2 - h3))
            scale = max(scale, min_ascent_h / _box_h(im_box))
        out.append(normalize_scale_and_feet_with_scale(ref, im, scale))
    # Lock frame 1 and 5 (standing) to identical pixels
    out[0] = ref.copy()
    out[-1] = ref.copy()
    return out


def blend_smooth(a: Image.Image, b: Image.Image, t: float) -> Image.Image:
    return Image.blend(a, b, smoothstep(t))


def main() -> None:
    # Reuse best k6 keys: skip 10% / frame 5–6 filler
    names = ["squat-k6-01.jpg", "squat-k6-002.jpg", "squat-k6-003.jpg", "squat-k6-004.jpg", "squat-k6-01.jpg"]
    paths = [ASSETS / n for n in names]
    for p in paths:
        if not p.exists():
            raise SystemExit(f"Missing {p}")

    kf = normalize_keyframes([load_rgb(p) for p in paths])
    # (from_idx, to_idx, ghost_steps) — more steps on large leg travel
    segments = [
        (0, 1, 7),  # stand -> mid down
        (1, 2, 10),  # mid -> bottom
        (2, 3, 10),  # bottom -> mid up
        (3, 4, 7),  # mid -> stand
    ]

    frames: list[Image.Image] = [kf[0]]
    for i_from, i_to, steps in segments:
        a, b = kf[i_from], kf[i_to]
        for s in range(1, steps + 1):
            t = s / steps
            frames.append(blend_smooth(a, b, t))
        if i_to == 2:
            for _ in range(BOTTOM_HOLD_COPIES):
                frames.append(b.copy())
        elif i_to == 4:
            for _ in range(STAND_HOLD_COPIES):
                frames.append(b.copy())

    frames[0].save(
        OUT_GIF,
        save_all=True,
        append_images=frames[1:],
        duration=FRAME_MS,
        loop=0,
        optimize=True,
    )
    print(
        OUT_GIF,
        "keyframes",
        len(kf),
        "gif_frames",
        len(frames),
        "bytes",
        OUT_GIF.stat().st_size,
    )


if __name__ == "__main__":
    main()
