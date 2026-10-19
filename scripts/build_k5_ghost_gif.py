"""5 keyframes (0-45-100-45-0) + smoothstep ghost blends with adaptive step counts."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageChops

ASSETS = Path(r"C:\Users\Dogan\.cursor\projects\C-Users-Dogan-Projects\assets")
OUT_GIF = Path(r"C:\Users\Dogan\Projects\kalori-exercise-assets\squat-k5-ghost.gif")
SIZE = 512
FRAME_MS = 88
BOTTOM_HOLD_COPIES = 2  # extra display time at deepest squat
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


def _head_span(box: tuple[int, int, int, int]) -> int:
    """Head/shoulder band height — stable scale reference across squat poses."""
    h = max(1, box[3] - box[1])
    return max(1, int(h * 0.24))


def normalize_scale_and_feet(ref: Image.Image, im: Image.Image) -> Image.Image:
    """Match head scale + foot anchor to standing reference (not full bbox height)."""
    if im is ref:
        return im.copy()

    ref_box = _content_bbox(ref)
    im_box = _content_bbox(im)
    ref_head = _head_span(ref_box)
    im_head = _head_span(im_box)
    scale = ref_head / im_head

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
    """Normalize every frame including standing so GIF loop has one scale."""
    ref = keyframes[0]
    return [normalize_scale_and_feet(ref, im) for im in keyframes]


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

    frames: list[Image.Image] = []
    for i_from, i_to, steps in segments:
        a, b = kf[i_from], kf[i_to]
        frames.append(a)
        for s in range(1, steps + 1):
            t = s / (steps + 1)
            frames.append(blend_smooth(a, b, t))
        if i_to == 2:
            for _ in range(BOTTOM_HOLD_COPIES):
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
