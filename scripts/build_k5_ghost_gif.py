"""5 keyframes (0-45-100-45-0) + smoothstep ghost blends with adaptive step counts."""
from __future__ import annotations

from pathlib import Path

from PIL import Image

ASSETS = Path(r"C:\Users\Dogan\.cursor\projects\C-Users-Dogan-Projects\assets")
OUT_GIF = Path(r"C:\Users\Dogan\Projects\kalori-exercise-assets\squat-k5-ghost.gif")
SIZE = 512
FRAME_MS = 88
BOTTOM_HOLD_COPIES = 2  # extra display time at deepest squat


def smoothstep(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return t * t * (3.0 - 2.0 * t)


def load_rgb(path: Path) -> Image.Image:
    return Image.open(path).convert("RGB").resize((SIZE, SIZE), Image.Resampling.LANCZOS)


def blend_smooth(a: Image.Image, b: Image.Image, t: float) -> Image.Image:
    return Image.blend(a, b, smoothstep(t))


def main() -> None:
    # Reuse best k6 keys: skip 10% / frame 5–6 filler
    names = ["squat-k6-01.jpg", "squat-k6-002.jpg", "squat-k6-003.jpg", "squat-k6-004.jpg", "squat-k6-01.jpg"]
    paths = [ASSETS / n for n in names]
    for p in paths:
        if not p.exists():
            raise SystemExit(f"Missing {p}")

    kf = [load_rgb(p) for p in paths]
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
